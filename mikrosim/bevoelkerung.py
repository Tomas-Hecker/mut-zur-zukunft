"""Synthetische Bevölkerung für die Mikrosimulation „Wir können uns die Zukunft leisten“.

Erzeugt rund 45.000 künstliche Haushalte (und erwachsene Kinder im Elternhaus als eigene Steuerfälle) mit Gewichten, die zusammen
die gut 41 Mio. Haushalte in Deutschland darstellen. Jeder Haushalt hat Alter, Erwachsene, Kinder, Löhne, Renten, Gewinne,
Kapitalerträge, Mieten, Vermögen (eigenes Haus, andere Immobilien, Geld und Wertpapiere, Betriebe) und eine Sparquote.

Geeicht wird auf öffentliche Eckwerte (siehe ECKWERTE und eichung.md). Alles ist eine Schätzung: Die Haushalte sind künstlich,
aber so gebaut, dass Summen und Verteilungen zu den amtlichen Zahlen passen. Fester Zufallsstartwert, das Ergebnis ist immer gleich.

Aufruf: python3 bevoelkerung.py  ->  bevoelkerung.json
"""
import json
import math
import os

import numpy as np

HIER = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20261114)

# ---------------------------------------------------------------- Eckwerte (Quellen in eichung.md)
ECKWERTE = {
    "haushalte_mio": 41.1,           # Mikrozensus 2025: 41,1 Mio. Privathaushalte
    "konsum_mrd": 2300.2,            # Konsumausgaben ohne Organisationen ohne Erwerbszweck, wie Version 31 (Blatt Annahmen, Konsum)
    "mietwert_mrd": 214.5,           # Mietwert selbst genutzter Wohnungen nach Eurostat, wie Version 31 (Nutzwert)
    "vermoegen_bio": 16.6,           # Eichpunkt „Vermögen heute“ (PHF 2023 plus fehlende Reiche), Thread Kurzfassung
    "eigentuemer_quote": 0.42,       # Mikrozensus 2022: 41,9 % der Haushalte wohnen im Eigentum
    "bruttoloehne_mrd": 2036.3,      # VGR 2025 (Destatis, Fachserie 18 Reihe 1.4, Tabelle 2.1.8): Bruttolöhne und -gehälter der Inländer
    "heimkredit_bio": 1.15,          # Restschuld auf selbst genutzte Häuser und Wohnungen: Wohnungsbaukredite an private Haushalte rund
                                     # 1,58 Bio. € (Bundesbank 2025: gut 35 % des BIP), davon rund drei Viertel für das eigene Heim (Schätzung)
    "nebenjob_mio": 3.3,             # Minijob als Nebenjob (Minijob-Zentrale, Quartalsbericht 2025: rund 3,3 Mio.)
}

# Haushaltstypen: Anzahl in Mio. (Mikrozensus 2024/25, gerundet und vereinfacht), Stichprobengröße
TYPEN = {
    #            Mio.  n      Erw  Rentner
    "single":   (11.8, 9000, 1, 0),   # allein, unter 65
    "allein_k": (1.5,  2500, 1, 0),   # alleinerziehend mit Kindern unter 18
    "allein_v": (1.0,  1200, 1, 0),   # alleinerziehend, nur volljährige Kinder im Haus
    "paar":     (5.8,  4500, 2, 0),   # Paar unter 65 ohne Kinder im Haus
    "paar_k":   (6.9,  6000, 2, 0),   # Paar mit Kindern unter 18
    "paar_v":   (2.4,  2000, 2, 0),   # Paar, nur volljährige Kinder im Haus
    "rentner1": (6.3,  4500, 1, 1),   # allein, 65 und älter
    "rentner2": (4.9,  4000, 2, 1),   # Paar, 65 und älter
}
KIND_ERW_MIO = 4.0                    # erwachsene Kinder und Verwandte im Haushalt mit eigenem Einkommen, als eigene Steuerfälle
KIND_ERW_N = 3000

