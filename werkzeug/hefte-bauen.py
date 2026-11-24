#!/usr/bin/env python3
"""Baut aus den Satzdateien der beiden Gesundheits-Hefte die Online-Leseseiten.

  python3 werkzeug/hefte-bauen.py ratgeber   <ratgeber_voll.html>  <ordner mit bilder/>
  python3 werkzeug/hefte-bauen.py broschuere <broschuere.html>     <ordner mit img/>

Die Seiten bleiben im Druckbild (A4), werden aber nicht mehr abgeschnitten und
passen sich am Handy der Bildschirmbreite an. Das CSS der Hefte wird auf .heft
begrenzt, die Website-Styles laufen in einer eigenen Ebene (layer), damit sich
beides nicht stört. Fotos werden als WebP verkleinert.

Die Quellen liegen im Projektordner „Gesundheit“: gesundheit/quelle-ratgeber/
(python3 build2.py erzeugt ratgeber_voll.html) und gesundheit/quelle-broschuere/.
Bei jeder neuen PDF-Fassung auch die Leseseiten neu bauen.
"""
import os, re, sys, html, shutil
from bs4 import BeautifulSoup
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GR = os.path.join(ROOT, 'gesundheitsrechner')
HEFTE = os.path.join(GR, 'hefte')

DOCS = {
    'ratgeber': dict(
        dir='ratgeber', pdf='lebensmittel-ratgeber.pdf',
        title='Erkennen statt zählen',
        eyebrow='Lebensmittel-Ratgeber online lesen',
        lead='Welche Lebensmittel lange satt machen und welche den Bauch wachsen lassen: 150 Lebensmittel mit echten Fotos, Sättigungs-Ampel und Bauch-Index, dazu 21 Rezepte und eine Tauschliste.',
        desc='Lebensmittel-Ratgeber „Erkennen statt zählen“ von Tomas Hecker online lesen: 150 Lebensmittel mit Sättigungs-Ampel und Bauch-Index, Rezepte und Tauschliste.',
        foot='Erkennen statt zählen · Der Lebensmittel-Ratgeber'),
    'broschuere': dict(
        dir='broschuere', pdf='broschuere-kleine-schritte-grosse-wirkung.pdf',
        title='Kleine Schritte. Große Wirkung.',
        eyebrow='Broschüre online lesen',
        lead='Für Fettleber, Vorstufe Diabetes und Typ-2-Diabetes: Teller-Regel, Tauschideen, Bauch-Index, Bewegung, 4-Wochen-Plan, Rezepte und die Gesundheitskette.',
        desc='Broschüre „Kleine Schritte. Große Wirkung.“ von Tomas Hecker online lesen: Teller-Regel, Tauschideen, Bauch-Index, Bewegung und 4-Wochen-Plan.',
        foot='Kleine Schritte. Große Wirkung.'),
}
# Feste Sprungziele (unabhängig von Seitenzahlen): Seite, deren Titel so beginnt -> id
ANKER = {
    'ratgeber': [('Gesund und glücklich', 'gluecklich'), ('So funktioniert der Ratgeber', 'legende'), ('Das Tellerprinzip', 'teller'), ('Gemeinsam kochen', 'gemeinsam'),
                 ('Der Bauch-Index', 'bauch-index'), ('Was macht so satt wie 2 Bananen', 'bananen'),
                 ('Eine Woche nach dem Teller', 'rezepte'), ('Tauschliste', 'tauschliste'),
                 ('Woher die Angaben stammen', 'quellen'), ('Register', 'register'), ('Bildnachweis', 'bildnachweis')],
    'broschuere': [('Bevor es losgeht', 'wuensche'), ('Kleines Quiz', 'quiz'), ('Die gute Nachricht', 'gute-nachricht'),
                   ('Die Teller-Regel', 'teller-regel'), ('Clever tauschen', 'tauschen'),
                   ('Satt werden, ohne zu zählen', 'satt'), ('Der Bauch-Index', 'bauch-index'),
                   ('Der Index für den Alltag', 'einkaufszettel'), ('Bewegung', 'bewegung'),
                   ('Ihr Startplan', 'startplan'), ('Lebensfreude als Motor', 'gluecklich'),
                   ('Gemeinsam geht es leichter', 'gemeinsam'), ('Die Gesundheitskette', 'gesundheitskette'),
                   ('Ein Tag voller Genuss', 'rezepte'), ('Fortschritt sichtbar machen', 'fortschritt'),
                   ('Bauch und Langzeitzucker', 'tafel'), ('Zum Nachlesen', 'quellen'), ('Sie sind nicht allein', 'unterstuetzung')],
}

