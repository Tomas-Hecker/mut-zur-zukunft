#!/usr/bin/env python3
"""Baut die Rechner-Seite der HeCoAir GmbH (hecoair.org) aus den Rechnern dieses Repos.

Die Rechner bleiben hier die einzige Quelle. Das Skript kopiert sie in einen eigenen Ordner,
tauscht Kopfzeile, Hinweis und Fußzeile gegen das HeCoAir-Erscheinungsbild (hecoair/ci/),
und verlinkt alles, was zum Buch gehört, auf die Buch-Homepage. Am Inhalt der Rechner ändert es nichts.

Aufruf:   python3 werkzeug/hecoair-seite.py [Zielordner]      (Standard: _hecoair-seite/, nicht im Repo)
Ergebnis: Zielordner per FTP/Plesk in das Hauptverzeichnis von hecoair.org hochladen.
"""
import re
import shutil
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent
ZIEL = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else WURZEL / "_hecoair-seite"

# Adresse der Buch-Homepage: Links auf Buch, Steuerrechner, Vorträge usw. gehen dorthin.
BUCH_URL = "https://tomas-hecker.github.io/mut-zur-zukunft/"

RECHNER = [  # Ordner, Name im Menü, Kurzbeschreibung für die Startseite
    ("energie-rechner", "Energie-Rechner", "PV, Speicher, Wärmepumpe und E-Auto: ein Jahr Stunde für Stunde mit dem Wetter deines Orts, Festpreis, dynamischer Tarif und § 14a."),
    ("heizungsrechner", "Heizung und Dämmung", "Wärmepumpe, Gas oder Öl über 20 Jahre: mit Förderung, CO₂-Preis, Dämmung und neuen Fenstern."),
    ("eauto-rechner", "E-Auto-Rechner", "Was ein Elektroauto über sein ganzes Leben im Vergleich zum Verbrenner kostet, privat oder als Dienstwagen."),
    ("balkon-rechner", "Balkon-Rechner", "Balkonkraftwerk und kleiner Speicher für Mieter: Eigenverbrauch, Ersparnis und Amortisation."),
]
# Seiten, die nur auf der Buch-Homepage existieren
NUR_BUCH = ("buch/", "steuerrechner/", "vortraege/", "gesundheitsrechner/", "steuerlast/", "ueber-mich.html")
KOPIEREN = ["cockpit.css", "profil.js", "satz.js", "info.js", "methode.js", "wetter"]  # fehlende werden übersprungen
ENTFERNEN = ["tools-buchlinks.js", "energie-link.js"]  # Buchlinks und Übergabe an den Steuerrechner


def kopf(aktiv: str) -> str:
    links = '<a href="../rechner.html">Alle Rechner</a>' + "".join(
        f'<a href="../{o}/"{" aria-current=\"page\"" if o == aktiv else ""}>{n}</a>' for o, n, _ in RECHNER)
    return ('<header class="hc-kopf sitenav flush"><div class="hc-in">'
            '<a class="hc-logo" href="../" aria-label="HeCoAir, zur Startseite">'
            '<img src="../ci/hecoair-logo-klein.png" width="182" height="34" alt="HeCoAir"></a>'
            '<span class="hc-claim">Heizen · Kühlen · Lüften</span>'
            f'<nav aria-label="Rechner">{links}</nav>'
            '</div></header>')


HINWEIS = ('<div class="sitehinweis" role="note"><p><b>Prototyp, noch nicht unabhängig geprüft.</b> '
           'Die Rechner der HeCoAir GmbH sind vereinfachte Modelle. Die Ergebnisse sind Größenordnungen, '
           'können Fehler enthalten und ersetzen keine Energie-, Steuer-, Rechts- oder Finanzberatung. '
           'Alle Angaben ohne Gewähr. <a href="../impressum.html#haftung">Haftungsausschluss</a></p>'
           '<p>Für die Planung Ihres Gebäudes: qualifizierte Energieberater vor Ort finden Sie in der '
           '<a href="https://www.energie-effizienz-experten.de/" rel="noopener">Energieeffizienz-Expertenliste</a>, '
           'eine unabhängige Erstberatung bei der <a href="https://verbraucherzentrale-energieberatung.de/" rel="noopener">Verbraucherzentrale</a>.</p></div>')