# Vermögensstufen des Eichpunkts (version-31/aufkommen/vermoegen-heute.json): Untergrenze, Haushalte, Mittelwert, Zusammensetzung
STUFEN = [
    # lo,     hi,      Haushalte,  Mittel,     Heim, andere Immob., Geld/WP, Betriebe
    (-1e9,    1e5,     20212500,   22000,      20, 5, 70, 5),
    (1e5,     2e5,     5362500,    145000,     60, 8, 27, 5),
    (2e5,     4e5,     5362500,    290000,     62, 10, 23, 5),
    (4e5,     8e5,     6311250,    560000,     50, 20, 22, 8),
    (8e5,     1e6,     1320000,    895000,     40, 25, 23, 12),
    (1e6,     1e7,     2590500,    2100000,    20, 30, 22, 28),
    (1e7,     1e8,     86749,      21000000,   5, 25, 20, 50),
    (1e8,     4e10,    4001,       450000000,  1, 10, 14, 75),
]
EIGEN_P = [0.06, 0.62, 0.78, 0.85, 0.88, 0.90, 0.93, 0.95]   # Anteil der Eigentümer je Stufe (Schätzung, PHF: mit dem Vermögen steigend)

# Erträge (wie Eichpunkt): Mieten 3,5 %, Geld und Wertpapiere 3 %, Betriebe 7 % des Werts, Mietwert rund 3,2 % des Hauswerts
R_MIETE, R_GELD, R_BETRIEB = 0.035, 0.03, 0.07
MIETE_STEUERPFLICHTIG = 0.35  # nach Abschreibung und Zinsen: Einkünfte aus Vermietung in der Steuerstatistik rund ein Drittel der Mieten
AUSSCHUETTUNG = 0.50          # ausgeschütteter Teil der Betriebsgewinne großer Vermögen, Rest bleibt in der Firma (GmbH)

# ---------------------------------------------------------------- Hilfen
def lognorm(median, sigma, n):
    return median * np.exp(sigma * rng.standard_normal(n))


def wahl(n, p):
    keys = list(p)
    probs = np.array([p[k] for k in keys], float)
    return np.array(keys)[rng.choice(len(keys), size=n, p=probs / probs.sum())]


def alter(n, lo, hi, modus):
    a = rng.triangular(lo, modus, hi, n)
    return np.floor(a).astype(int)


def lohn_vz(n, a):   # Vollzeit: Median 3.950 € im Monat, Streuung 0,42 (Annahmen des Rechenmodells), mit Altersprofil und Spitze
    prof = np.interp(a, [18, 25, 32, 45, 58, 66], [0.62, 0.78, 0.95, 1.08, 1.06, 1.0])
    w = 12 * 3950 * prof * np.exp(0.40 * rng.standard_normal(n))
    top = rng.random(n) < 0.05   # obere 5 %: Pareto ab rund 100.000 € (Steuerstatistik: dünner, langer Rand)
    w[top] = np.maximum(w[top], 100000 * (1 - rng.random(top.sum())) ** (-1 / 2.2))
    return np.minimum(w, 3e6)


def lohn_tz(n):
    return np.clip(12 * 1650 * np.exp(0.5 * rng.standard_normal(n)), 7300, 60000)


def selbst(n):    # Gewinn kleiner und mittlerer Selbständiger
    return np.clip(lognorm(45000, 0.95, n), 6000, 5e6)


def beamte(n, a):
    prof = np.interp(a, [25, 40, 60], [0.8, 1.0, 1.15])
    return 12 * 4200 * prof * np.exp(0.25 * rng.standard_normal(n))


# ---------------------------------------------------------------- Personen und Einkommen je Haushalt
def erwerb(n, p):
    return wahl(n, p)


ERW_SINGLE = {"vz": 0.50, "tz": 0.12, "mini": 0.04, "selbst": 0.08, "beamt": 0.04, "bg": 0.11, "stud": 0.07, "ohne": 0.04}
ERW_ALLEIN = {"vz": 0.35, "tz": 0.30, "mini": 0.05, "selbst": 0.03, "beamt": 0.02, "bg": 0.25}
ERW_MITTE = {"vz": 0.56, "tz": 0.14, "mini": 0.05, "selbst": 0.09, "beamt": 0.05, "ohne": 0.08, "bg": 0.03}
ERW_ELTERN1 = {"vz": 0.78, "selbst": 0.10, "beamt": 0.06, "bg": 0.04, "tz": 0.02}
ERW_ELTERN2 = {"vz": 0.30, "tz": 0.45, "mini": 0.08, "ohne": 0.12, "selbst": 0.05}
ERW_KIND = {"vz": 0.45, "tz": 0.25, "mini": 0.10, "ohne": 0.15, "bg": 0.05}


