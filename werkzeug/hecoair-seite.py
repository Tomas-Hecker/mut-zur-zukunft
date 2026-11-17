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
KOPIEREN = ["cockpit.css", "profil.js", "satz.js", "info.js", "wetter"]
ENTFERNEN = ["tools-buchlinks.js", "energie-link.js"]  # Buchlinks und Übergabe an den Steuerrechner


def kopf(aktiv: str) -> str:
    links = "".join(
        f'<a href="../{o}/"{" aria-current=\"page\"" if o == aktiv else ""}>{n}</a>' for o, n, _ in RECHNER)
    return ('<header class="hc-kopf sitenav flush"><div class="hc-in">'
            '<a class="hc-logo" href="../" aria-label="HeCoAir, zur Startseite">'
            '<img src="../ci/hecoair-logo-klein.png" width="182" height="34" alt="HeCoAir"></a>'
            '<span class="hc-claim">Heizen · Kühlen · Lüften</span>'
            f'<nav aria-label="Rechner">{links}</nav>'
            '<button type="button" class="hc-druck" onclick="print()" title="Eingaben und Ergebnisse drucken oder als PDF speichern">Drucken / PDF</button>'
            '</div></header>')


HINWEIS = ('<div class="sitehinweis" role="note"><p><b>Prototyp, noch nicht unabhängig geprüft.</b> '
           'Die Rechner der HeCoAir GmbH sind vereinfachte Modelle. Die Ergebnisse sind Größenordnungen, '
           'können Fehler enthalten und ersetzen keine Energie-, Steuer-, Rechts- oder Finanzberatung. '
           'Alle Angaben ohne Gewähr. <a href="../impressum.html#haftung">Haftungsausschluss</a></p></div>')

FUSS = ('<footer class="hc-fuss"><p><span class="hc-firma">HeCoAir GmbH · Heizen · Kühlen · Lüften</span><br>'
        'Neutral und ohne Provision. Der Rechner läuft im Browser, deine Angaben bleiben auf deinem Gerät.</p>'
        '<p><a href="../">Alle Rechner</a> · <a href="../impressum.html">Impressum</a> · '
        '<a href="../datenschutz.html">Datenschutz</a></p></footer>')


def buch_links(s: str) -> str:
    """../buch/… usw. (in HTML und in Skripten) auf die Buch-Homepage umbiegen."""
    for p in NUR_BUCH:
        s = s.replace("../" + p, BUCH_URL + p)
    return s


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
    s = buch_links(s)
    ziel = ZIEL / ordner / "index.html"
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(s, encoding="utf-8")
    print(f"  {ordner}: {n0:,} → {len(s):,} Zeichen")


def startseite() -> None:
    karten = "".join(
        f'<a class="hc-karte" href="{o}/"><h2>{n}</h2><p>{t}</p><span>Rechner öffnen ›</span></a>' for o, n, t in RECHNER)
    menue = "".join(f'<a href="{o}/">{n}</a>' for o, n, _ in RECHNER)
    html = f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Energie-Rechner · HeCoAir GmbH</title>