FUSS = ('<footer class="hc-fuss"><p><span class="hc-firma">HeCoAir GmbH · Heizen · Kühlen · Lüften</span><br>'
        'Neutral und ohne Provision. Der Rechner läuft im Browser, deine Angaben bleiben auf deinem Gerät.</p>'
        '<p><a href="../">Start</a> · <a href="../rechner.html">Alle Rechner</a> · <a href="../kontakt.html">Kontakt</a> · <a href="../impressum.html">Impressum</a> · '
        '<a href="../datenschutz.html">Datenschutz</a></p></footer>')


def buch_links(s: str) -> str:
    """../buch/… usw. (in HTML und in Skripten) auf die Buch-Homepage umbiegen."""
    for p in NUR_BUCH:
        s = s.replace("../" + p, BUCH_URL + p)
    return s


def neutral(s: str) -> str:
    """Reform-Vergleiche und Buch-Vorschläge entfernen; was dynamisch entsteht, räumt ci/neutral.js auf."""
    # Energie-Rechner: Tarifspalte „8 h ohne Netzentgelt“ (Vorschlag) gar nicht erst rechnen
    s = re.sub(r'\n\s*\{ k: "h8",[^\n]*vorschlag: true \},', "", s)
    # Listenpunkte, die einen Vorschlag aus dem Buch beschreiben
    s = re.sub(r'\s*<li>(?:<b>)?Vorschlag aus dem Buch.*?</li>', "", s, flags=re.S)
    s = s.replace(", und der Vorschlag aus dem Buch, 8 Stunden am Tag ohne Netzentgelt, der heute noch nicht gilt", "")
    return s.replace("</body>", '<script src="../ci/neutral.js"></script>\n</body>', 1)


def rechner_umbauen(ordner: str) -> None:
    s = (WURZEL / ordner / "index.html").read_text(encoding="utf-8")
    n0 = len(s)
    s = s.replace('<link rel="icon" href="../favicon.svg" type="image/svg+xml">',
                  '<link rel="icon" href="../ci/favicon.png" type="image/png">')
    s = s.replace('<link rel="stylesheet" href="../schriften/schriften.css">\n', "")
    s = re.sub(r'<style id="sitenav-css">.*?</style>\n?', "", s, flags=re.S)
    s = s.replace("</head>", '<link rel="stylesheet" href="../ci/hecoair.css">\n</head>', 1)
    s, n = re.subn(r'<nav class="sitenav[^"]*".*?</nav>', kopf(ordner), s, count=1, flags=re.S)
    assert n == 1, f"{ordner}: Menü nicht gefunden"
    s, n = re.subn(r'<div class="sitehinweis".*?</div>', HINWEIS, s, count=1, flags=re.S)
    assert n == 1, f"{ordner}: Hinweis nicht gefunden"
    s, n = re.subn(r'<footer\b.*?</footer>', FUSS, s, count=1, flags=re.S)
    assert n == 1, f"{ordner}: Fußzeile nicht gefunden"
    for js in ENTFERNEN:
        s = s.replace(f'<script src="../{js}"></script>\n', "")
    s = neutral(s)
    s = buch_links(s)
    ziel = ZIEL / ordner / "index.html"
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(s, encoding="utf-8")
    print(f"  {ordner}: {n0:,} → {len(s):,} Zeichen")


FIRMA_MENUE = [("start", "index.html", "Start"), ("lebenszyklus", "lebenszyklus.html", "Lebenszyklus"), ("entwicklung", "entwicklung.html", "Entwicklung"),
               ("schulung", "schulung.html", "Schulungen"), ("rechner", "rechner.html", "Rechner"),
               ("ueber-uns", "ueber-uns.html", "Über uns"), ("kontakt", "kontakt.html", "Kontakt")]