def leer(n):
    f = ["lohn1", "std1", "lohn2", "std2", "mini", "rente", "gewinn", "kap", "gmbh", "aus", "transfer", "verm", "vermiet",
         "vermietCash", "pension", "miet", "hb", "pkv", "vorsorge", "unterhalt"]
    d = {k: np.zeros(n) for k in f}
    for k in ["erw", "kinder", "kid6", "kid3", "kinderlos", "rentner", "bs", "allein", "vollj", "pg", "bjob", "beamter", "selbst", "bg"]:
        d[k] = np.zeros(n, int)
    return d


def person(d, i_slot, st, a):
    """Trägt für jede Zeile die Erwerbsart st in die Person i_slot (1 oder 2) ein."""
    n = len(st)
    L, S = f"lohn{i_slot}", f"std{i_slot}"
    m = st == "vz"; d[L][m] += lohn_vz(m.sum(), a[m]); d[S][m] = 40
    m = st == "tz"; d[L][m] += lohn_tz(m.sum()); d[S][m] = 22
    m = st == "mini"; d["mini"][m] += 12 * 603 * rng.uniform(0.4, 1.0, m.sum())
    m = st == "selbst"; g = selbst(m.sum()); d["gewinn"][m] += g; d["selbst"][m] = 1
    # Krankenversicherung der Selbständigen: 40 % privat (rund 6.500 € im Jahr), sonst freiwillig gesetzlich, rund 20 % bis zur Grenze
    d["pkv"][m] += np.where(rng.random(m.sum()) < 0.4, 6500, 0.20 * np.clip(g, 14000, 69750))
    m = st == "beamt"; d["pension"][m] += beamte(m.sum(), a[m]); d["beamter"][m] = 1; d["pkv"][m] += 3600
    m = st == "stud"; d["mini"][m] += 12 * 603 * rng.uniform(0.3, 1.0, m.sum()); d["verm"][m] += 12 * rng.uniform(300, 700, m.sum())


def kinder(d, n_k, kopf_alter):
    d["kinder"] += n_k
    for j in range(int(n_k.max())):
        hat = n_k > j
        alt = rng.integers(0, 18, len(n_k))
        alt = np.minimum(alt, np.maximum(0, kopf_alter - 20))
        d["kid6"] += (hat & (alt < 6)).astype(int)
        d["kid3"] += (hat & (alt < 3)).astype(int)