LOGO = '<svg class="logo" viewBox="0 0 360 100" role="img" aria-label="Mut zur Zukunft"><g transform="translate(4,4) scale(0.92)"><circle cx="50" cy="50" r="44" fill="none" stroke="#f2b33d" stroke-width="1.6"/><line x1="27.5" y1="51.0" x2="21.4" y2="47.5" stroke="#f2b33d" stroke-width="2.4" stroke-linecap="round"/><line x1="37.0" y1="41.5" x2="33.5" y2="35.4" stroke="#f2b33d" stroke-width="2.4" stroke-linecap="round"/><line x1="63.0" y1="41.5" x2="66.5" y2="35.4" stroke="#f2b33d" stroke-width="2.4" stroke-linecap="round"/><line x1="72.5" y1="51.0" x2="78.6" y2="47.5" stroke="#f2b33d" stroke-width="2.4" stroke-linecap="round"/><path d="M30,64 A20,20 0 0 1 70,64 Z" fill="#f2b33d"/><path d="M50,64 L50,33" stroke="#fbf8f1" stroke-width="3.2" stroke-linecap="round"/><path d="M50,47 C41,46 33,39 31,28 C41,29 48,36 50,47 Z" fill="#9fd8b0"/><path d="M50,40 C57,37 65,30 68,19 C58,20 51,28 50,40 Z" fill="#9fd8b0"/><line x1="17" y1="64" x2="83" y2="64" stroke="#fbf8f1" stroke-width="2.4" stroke-linecap="round"/><line x1="28" y1="71" x2="72" y2="71" stroke="#fbf8f1" stroke-width="1.6" stroke-linecap="round" opacity="0.6"/><line x1="38" y1="77" x2="62" y2="77" stroke="#fbf8f1" stroke-width="1.2" stroke-linecap="round" opacity="0.35"/></g><text x="110" y="50" font-family="system-ui, sans-serif" font-weight="800" font-size="25" letter-spacing="1" fill="#fbf8f1">MUT ZUR</text><text x="110" y="80" font-family="system-ui, sans-serif" font-weight="800" font-size="30" letter-spacing="1.5" fill="#f2b33d">ZUKUNFT</text></svg>'