def seiten() -> None:
    """Firmenseiten aus hecoair/seiten/*.html: erste Zeile ist ein Kommentar mit titel | beschreibung | aktiv | robots."""
    karten = "".join(
        f'<a class="karte" href="{o}/"><h3>{n}</h3><p>{t}</p><span class="mehr">Rechner öffnen ›</span></a>' for o, n, t in RECHNER)
    fuss = FUSS.replace('href="../rechner.html"', 'href="rechner.html"').replace('href="../', 'href="')
    for datei in sorted((WURZEL / "hecoair" / "seiten").glob("*.html")):
        kopfzeile, inhalt = datei.read_text(encoding="utf-8").split("\n", 1)
        meta = dict(teil.split(":", 1) for teil in kopfzeile.strip()[4:-3].split(" | "))
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        menue = "".join(f'<a href="{h}"{" aria-current=\"page\"" if k == meta.get("aktiv") else ""}>{n}</a>' for k, h, n in FIRMA_MENUE)
        titel = meta["titel"] if datei.stem == "start" else f'{meta["titel"]} · HeCoAir GmbH'
        robots = f'<meta name="robots" content="{meta["robots"]}">\n' if meta.get("robots") else ""
        html = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data:; base-uri 'self'; form-action 'self'">
<title>{titel}</title>
<meta name="description" content="{meta["beschreibung"]}">
{robots}<link rel="icon" href="ci/favicon.png" type="image/png">
<link rel="stylesheet" href="ci/hecoair.css">
<link rel="stylesheet" href="ci/seite.css">
</head>
<body>
<header class="hc-kopf"><div class="hc-in"><a class="hc-logo" href="./" aria-label="HeCoAir, zur Startseite"><img src="ci/hecoair-logo-klein.png" width="182" height="34" alt="HeCoAir"></a><span class="hc-claim">Heizen · Kühlen · Lüften</span><nav aria-label="Hauptmenü">{menue}</nav></div></header>
<main>
{inhalt.replace("{{RECHNERKARTEN}}", karten)}</main>
{fuss}
</body>
</html>
"""
        ziel = "index.html" if datei.stem == "start" else datei.name
        (ZIEL / ziel).write_text(html, encoding="utf-8")
        print(f"  Seite {ziel}")


def main() -> None:
    if ZIEL.exists():
        shutil.rmtree(ZIEL)
    ZIEL.mkdir(parents=True)
    print(f"HeCoAir-Seite nach {ZIEL}")
    shutil.copytree(WURZEL / "hecoair" / "ci", ZIEL / "ci")
    (ZIEL / ".htaccess").write_text((WURZEL / "hecoair" / "htaccess").read_text(encoding="utf-8"), encoding="utf-8")
    for name in KOPIEREN:
        q = WURZEL / name
        if not q.exists():
            continue
        (shutil.copytree if q.is_dir() else shutil.copy2)(q, ZIEL / name)
    # Erklär-Knöpfe: „Mehr im Buch“ zeigt auf die Buch-Homepage statt auf einen Ordner buch/ neben dem Skript
    info = ZIEL / "info.js"
    t = info.read_text(encoding="utf-8")
    t = t.replace('new URL("buch/", document.currentScript.src).href', f'"{BUCH_URL}buch/"')
    t = t.replace('>Mehr im Buch${name ? ": " + name : ""} ›</a>', '>Quelle: „Wir können uns die Zukunft leisten“${name ? ", " + name : ""} ›</a>')
    assert "Quelle: „Wir" in t, "info.js: Link-Text nicht gefunden"
    info.write_text(t, encoding="utf-8")
    for ordner, _, _ in RECHNER:
        rechner_umbauen(ordner)
    seiten()
    # Prüfen: jeder relative Link und jede Datei muss im Zielordner existieren
    tot = []
    for html in ZIEL.rglob("*.html"):
        for ref in re.findall(r'(?:href|src)="([^"]*)"', html.read_text(encoding="utf-8")):
            ref = ref.split("#")[0].split("?")[0]
            if not ref or ":" in ref or ref.startswith("//") or "${" in ref:
                continue
            ziel = (html.parent / ref).resolve()
            if ref.endswith("/"):
                ziel = ziel / "index.html"
            if not ziel.exists():
                tot.append(f"{html.relative_to(ZIEL)}: {ref}")
    if tot:
        print("Achtung, Links ins Leere:", *sorted(set(tot)), sep="\n  ")


if __name__ == "__main__":
    main()