def baue_typ(typ):
    mio, n, erw, rentner = TYPEN[typ]
    d = leer(n)
    d["erw"][:] = erw
    d["typ"] = np.array([typ] * n)
    d["w"] = np.full(n, mio * 1e6 / n)
    if typ == "single":
        a = alter(n, 18, 65, 30); st = erwerb(n, ERW_SINGLE); st[(a > 30) & (st == "stud")] = "vz"
        person(d, 1, st, a); d["kinderlos"][:] = (rng.random(n) < 0.75) & (a >= 23)
    elif typ == "allein_k":
        a = alter(n, 20, 60, 38); st = erwerb(n, ERW_ALLEIN); person(d, 1, st, a)
        kinder(d, rng.choice([1, 2, 3], n, p=[0.6, 0.3, 0.1]), a); d["allein"][:] = 1
    elif typ == "allein_v":
        a = alter(n, 40, 65, 54); st = erwerb(n, {**ERW_MITTE, "bg": 0.10}); person(d, 1, st, a)
        d["vollj"][:] = rng.random(n) < 0.5; d["unterhalt"][:] = np.where(d["vollj"] > 0, 600, 0)
    elif typ in ("paar", "paar_v"):
        a = alter(n, 22 if typ == "paar" else 42, 65, 55 if typ == "paar" else 54)
        st = erwerb(n, ERW_MITTE); person(d, 1, st, a); person(d, 2, erwerb(n, {**ERW_MITTE, "bg": 0.0}), a)
        d["kinderlos"][:] = (rng.random(n) < (0.45 if typ == "paar" else 0.0)) & (a >= 23)
        if typ == "paar_v":
            d["vollj"][:] = rng.random(n) < 0.4; d["unterhalt"][:] = np.where(d["vollj"] > 0, 650, 0)
    elif typ == "paar_k":
        a = alter(n, 21, 62, 40)
        st = erwerb(n, ERW_ELTERN1); person(d, 1, st, a); person(d, 2, erwerb(n, ERW_ELTERN2), a)
        kinder(d, rng.choice([1, 2, 3, 4], n, p=[0.47, 0.40, 0.10, 0.03]), a)
        d["vollj"][:] = (rng.random(n) < 0.12) & (a > 42); d["unterhalt"][:] = np.where(d["vollj"] > 0, 650, 0)
    elif typ in ("rentner1", "rentner2"):
        a = alter(n, 65, 97, 72)
        frau = rng.random(n) < (0.73 if typ == "rentner1" else 0.5)
        r = np.where(frau, lognorm(12 * 1550, 0.40, n), lognorm(12 * 1800, 0.40, n))   # Frauen mit Witwenrente
        if typ == "rentner2":
            r = lognorm(12 * 1850, 0.40, n) + lognorm(12 * 1100, 0.50, n)   # mit Betriebs- und Zusatzrenten
        pens = rng.random(n) < (0.10 if typ == "rentner1" else 0.13)   # Pensionäre und Hinterbliebene
        d["rente"][:] = np.where(pens, np.where(rng.random(n) < 0.5, r * 0.3, 0), r)   # Pensionäre oft mit kleiner Rente
        d["pension"][pens] += lognorm(12 * 3400, 0.30, pens.sum()) * (1.4 if typ == "rentner2" else 1.0)
        d["beamter"][pens] = 1; d["pkv"][pens] += 3600 * erw
        jobs = rng.random(n) < (0.09 if typ == "rentner1" else 0.12)
        d["mini"][jobs] += 12 * 603 * rng.uniform(0.5, 1.0, jobs.sum())
        d["rentner"][:] = 1; d["bs"][:] = 1; d["kinderlos"][:] = rng.random(n) < 0.18
        st = np.array(["rente"] * n)
    a = np.asarray(a)
    d["alter"] = a
    if not typ.startswith("rentner"):
        # ohne Arbeit mit 55 bis 64: Erwerbsminderungs- oder Frührente (heutige Rentner mit Bestandsschutz)
        # Arbeitslosengeld, Elterngeld, Wohngeld, Krankengeld und andere Leistungen in Geld (zusammen rund 70 Mrd. €), vereinfacht als
        # Leistung ohne Steuer bei einem Teil der Haushalte ohne volle Arbeit; im Kern wie Ausgaben aus Vermögen gezählt (verm)
        ls = ((st == "ohne") | (st == "tz") | (st == "mini")) & (rng.random(n) < 0.45)
        d["leist"] = np.where(ls, lognorm(12 * 1000, 0.5, n), 0.0)
        kg = (st == "vz") & (rng.random(n) < 0.08)   # Kranken-, Eltern- und Kurzarbeitergeld bei Beschäftigten
        d["leist"] += np.where(kg, lognorm(12 * 800, 0.5, n), 0.0)
        fr = (st == "ohne") & (a >= 55) & (rng.random(n) < 0.6)
        d["rente"][fr] += lognorm(12 * 1250, 0.35, fr.sum()); d["rentner"][fr] = 1; d["bs"][fr] = 1
    else:
        # Betriebs-, Zusatz- und Privatrenten: knapp die Hälfte der Rentnerhaushalte
        d["leist"] = np.zeros(n)
        br = rng.random(n) < 0.50
        d["rente"][br] += lognorm(12 * 450, 0.8, br.sum()) * erw
    # Bürgergeld (Grundsicherung): Regelbedarf plus Miete und Heizung, ohne Einkommen aus Arbeit
    if typ.startswith("rentner"):
        gs = d["rente"] + d["pension"] < 12 * (800 if erw == 1 else 1300)
        gs &= rng.random(n) < 0.45
    else:
        gs = (st == "bg")
    for k in ["lohn1", "lohn2", "std1", "std2", "gewinn", "pension"]:
        if not typ.startswith("rentner"):
            d[k][gs] = 0
    regel = np.where(d["erw"] == 2, 2 * 506, 563) + 400 * d["kinder"]
    kdu = np.where(d["erw"] == 2, 650, 520) + 120 * d["kinder"]
    d["transfer"][gs] = np.maximum(0, 12 * (regel[gs] + kdu[gs]) - d["rente"][gs] - 0.7 * d["mini"][gs])
    d["bg"][gs] = 1
    d["leist"][gs] = 0
    return d