<meta name="description" content="Neutrale Energie-Rechner der HeCoAir GmbH: Photovoltaik, Speicher, Wärmepumpe, Dämmung, E-Auto und Balkonkraftwerk. Kostenlos, ohne Provision, die Angaben bleiben auf deinem Gerät.">
<link rel="icon" href="ci/favicon.png" type="image/png">
<link rel="stylesheet" href="ci/hecoair.css">
<style>
* {{ box-sizing: border-box }}
body {{ margin: 0; background: var(--bg); color: var(--fg); font: 17px/1.55 var(--body); padding: 28px max(16px, env(safe-area-inset-left, 0px)) 56px }}
.wrap {{ max-width: 1180px; margin: 0 auto }}
.eyebrow {{ font-size: 12.5px; text-transform: uppercase }}
.held {{ padding: 36px 0 28px; border-bottom: 1px solid var(--line); margin-bottom: 28px }}
.held h1 {{ font-size: clamp(32px, 5vw, 52px); line-height: 1.08; margin: 10px 0 14px; max-width: 18ch }}
.held p {{ max-width: 62ch; color: var(--muted); font-size: 19px; font-weight: 300; margin: 0 }}
.hc-karten {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px }}
.hc-karte {{ display: grid; gap: 8px; align-content: start; background: var(--panel); border: 1px solid var(--line); border-top: 4px solid var(--hc-oliv); border-radius: 6px; padding: 18px; text-decoration: none; color: var(--fg) }}
.hc-karte:hover {{ border-top-color: var(--hc-orange) }}
.hc-karte h2 {{ font-size: 22px; margin: 0; color: var(--fg) }}
.hc-karte p {{ margin: 0; color: var(--muted); font-size: 15.5px }}
.hc-karte span {{ color: var(--hc-oliv); font-weight: 600; font-size: 15px }}
.leitsatz {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-top: 32px }}
.leitsatz div {{ border-left: 3px solid var(--hc-orange); padding: 2px 0 2px 14px }}
.leitsatz b {{ display: block; font-family: var(--display); font-weight: 600; font-size: 17px }}
.leitsatz p {{ margin: 4px 0 0; color: var(--muted); font-size: 15px }}
</style>
</head>
<body>
<header class="hc-kopf"><div class="hc-in"><a class="hc-logo" href="./" aria-label="HeCoAir, zur Startseite"><img src="ci/hecoair-logo-klein.png" width="182" height="34" alt="HeCoAir"></a><span class="hc-claim">Heizen · Kühlen · Lüften</span><nav aria-label="Rechner">{menue}</nav></div></header>
<main class="wrap">
<section class="held">
<p class="eyebrow">HeCoAir GmbH · Energie-Rechner</p>
<h1>Selbst nachrechnen, bevor man kauft</h1>
<p>Lohnt sich die Wärmepumpe, wie groß soll die Solaranlage sein, braucht es einen Speicher? Unsere Rechner zeigen es mit dem Wetter deines Orts, neutral und ohne Provision.</p>
</section>
<div class="hc-karten">{karten}</div>
<div class="leitsatz">
<div><b>Neutral</b><p>Wir verkaufen keine Geräte und bekommen keine Provision.</p></div>
<div><b>Nachvollziehbar</b><p>Jede Annahme steht mit Quelle beim Rechner und lässt sich ändern.</p></div>
<div><b>Privat</b><p>Alles läuft im Browser. Deine Angaben verlassen dein Gerät nicht.</p></div>
</div>
</main>
{FUSS.replace('href="../', 'href="').replace('<a href="">Alle Rechner</a> · ', '')}
</body>
</html>
"""
    (ZIEL / "index.html").write_text(html, encoding="utf-8")
    print("  Startseite")


def main() -> None:
    if ZIEL.exists():
        shutil.rmtree(ZIEL)
    ZIEL.mkdir(parents=True)
    print(f"HeCoAir-Seite nach {ZIEL}")
    shutil.copytree(WURZEL / "hecoair" / "ci", ZIEL / "ci")
    for name in KOPIEREN:
        q = WURZEL / name
        (shutil.copytree if q.is_dir() else shutil.copy2)(q, ZIEL / name)
    # Erklär-Knöpfe: „Mehr im Buch“ zeigt auf die Buch-Homepage statt auf einen Ordner buch/ neben dem Skript
    info = ZIEL / "info.js"
    t = info.read_text(encoding="utf-8")
    t = t.replace('new URL("buch/", document.currentScript.src).href', f'"{BUCH_URL}buch/"')
    info.write_text(t, encoding="utf-8")
    for p in ("impressum.html", "datenschutz.html"):
        shutil.copy2(WURZEL / "hecoair" / p, ZIEL / p)
    for ordner, _, _ in RECHNER:
        rechner_umbauen(ordner)
    startseite()
    rest = [f"{d.name}: {m}" for d in ZIEL.iterdir() if d.is_dir() and d.name in {o for o, _, _ in RECHNER}
            for m in re.findall(r'(?:href|src)="\.\./(?!"|ci/|wetter/|impressum|datenschutz|profil|satz|info|cockpit|(?:%s)/)[^"]*"' % "|".join(o for o, _, _ in RECHNER),
                                (d / "index.html").read_text(encoding="utf-8"))]
    if rest:
        print("Achtung, Links ins Leere:", *rest, sep="\n  ")


if __name__ == "__main__":
    main()
