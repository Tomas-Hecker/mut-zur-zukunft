#!/usr/bin/env python3
"""Leseseiten (Wunsch Tomas, 22.11.2026): Kurzheft, Flyer und Vortrag online lesen, ohne Download, mit Teilen-Knopf.
Jede Seite des PDFs wird ein Bild (lesen/bilder/<name>/NN.webp); der Text der Seite steht für Vorleseprogramme und die Suche dabei.
Aufruf aus dem Projektordner: python3 werkzeug/lesen-bauen.py. Nach jedem neuen PDF wieder laufen lassen (die Bilder werden neu gemacht).
Ein zweiter Lauf mit denselben PDFs schreibt dieselben Dateien."""
import hashlib, html, os, re, shutil, subprocess, tempfile
from PIL import Image

BUCH = 'Wir können uns die Zukunft leisten'
SEITEN = [
    dict(name='kurzheft', pdf='buch/Wir-koennen-uns-die-Zukunft-leisten-Kurzfassung.pdf', px=1200, art='Seite',
         titel='Kurzheft zum Buch', eyebrow='Kurzfassung zum Buch',
         lead='Das Wichtigste aus dem Buch „Wir können uns die Zukunft leisten“ auf {n} Seiten: was die Reform jedem bringt, wer mehr zahlt und wie der Staat schuldenfrei wird.',
         teilen='Das Kurzheft zum Buch „Wir können uns die Zukunft leisten“, kostenlos online lesen:', breit=760),
    dict(name='flyer', pdf='buch/Wir-koennen-uns-die-Zukunft-leisten-Flyer.pdf', px=1400, art='Seite',
         titel='Flyer zum Weitergeben', eyebrow='Flyer zum Buch',
         lead='Ein Blatt A4, beidseitig: die Idee des Buchs „Wir können uns die Zukunft leisten“ in fünf Minuten. Zum Lesen, Ausdrucken und Weitergeben.',
         teilen='Ein Blatt, fünf Minuten: der Flyer zum Buch „Wir können uns die Zukunft leisten“:', breit=760),
    dict(name='vortrag', pdf='vortraege/wir-koennen-uns-die-zukunft-leisten/Wir-koennen-uns-die-Zukunft-leisten-Vortrag.pdf', px=1600, art='Folie',
         titel='Vortrag zum Buch', eyebrow='Vortrag zum Buch',
         lead='Die {n} Folien des Vortrags zum Buch „Wir können uns die Zukunft leisten“: woher wir kommen, warum es ohne Reform nicht geht und was die Reform für den Staat und die Haushalte bis 2070 bedeutet.',
         teilen='Der Vortrag zum Buch „Wir können uns die Zukunft leisten“, alle Folien online:', breit=1040),
]
OUT = 'lesen'
os.makedirs(OUT, exist_ok=True)
buch = open('buch/vorwort.html', encoding='utf-8').read()
logo = re.search(r'<a href="\.\./" aria-label="Zur Startseite">.*?</a>', buch, re.S).group(0)
nav = re.search(r'<nav aria-label="Hauptmenü">.*?</nav>', buch, re.S).group(0).replace(' aria-current="page"', '')
nav = nav.replace('href="./"', 'href="../buch/" aria-current="page"')
FUSS = ('<footer><div class="wrap"><span>© 2026 Tomas Hecker · Mut zur Zukunft · Alle Angaben ohne Gewähr</span><nav aria-label="Rechtliches">'
        '<a href="../impressum.html#haftung">Haftungsausschluss</a><a href="../impressum.html">Impressum</a><a href="../datenschutz.html">Datenschutz</a></nav></div></footer>\n'
        '<script src="../satz.js" defer></script>\n<script src="../teilen.js" defer></script>\n</body>\n</html>\n')
CSS = ('<style>.lesen{padding:24px 0 40px}.lesen figure{margin:0 auto 22px;background:#fff;border:1px solid var(--line);border-radius:6px;overflow:hidden;'
       'box-shadow:0 2px 10px rgba(0,0,0,.08)}.lesen img{display:block;width:100%;height:auto}.lesen figcaption{font-size:.85rem;color:var(--muted);'
       'padding:6px 10px;border-top:1px solid var(--line);background:var(--bg)}.lesen .weg{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}'
       '.lesen .alle{display:flex;flex-wrap:wrap;gap:10px 18px;justify-content:center;margin:8px 0 0}'
       '.bhero.big .btns.lesebtns{grid-template-columns:repeat(3,minmax(0,1fr))}@media (max-width:560px){.bhero.big .btns.lesebtns{grid-template-columns:1fr}}</style>\n')