def baue_kind_erw():
    n = KIND_ERW_N
    d = leer(n)
    d["erw"][:] = 1
    d["typ"] = np.array(["kind_erw"] * n)
    d["w"] = np.full(n, KIND_ERW_MIO * 1e6 / n)
    a = alter(n, 18, 35, 21)
    st = erwerb(n, ERW_KIND)
    person(d, 1, st, a)
    d["alter"] = a
    d["kinderlos"][:] = a >= 23
    d["bg"][:] = 0
    d["leist"] = np.where((st != "vz") & (rng.random(n) < 0.3), lognorm(12 * 600, 0.5, n), 0.0)   # BAföG, Ausbildungsgeld, Arbeitslosengeld
    return d


def zusammen(teile):
    out = {}
    for k in teile[0]:
        out[k] = np.concatenate([t[k] for t in teile])
    return out


# ---------------------------------------------------------------- Vermögen: Rang aus Einkommen und Alter, Höhe aus dem Eichpunkt
def stufen_grenzen():
    h = np.array([s[2] for s in STUFEN], float)
    cum = np.concatenate([[0], np.cumsum(h) / h.sum()])
    return cum


def form_c(lo, hi, mittel):
    """W = lo·(hi/lo)^(u^c): c so, dass der Mittelwert stimmt (Bisektion, Mittel über ein feines Raster)."""
    u = (np.arange(20000) + 0.5) / 20000
    f = lambda c: (lo * (hi / lo) ** (u ** c)).mean()
    a, b = 0.05, 20.0
    for _ in range(80):
        m = math.sqrt(a * b)
        if f(m) > mittel:
            a = m
        else:
            b = m
    return math.sqrt(a * b)


def q_vermoegen(p):
    cum = stufen_grenzen()
    W = np.zeros_like(p)
    for j, (lo, hi, nh, mittel, *_rest) in enumerate(STUFEN):
        m = (p >= cum[j]) & (p < cum[j + 1]) if j < len(STUFEN) - 1 else (p >= cum[j])
        u = np.clip((p[m] - cum[j]) / (cum[j + 1] - cum[j]), 1e-9, 1 - 1e-9)
        if j == 0:   # 12 % mit Schulden (im Mittel −15.000 €), sonst 100.000 · u^2,7 (Mittel 22.000 €)
            neg = u < 0.12
            W[m] = np.where(neg, -30000 * (1 - u / 0.12), 1e5 * (np.maximum(u - 0.12, 0) / 0.88) ** 2.70)
        elif j == len(STUFEN) - 1:   # Pareto ab 100 Mio. €, Mittel 450 Mio. € (alpha 1,286), gedeckelt bei 40 Mrd. €
            W[m] = np.minimum(lo * (1 - u) ** (-1 / 1.2857), hi)
        else:
            c = FORM[j]
            W[m] = lo * (hi / lo) ** (u ** c)
    return W


FORM = {j: form_c(s[0], s[1], s[3]) for j, s in enumerate(STUFEN) if 0 < j < len(STUFEN) - 1}


def gewichteter_rang(x, w):
    o = np.argsort(x, kind="stable")
    cw = np.cumsum(w[o])
    p = np.empty_like(x, dtype=float)
    p[o] = (cw - 0.5 * w[o]) / cw[-1]
    return p


def vermoegen(d):
    n = len(d["w"])
    hh = d["typ"] != "kind_erw"
    eink = d["lohn1"] + d["lohn2"] + d["gewinn"] + d["pension"] + d["rente"] + d["mini"]
    eink_j = eink / np.where(d["erw"] == 2, 1.5, 1.0)
    z_ink = np.log(np.maximum(eink_j, 3000))
    z_ink = (z_ink - z_ink[hh].mean()) / z_ink[hh].std()
    alt = np.clip((d["alter"] - 25) / 40, 0, 1.2)
    z = 0.6 * z_ink + 0.55 * alt + 0.3 * d["selbst"] + 0.75 * rng.standard_normal(n)   # PHF 2023: Median nach Alter 55-74 rund 140.000 €
    z[d["bg"] > 0] -= 3.0                      # Bürgergeld: Schonvermögen, fast nichts
    p = gewichteter_rang(np.where(hh, z, -99), np.where(hh, d["w"], 0.0))
    return p, hh