def split_rules(css):
    """Zerlegt CSS in (prelude, body) auf oberster Ebene."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0: break
        pre = css[i:j].strip()
        depth, k = 1, j + 1
        while k < n and depth:
            if css[k] == '{': depth += 1
            elif css[k] == '}': depth -= 1
            k += 1
        out.append((pre, css[j + 1:k - 1]))
        i = k
    return out


def scope_sel(sel):
    parts = []
    for s in sel.split(','):
        s = s.strip()
        if not s: continue
        if s in ('html', 'body', ':root'): parts.append('.heft'); continue
        s = re.sub(r'^(html|body|:root)\b\s*', '.heft ', s)
        parts.append(s if s.startswith('.heft') else '.heft ' + s)
    return ','.join(dict.fromkeys(parts))


def scope_css(css):
    out = []
    for pre, body in split_rules(css):
        if pre.startswith('@font-face') or pre.startswith('@page') or pre.startswith('@import'):
            continue
        if pre.startswith('@media print'):
            continue
        if pre.startswith('@media') or pre.startswith('@supports'):
            out.append(pre + '{' + scope_css(body) + '}')
            continue
        if pre.startswith('@'):
            out.append(pre + '{' + body + '}'); continue
        out.append(scope_sel(pre) + '{' + body.strip() + '}')
    return '\n'.join(out)


def bild(src_path, dst_dir, maxw):
    """Kopiert ein Foto als WebP (verkleinert) und gibt den neuen Dateinamen zurück."""
    base = os.path.splitext(os.path.basename(src_path))[0]
    if src_path.endswith('.svg'):
        shutil.copy(src_path, os.path.join(dst_dir, base + '.svg')); return base + '.svg'
    name = base + '.webp'
    im = Image.open(src_path)
    im = im.convert('RGBA' if im.mode in ('RGBA', 'LA', 'P') and 'transparency' in im.info or im.mode == 'RGBA' else 'RGB')
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(os.path.join(dst_dir, name), 'WEBP', quality=78, method=6)
    return name


def main():
    key, src, imgroot = sys.argv[1], sys.argv[2], sys.argv[3]
    D = DOCS[key]
    out = os.path.join(GR, D['dir'])
    bdir = os.path.join(out, 'bilder')
    if os.path.isdir(bdir): shutil.rmtree(bdir)
    os.makedirs(bdir)
    raw = open(src, encoding='utf-8').read()
    soup = BeautifulSoup(raw, 'html.parser')

    css = ''.join(s.get_text() for s in soup.find_all('style'))
    scoped = scope_css(css)

    pages = soup.select('section.page')
    # Bilder: groß verwendete Fotos 1100 px, kleine Vorschaubilder 320 px
    gross = set()
    for el in soup.find_all(style=True):
        m = re.search(r"url\(['\"]?([^)'\"]+\.(?:jpe?g|png|webp))", el['style'])
        if m and not set(el.get('class') or []) & {'ph', 'st-img'}: gross.add(m.group(1))
    for el in soup.find_all('img'):
        if el.get('src', '').startswith(('bilder/', 'img/')) and 'st-img' not in (el.get('class') or []): gross.add(el['src'])
    done = {}
    def neu(ref):
        if ref not in done:
            p = os.path.join(imgroot, ref)
            done[ref] = 'bilder/' + bild(p, bdir, 1100 if ref in gross else 320)
        return done[ref]
    for el in soup.find_all(style=True):
        el['style'] = re.sub(r"url\((['\"]?)((?:bilder|img)/[^)'\"]+)\1\)", lambda m: f"url('{neu(m.group(2))}')", el['style'])
    for el in soup.find_all('img'):
        s = el.get('src', '')
        if s.startswith(('bilder/', 'img/')): el['src'] = neu(s)
        el['loading'] = 'lazy'; el['decoding'] = 'async'
    for el in soup.find_all('image'):
        for att in ('href', 'xlink:href'):
            s = el.get(att, '')
            if s.startswith(('bilder/', 'img/')): el[att] = neu(s)

    # Seiten-IDs p1 … pN, feste Anker, Inhaltsverzeichnis
    toc, anchors_used = [], {}
    for i, p in enumerate(pages, 1):
        p['id'] = f'p{i}'
        p['aria-label'] = f'Seite {i}'
        k = p.select_one('.kicker'); h = p.find(['h1', 'h2'])
        kt = k.get_text(' ', strip=True) if k else ''
        ht = h.get_text(' ', strip=True) if h else ''
        for start, aid in ANKER[key]:
            if aid in anchors_used: continue
            if kt.startswith(start) or ht.startswith(start) or (key == 'ratgeber' and start == 'Tauschliste' and kt.startswith('Tauschen statt')):
                a = soup.new_tag('span', attrs={'id': aid, 'class': 'heft-anker'})
                p.insert(0, a); anchors_used[aid] = i
        if key == 'broschuere':
            toc.append((i, 'Titel' if i == 1 else ('Rückseite: ' + kt if i == len(pages) else (kt or ht)), ''))
    if key == 'ratgeber':
        for a in soup.select('a.toc-row'):
            n = int(a['href'][2:]); name = a.find('span').get_text(' ', strip=True)
            toc.append((n, name, ''))
        toc.append((1, 'Titel', ''))
        for i, p in enumerate(pages, 1):
            k = p.select_one('.kicker'); kt = k.get_text(' ', strip=True) if k else ''
            if kt in ('Zum Start', 'So funktioniert der Ratgeber'): toc.append((i, kt, ''))
        # Wegweiser im Heft: statt aufs PDF auf die Online-Fassung der Broschüre und den Rechner zeigen
        basis = 'https://tomas-hecker.github.io/mut-zur-zukunft/gesundheitsrechner/'
        for a in soup.find_all('a', href=True):
            m = re.match(re.escape(basis) + r'broschuere-kleine-schritte-grosse-wirkung\.pdf#page=(\d+)$', a['href'])
            if m: a['href'] = f'../broschuere/#p{m.group(1)}'
            elif a['href'].startswith(basis) and '.pdf' not in a['href']: a['href'] = '../' + a['href'][len(basis):]
        toc = sorted(dict(((t[0], t[1]), t) for t in toc).values())
    if key == 'broschuere':
        # Zeilen „Mehr dazu: Ratgeber S. N“ führen online zur Lesefassung des Ratgebers
        for d in soup.select('div.mehr'):
            m = re.search(r'Ratgeber (?:ab )?S\. (\d+)', d.get_text())
            if not m: continue
            a = soup.new_tag('a', attrs={'href': f'../ratgeber/#p{m.group(1)}', 'style': 'color:inherit'})
            for c in list(d.contents): a.append(c.extract())
            d.append(a)
    # Externe Links in neuem Tab
    for a in soup.find_all('a', href=True):
        if a['href'].startswith('http'):
            a['target'] = '_blank'; a['rel'] = 'noopener'
    body = ''.join(str(p) for p in pages)

    side_items = ''.join(
        f'<li><a href="#p{n}"><span class="no">{n}</span><span>{html.escape(t)}</span></a></li>' for n, t, _ in toc)
    andere = 'broschuere' if key == 'ratgeber' else 'ratgeber'
    A = DOCS[andere]
    andere_txt = 'Broschüre „Kleine Schritte. Große Wirkung.“' if andere == 'broschuere' else 'Lebensmittel-Ratgeber „Erkennen statt zählen“'
    pdf = f'../{D["pdf"]}'
    pdf_mb = os.path.getsize(os.path.join(GR, D['pdf'])) / 1e6
    seiten = len(pages)

    page = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(D['title'])} · online lesen · Mut zur Zukunft</title>
<meta name="description" content="{html.escape(D['desc'])}">
<link rel="icon" href="../../favicon.svg" type="image/svg+xml">
<style>@import url("../../style.css") layer(site);@import url("../../buch/buch.css") layer(site);</style>
<link rel="stylesheet" href="../hefte/hefte.css">
<style>
{scoped}
</style>
</head>
<body class="buch heftseite">
<header class="top" id="top"><div class="wrap"><a href="../../" aria-label="Zur Startseite">{LOGO}</a><nav aria-label="Hauptmenü"><a href="../../">Start</a><a href="../../buch/">Das Buch</a><a href="../">Gesundheitsrechner</a><a href="../../steuerrechner/">Steuerrechner</a><a href="../../ueber-mich.html">Über mich</a></nav></div></header>
<div class="bbar"><button type="button" class="tocbtn" aria-expanded="false" aria-controls="seite">Inhalt</button><span class="bbar-t">{html.escape(D['title'])}</span></div>
<div class="blayout" id="seite"><aside class="bside"><button type="button" class="sideclose">Schließen</button><nav class="btoc" aria-label="Inhalt"><a class="btoc-home" href="#top">{html.escape(D['title'])}</a><ol>{side_items}</ol></nav>
<div class="heft-side"><a href="{pdf}" download>Als PDF herunterladen</a><a href="../{A['dir']}/">{andere_txt} online lesen</a><a href="../">Zum Gesundheitsrechner</a></div></aside>
<main class="bmain"><div class="bhero"><div class="bwrap"><div><p class="eyebrow">{html.escape(D['eyebrow'])}</p><h1>{html.escape(D['title'])}</h1><p class="blead">{html.escape(D['lead'])}</p><div class="btns"><a class="btn" href="#p1">Lesen</a><a class="btn ghost" href="{pdf}" download>PDF herunterladen ({seiten} Seiten, {pdf_mb:.1f} MB)</a><a class="btn ghost" href="../">Zum Gesundheitsrechner</a></div></div></div></div>
<p class="heft-hinweis">Die Seiten sehen aus wie im gedruckten Heft. Am Handy kannst du sie mit zwei Fingern größer ziehen. Über „Inhalt“ springst du zu jedem Kapitel.</p>
<div class="heft heft-{key}">
{body}
</div>
<nav class="pn" aria-label="Weiter"><a class="prev" href="../"><small>Zurück</small>Zum Gesundheitsrechner</a><a class="next" href="../{A['dir']}/"><small>Weiter lesen</small>{andere_txt}</a></nav>
</main></div>
<footer><div class="wrap"><span>© 2026 Tomas Hecker · Mut zur Zukunft · Alle Angaben ohne Gewähr</span><nav aria-label="Rechtliches"><a href="{pdf}" download>Als PDF</a><a href="../../impressum.html#haftung">Haftungsausschluss</a><a href="../../impressum.html">Impressum</a><a href="../../datenschutz.html">Datenschutz</a></nav></div></footer>
<script src="../../buch/buch.js" defer></script>
<script src="../hefte/hefte.js" defer></script>
</body>
</html>
'''
    page = page.replace('.nf.woff2', '.woff2')
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(page)
    print(key, seiten, 'Seiten,', len(done), 'Bilder, Anker:', anchors_used)


if __name__ == '__main__':
    main()
