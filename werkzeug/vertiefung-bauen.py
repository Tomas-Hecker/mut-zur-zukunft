#!/usr/bin/env python3
"""Baut die Vertiefungsseiten zum Buch (Texte, die im Buch gekürzt sind) unter vertiefung/.
Aufruf: python3 werkzeug/vertiefung-bauen.py <Ordner mit name.html und vertiefung.json>
Jede Quelldatei ist ein <section class="chapter"> mit einem h1 (mit id); Kopf, Navigation und Fußzeile kommen von hier.
Volle Links auf die Seite (https://tomas-hecker.github.io/mut-zur-zukunft/...) werden relativ, damit sie die Linkprüfung erreicht.
Ein zweiter Lauf schreibt dieselben Dateien."""
import html, json, os, re, sys
SRC = sys.argv[1]
OUT = 'vertiefung'
BASIS = 'https://tomas-hecker.github.io/mut-zur-zukunft/'
os.makedirs(OUT, exist_ok=True)
L = json.load(open(os.path.join(SRC, 'vertiefung.json'), encoding='utf-8'))
buch = open('buch/vorwort.html', encoding='utf-8').read()
logo = re.search(r'<a href="\.\./" aria-label="Zur Startseite">.*?</a>', buch, re.S).group(0)
nav = re.search(r'<nav aria-label="Hauptmenü">.*?</nav>', buch, re.S).group(0).replace(' aria-current="page"', '')
nav = nav.replace('href="./"', 'href="../buch/" aria-current="page"')
pdf = re.search(r'href="(Wir-koennen-uns-die-Zukunft-leisten\.pdf[^"]*)"', buch).group(1)
FUSS = ('<footer><div class="wrap"><span>© 2026 Tomas Hecker · Mut zur Zukunft · Alle Angaben ohne Gewähr</span><nav aria-label="Rechtliches">'
        f'<a href="../buch/{pdf}" download>Buch als PDF</a><a href="../impressum.html#haftung">Haftungsausschluss</a>'
        '<a href="../impressum.html">Impressum</a><a href="../datenschutz.html">Datenschutz</a></nav></div></footer>\n'
        '<script src="../satz.js" defer></script>\n</body>\n</html>\n')

def kopf(titel, beschr):
    return ('<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'<title>{html.escape(titel)} · Wir können uns die Zukunft leisten</title>\n'
            f'<meta name="description" content="{html.escape(beschr)}">\n'
            '<link rel="icon" href="../favicon.svg" type="image/svg+xml">\n<link rel="stylesheet" href="../style.css">\n'
            '<link rel="stylesheet" href="../buch/buch.css">\n</head>\n<body class="buch">\n'
            f'<header class="top" id="top"><div class="wrap">{logo}{nav}</div></header>\n')

# Buchanker, die sich mit einer neuen Satzdatei geändert haben
ANKER_NEU = {'#auch-fuer-hallen-schulen-und-kliniken': '#hallen-schulen-und-kliniken-heute-zu-teuer-mit-der-reform-ma'}

def relativ(s):
    for a, b in ANKER_NEU.items():
        s = s.replace('stelle.html' + a + '"', 'stelle.html' + b + '"')
    s = s.replace('href="' + BASIS + 'vertiefung/', 'href="')
    s = s.replace('href="' + BASIS, 'href="../')
    # Links auf die eigene Seite öffnen nicht in einem neuen Fenster
    s = re.sub(r'(<a [^>]*href="(?:\.\./|[a-z0-9-]+\.html)[^"]*")\s+target="_blank"(\s+rel="noopener")?', r'\1', s)
    return s

def tabellen(s):
    """Tabellen scrollbar wie im Online-Buch (div.twrap)."""
    s = re.sub(r'<table\b', '<div class="twrap"><table', s)
    return s.replace('</table>', '</table></div>')

def kap_text(k):
    return 'Vertiefung zu Kapitel ' + k if k and k[0].isdigit() else ('Vertiefung zu Anhang ' + k if k else 'Vertiefung')

for e in L:
    q = open(os.path.join(SRC, e['name'] + '.html'), encoding='utf-8').read()
    m = re.search(r'<section class="chapter">\s*<h1 id="([^"]+)">(.*?)</h1>(.*)</section>', q, re.S)
    assert m, e['name']
    hid, h1, body = m.groups()
    assert not re.search(r'[Vv]ersion \d', re.sub(r'<[^>]+>', ' ', body)), ('Versionsnummer im Text', e['name'])
    seite = (kopf(e['titel'], e['kurzbeschreibung'])
             + f'<main class="bmain vertiefung"><span id="{hid}"></span><div class="bhero"><div class="bwrap"><div><p class="eyebrow">{kap_text(e.get("kapitel", ""))}</p>'
             f'<h1>{h1}</h1><p class="blead">{html.escape(e["kurzbeschreibung"])}</p></div></div></div>'
             f'<article class="btext">{tabellen(relativ(body))}'
             '<p class="weiter"><a href="./">Alle Vertiefungen</a> · <a href="../buch/">Zum Buch</a></p></article></main>\n' + FUSS)
    open(os.path.join(OUT, e['name'] + '.html'), 'w', encoding='utf-8').write(seite)

liste = ''.join(f'<li><a href="{e["name"]}.html"><strong>{html.escape(e["titel"])}</strong></a><br>'
                f'<span>{html.escape(e["kurzbeschreibung"])} ({kap_text(e.get("kapitel", ""))})</span></li>' for e in L)
index = (kopf('Vertiefungen zum Buch', 'Was im Buch nur kurz steht, hier ausführlich: Wohnung, Strom, Straße, Energiewende, Geflüchtete, Chancen, Zukunftsfonds, Rechtsprüfung und mehr.')
         + '<main class="bmain vertiefung"><div class="bhero"><div class="bwrap"><div><p class="eyebrow">Zum Buch</p><h1>Vertiefungen</h1>'
         '<p class="blead">Das Buch erzählt, der Anhang rechnet. Was nur kurz im Buch steht, findest du hier ausführlich, mit allen Beispielen, Studien und Rechnungen.</p></div></div></div>'
         f'<article class="btext"><ul class="vliste">{liste}</ul><p class="weiter"><a href="../buch/">Zum Buch</a></p></article></main>\n' + FUSS)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(index)
print(len(L), 'Vertiefungen gebaut')