def klone(d, p):
    """Teilt reiche Haushalte in Klone mit eigenem Rang im Rand der Verteilung, damit der Rand fein aufgelöst ist."""
    w = d["w"]
    cum = np.cumsum(np.ones_like(w))  # nur Platzhalter
    teile = {k: [] for k in d}
    teile["p"] = []
    o = np.argsort(p)
    # Massengrenzen je Haushalt im Rang
    pw = w / w[d["typ"] != "kind_erw"].sum()
    for i in range(len(w)):
        m = 1
        if d["typ"][i] != "kind_erw":
            if p[i] > 0.999:
                m = 40
            elif p[i] > 0.99:
                m = 15
            elif p[i] > 0.95:
                m = 6
        lo = p[i] - pw[i] / 2
        for j in range(m):
            for k in d:
                v = d[k][i]
                teile[k].append(v / m if k == "w" else v)
            teile["p"].append(lo + pw[i] * (j + 0.5) / m if m > 1 else p[i])
    return {k: np.array(v) for k, v in teile.items()}


def verteile_vermoegen(d):
    n = len(d["w"])
    hh = d["typ"] != "kind_erw"
    W = np.where(hh, q_vermoegen(np.clip(d["p"], 0, 1 - 1e-12)), np.maximum(0, lognorm(4000, 1.0, n)))
    W[d["bg"] > 0] = np.minimum(W[d["bg"] > 0], rng.uniform(0, 12000, (d["bg"] > 0).sum()))
    cum = stufen_grenzen()
    stufe = np.clip(np.searchsorted(cum, d["p"], side="right") - 1, 0, len(STUFEN) - 1)
    stufe[~hh] = 0
    comp = np.array([s[4:8] for s in STUFEN], float) / 100
    pe = np.array(EIGEN_P)[stufe]
    eigen = hh & (rng.random(n) < pe) & (W > 5000) & (d["bg"] == 0)
    # bei jungen Haushalten mit wenig Vermögen: Eigentum mit großem Kredit; Rentner fast immer schuldenfrei
    c = comp[stufe]
    heim_anteil = np.where(eigen, np.minimum(0.92, c[:, 0] / np.maximum(pe, 0.05)), 0.0)
    rest = np.where(eigen[:, None], c[:, 1:], c[:, 1:])
    rest = rest / rest.sum(1, keepdims=True)
    netto_heim = W * heim_anteil
    uebrig = W - netto_heim
    imm, geld, betr = (uebrig[:, None] * rest).T
    geld = np.where(W < 0, W, geld)          # Schulden ohne Haus: Konsumkredite
    imm = np.where(W < 0, 0, imm); betr = np.where(W < 0, 0, betr)
    # nur Selbständige und große Vermögen halten Betriebe; sonst wird der Betriebsanteil Geld
    hat_betrieb = (d["selbst"] > 0) | (W >= 1e6)
    geld = geld + np.where(hat_betrieb, 0, betr); betr = np.where(hat_betrieb, betr, 0)
    # bezahlter Anteil des Hauses (PHF 2023: gut die Hälfte der Eigentümer zahlt noch ab, junge fast alle, Rentner selten).
    # Wer abzahlt, hat mit dem Alter mehr bezahlt. Die Restschuld wird danach auf die Wohnungsbaukredite für das eigene Heim geeicht.
    mit_kredit = np.where(d["rentner"] > 0, rng.random(n) < 0.08, rng.random(n) < np.interp(d["alter"], [25, 40, 55, 64], [0.9, 0.75, 0.45, 0.3]))
    mit_kredit |= (stufe == 0)
    hb_k = np.clip(rng.beta(2, 2, n) * np.interp(d["alter"], [25, 40, 55, 70], [0.5, 0.8, 1.2, 1.5]), 0.1, 0.97)
    hb_k = np.where(stufe == 0, np.minimum(hb_k, 0.35), hb_k)
    def haus(f):
        hb = np.where(mit_kredit, 1 - f * (1 - hb_k), 1.0)
        hw = np.where(eigen, np.maximum(netto_heim, 1) / hb, 0.0)
        hw = np.where(eigen, np.clip(hw, 120000, 12e6), 0)   # kleinere Vermögen kaufen keine Villen
        hb = np.where(eigen, np.clip(netto_heim / np.maximum(hw, 1), 0, 1), 0)
        return hw, hb
    lo, hi = 0.0, 1.5
    for _ in range(40):
        f = (lo + hi) / 2; hw, hb = haus(f)
        schuld = (d["w"] * hw * (1 - hb)).sum() / 1e12
        if schuld > ECKWERTE["heimkredit_bio"]: hi = f
        else: lo = f
    hauswert, hb = haus((lo + hi) / 2)
    d.update(W=W, stufe=stufe, eigen=eigen.astype(int), hauswert=hauswert, heim_netto=np.where(eigen, hauswert * hb, 0),
             immo=imm, geld=geld, betrieb=betr, hb=hb)
    # Vermögen nach der Klammer neu zusammenzählen
    d["W"] = d["heim_netto"] + imm + geld + betr
    return d