def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]

def seite_text(pdf, i):
    t = subprocess.run(['pdftotext', '-layout', '-f', str(i), '-l', str(i), pdf, '-'], capture_output=True, text=True).stdout
    t = t.replace('­', '').replace('‐\n', '')
    return re.sub(r'\s+', ' ', t).strip()

ANDERE = {'kurzheft': ('Kurzheft lesen', 'kurzheft.html'), 'flyer': ('Flyer lesen', 'flyer.html'), 'vortrag': ('Vortrag ansehen', 'vortrag.html')}
for S in SEITEN:
    pdf = S['pdf']; n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    w_pt = float(re.search(r'Page size:\s+([\d.]+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    bd = os.path.join(OUT, 'bilder', S['name'])
    if os.path.isdir(bd): shutil.rmtree(bd)
    os.makedirs(bd)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(['pdftoppm', '-r', str(round(S['px'] / w_pt * 72, 2)), '-png', pdf, os.path.join(tmp, 's')], check=True)
        pngs = sorted(f for f in os.listdir(tmp) if f.endswith('.png'))
        assert len(pngs) == n, (pdf, len(pngs), n)
        groesse = []
        for i, f in enumerate(pngs, 1):
            im = Image.open(os.path.join(tmp, f)).convert('RGB')
            if im.width != S['px']: im = im.resize((S['px'], round(im.height * S['px'] / im.width)), Image.LANCZOS)
            im.save(os.path.join(bd, f'{i:02d}.webp'), 'WEBP', quality=80, method=6)
            groesse.append(im.size)
    v = md5(pdf); pdf_rel = '../' + pdf + '?v=' + v
    mb = os.path.getsize(pdf) / 1e6
    figs = []
    for i in range(1, n + 1):
        w, h = groesse[i - 1]; t = seite_text(pdf, i)
        figs.append(f'<figure id="{S["art"].lower()}-{i}" style="max-width:{S["breit"]}px"><img src="bilder/{S["name"]}/{i:02d}.webp" width="{w}" height="{h}" '
                    f'alt="{S["art"]} {i} von {n}" loading="{"eager" if i <= 2 else "lazy"}" decoding="async">'
                    f'<div class="weg">{html.escape(t)}</div><figcaption>{S["art"]} {i} von {n}</figcaption></figure>')
    knoepfe = (f'<a class="btn" href="{pdf_rel}" download>Als PDF herunterladen</a>'
               f'<button type="button" class="btn ghost" data-teilen data-titel="{html.escape(S["titel"] + ": " + BUCH)}" data-text="{html.escape(S["teilen"])}" aria-haspopup="menu" aria-expanded="false">Teilen</button>'
               '<a class="btn ghost" href="../buch/">Das ganze Buch lesen</a>')
    weitere = ' · '.join(f'<a href="{u}">{t}</a>' for k, (t, u) in ANDERE.items() if k != S['name'])
    seite = ('<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n'
             '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
             f'<title>{html.escape(S["titel"])} · {BUCH}</title>\n<meta name="description" content="{html.escape(S["lead"].format(n=n))}">\n'
             '<link rel="icon" href="../favicon.svg" type="image/svg+xml">\n<link rel="stylesheet" href="../style.css">\n<link rel="stylesheet" href="../buch/buch.css">\n'
             + CSS + '</head>\n<body class="buch">\n'
             f'<header class="top" id="top"><div class="wrap">{logo}{nav}</div></header>\n'
             f'<main><div class="bhero big"><div class="bwrap"><div><p class="eyebrow">{S["eyebrow"]}</p><h1>{BUCH}</h1>'
             f'<p class="blead">{html.escape(S["lead"].format(n=n))} {"Als PDF" if True else ""} {n} {S["art"] + "n" if n != 1 else S["art"]}, {mb:.1f} MB.'.replace('.', ',', 0)
             + f'</p><div class="btns lesebtns">{knoepfe}</div></div></div></div>\n'
             f'<div class="wrap lesen">{"".join(figs)}<p class="alle">{weitere} · <a href="../buch/">Das Buch online lesen</a></p></div></main>\n' + FUSS)
    seite = seite.replace(f'{mb:.1f} MB', f'{mb:.1f} MB'.replace('.', ','))
    open(os.path.join(OUT, S['name'] + '.html'), 'w', encoding='utf-8').write(seite)
    print(S['name'], n, 'Seiten', sum(os.path.getsize(os.path.join(bd, f)) for f in os.listdir(bd)) // 1000, 'kB Bilder')