def ertraege(d):
    d["miet"] = 0.032 * d["hauswert"]
    d["vermietCash"] = R_MIETE * d["immo"]
    d["vermiet"] = MIETE_STEUERPFLICHTIG * d["vermietCash"]
    # Ausgezahlte Zinsen und Dividenden: kleine und mittlere Vermögen liegen vor allem auf Konten und in Versicherungen, die nichts
    # ausschütten (Bundesbank, Geldvermögensrechnung), große in Aktien und Fonds
    rendite = np.array([0.010, 0.015, 0.015, 0.020, 0.025, 0.030, 0.030, 0.030])[d["stufe"]]
    d["kap"] = rendite * np.maximum(d["geld"], 0)
    gross = d["W"] >= 1e6
    gew = R_BETRIEB * d["betrieb"]
    d["aus"] = np.where(gross, AUSSCHUETTUNG * gew, 0.0)
    d["gmbh"] = np.where(gross, (1 - AUSSCHUETTUNG) * gew, 0.0)
    # kleinere Betriebe: Gewinn steckt schon im Gewinn der Selbständigen; mindestens 7 % des Betriebswerts
    d["gewinn"] = np.where(~gross & (d["selbst"] > 0), np.maximum(d["gewinn"], gew), d["gewinn"])
    # Verzehr von Erspartem im Alter (Konsum aus Vermögen): 1 % mit 65 bis 3,5 % mit 90 des Geldvermögens
    verz = np.interp(d["alter"], [65, 75, 90], [0.01, 0.02, 0.035]) * (d["rentner"] > 0)   # Ältere entsparen langsam (PHF)
    d["verm"] = d["verm"] + verz * np.maximum(d["geld"], 0)
    return d


# ---------------------------------------------------------------- Konsum und Sparen
def sparquote(d, verf, a0):
    """Sparquote nach Einkommen (EVS 2018: unten Entsparen, oben 20 bis 40 %), Alter und Vermögen."""
    ln = np.log(np.maximum(verf, 5000) / 30000)
    s = a0 + 0.10 * ln
    s = np.where(d["rentner"] > 0, s - 0.05, s)
    s = np.where(d["bg"] > 0, 0.0, s)
    s = np.where(d["transfer"] > 0, 0.0, s)
    return np.clip(s, -0.10, 0.75)


def main():
    teile = [baue_typ(t) for t in TYPEN] + [baue_kind_erw()]
    d = zusammen(teile)
    p, hh = vermoegen(d)
    d = klone(d, p)
    d = verteile_vermoegen(d)
    # Feineichung: Vermögen je Stufe genau auf den Eichpunkt
    for j, s in enumerate(STUFEN):
        m = (d["stufe"] == j) & (d["typ"] != "kind_erw")
        ziel = s[2] * s[3]
        ist = (d["w"][m] * d["W"][m]).sum()
        if abs(ist) > 0:
            f = ziel / ist
            for k in ["heim_netto", "immo", "geld", "betrieb", "W"]:
                d[k][m] *= f
            d["hauswert"][m] *= f
        # Haushaltszahl je Stufe genau
        d["w"][m] *= s[2] / d["w"][m].sum()
    # Löhne auf die VGR: Minijobs als Nebenjob, dann alle Löhne und Besoldungen gleichmäßig so, dass die Summe den Bruttolöhnen
    # der VGR 2025 entspricht (enthält Sonderzahlungen, Lohnstand 2025 und Löhne, die Umfragen untererfassen)
    besch = (d["std1"] > 0) | (d["std2"] > 0)
    anzahl = (d["w"] * ((d["std1"] > 0).astype(float) + (d["std2"] > 0))).sum()
    p_nj = ECKWERTE["nebenjob_mio"] * 1e6 / anzahl
    nj = besch & (rng.random(len(d["w"])) < p_nj * (((d["std1"] > 0).astype(float) + (d["std2"] > 0)) / np.maximum(1, ((d["std1"] > 0).astype(float) + (d["std2"] > 0)))))
    d["mini"][nj] += 12 * 603 * rng.uniform(0.3, 1.0, nj.sum())
    aktivB = (d["beamter"] > 0) & (d["rentner"] == 0)
    blg_ist = (d["w"] * (d["lohn1"] + d["lohn2"] + d["mini"] + np.where(aktivB, d["pension"], 0))).sum() / 1e9
    blg_sv = (d["w"] * (d["lohn1"] + d["lohn2"] + np.where(aktivB, d["pension"], 0))).sum() / 1e9
    f_lohn = 1 + (ECKWERTE["bruttoloehne_mrd"] - blg_ist) / blg_sv
    for k in ["lohn1", "lohn2"]:
        d[k] *= f_lohn
    d["pension"] = np.where(aktivB, d["pension"] * f_lohn, d["pension"])
    print("Lohnfaktor auf VGR", round(f_lohn, 4), "Nebenjobs Mio", round(d["w"][nj].sum() / 1e6, 2))
    d = ertraege(d)
    # Mietwert genau auf 214,5 Mrd. €
    d["miet"] *= ECKWERTE["mietwert_mrd"] * 1e9 / (d["w"] * d["miet"]).sum()
    # Sparquote: Achsenabschnitt so, dass der Konsum (ohne Mietwert) 2.300,2 Mrd. € ergibt; das verfügbare Einkommen rechnet der
    # Rechenkern (heute) — hier eine Näherung, die simulation.js mit dem Kern nachschärft (Schalter eichen)
    d["spar0"] = np.zeros(len(d["w"]))
    out = {"stand": "2026-11-14", "eckwerte": ECKWERTE, "stufen": [list(s) for s in STUFEN], "n": int(len(d["w"])), "spalten": {}}
    weg = {"p", "spar0", "stufe", "heim_netto", "pg", "bjob", "vorsorge"}
    for k, v in d.items():
        if k in weg:
            continue
        if v.dtype.kind in "fi":
            nk = 2 if k in ("hb",) else (1 if k == "w" else 0)
            out["spalten"][k] = [round(float(x), nk) if nk else int(round(float(x))) for x in v]
        else:
            out["spalten"][k] = [str(x) for x in v]
    json.dump(out, open(os.path.join(HIER, "bevoelkerung.json"), "w"), separators=(",", ":"))
    w = d["w"]
    print("Einheiten", len(w), "Haushalte Mio", round(w[d["typ"] != "kind_erw"].sum() / 1e6, 2), "Erwachsene Mio", round((w * d["erw"]).sum() / 1e6, 1),
          "Kinder Mio", round((w * d["kinder"]).sum() / 1e6, 1))
    print("Vermögen Bio", round((w * d["W"]).sum() / 1e12, 2), "Eigentümer", round(w[d["eigen"] > 0].sum() / w[d["typ"] != "kind_erw"].sum(), 3))
    hhm = d["typ"] != "kind_erw"
    o = np.argsort(d["W"][hhm]); cw = np.cumsum(w[hhm][o]) / w[hhm].sum()
    for q in [0.5, 0.9, 0.99]:
        print(f"  P{int(q*100)}", round(d["W"][hhm][o][np.searchsorted(cw, q)]))
    tot = (w[hhm] * d["W"][hhm]).sum()
    for q in [0.9, 0.99]:
        print(f"  Anteil oberste {round((1-q)*100)} %", round((w[hhm] * d["W"][hhm])[o][cw > q].sum() / tot, 3))
    for k in ["leist", "lohn1", "lohn2", "mini", "gewinn", "pension", "rente", "kap", "vermietCash", "aus", "gmbh", "transfer", "verm", "miet"]:
        print(f"  {k:12} {(w * d[k]).sum() / 1e9:8.1f} Mrd. €")


if __name__ == "__main__":
    main()
