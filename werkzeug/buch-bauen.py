#!/usr/bin/env python3
"""Baut aus der Satzdatei des Buchs (quelltext/Mut-zur-Zukunft.html) das Online-Buch.
Aufruf: python3 buildbuch.py <quelle.html> <zielordner buch/>
"""
import re, sys, json, os, html
from bs4 import BeautifulSoup, NavigableString

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
soup = BeautifulSoup(open(SRC, encoding='utf-8').read(), 'html.parser')
secs = soup.body.find_all('section', recursive=False)

LOGO = '<g transform="translate(4,4) scale(0.92)"><circle cx="50" cy="50" r="44" fill="none" stroke="#f2b33d" stroke-width="1.6"/><line x1="27.5" y1="51.0" x2="21.4" y2="47.5" stroke="#f2b33d" stroke-width="2.4" stroke-linecap="round"/><line x1="37.0" y1="41.5" x2="33.5" y2="35.4" stroke="#f2b33d" stroke-width="2.4" stroke-linecap="round"/><line x1="63.0" y1="41.5" x2="66.5" y2="35.4" stroke="#f2b33d" stroke-width="2.4" stroke-linecap="round"/><line x1="72.5" y1="51.0" x2="78.6" y2="47.5" stroke="#f2b33d" stroke-width="2.4" stroke-linecap="round"/><path d="M30,64 A20,20 0 0 1 70,64 Z" fill="#f2b33d"/><path d="M50,64 L50,33" stroke="#fbf8f1" stroke-width="3.2" stroke-linecap="round"/><path d="M50,47 C41,46 33,39 31,28 C41,29 48,36 50,47 Z" fill="#9fd8b0"/><path d="M50,40 C57,37 65,30 68,19 C58,20 51,28 50,40 Z" fill="#9fd8b0"/><line x1="17" y1="64" x2="83" y2="64" stroke="#fbf8f1" stroke-width="2.4" stroke-linecap="round"/><line x1="28" y1="71" x2="72" y2="71" stroke="#fbf8f1" stroke-width="1.6" stroke-linecap="round" opacity="0.6"/><line x1="38" y1="77" x2="62" y2="77" stroke="#fbf8f1" stroke-width="1.2" stroke-linecap="round" opacity="0.35"/></g>'
WORT = '<svg class="logo" viewBox="0 0 360 100" role="img" aria-label="Schuldenfrei 2070">' + LOGO + '<text x="110" y="50" font-family="system-ui, sans-serif" font-weight="800" font-size="25" letter-spacing="1" fill="#fbf8f1">SCHULDENFREI</text><text x="110" y="80" font-family="system-ui, sans-serif" font-weight="800" font-size="30" letter-spacing="1.5" fill="#f2b33d">2070</text></svg>'

# ---------- Kapitel einsammeln ----------
chapters = []  # dict(slug, no, kicker, title, lead, nodes)
i = 0
while i < len(secs):
    s = secs[i]
    cls = s.get('class') or []
    if 'opener' in cls:
        kicker = s.find(class_='kicker').get_text(strip=True)
        no = s.find(class_='num').get_text(strip=True)
        title = s.find('h1').get_text(' ', strip=True)
        lead = s.find(class_='lead')
        body = secs[i + 1]
        slug = ('kapitel-' + no) if no.isdigit() else ('anhang-' + no.lower())
        chapters.append(dict(slug=slug, no=no, kicker=kicker, title=title,
                             lead=lead.decode_contents() if lead else '', body=body))
        i += 2; continue
    if 'chapter' in cls:
        h1 = s.find('h1')
        title = h1.get_text(' ', strip=True)
        if s.find(class_='kicker') and s.find(class_='kicker').get_text(strip=True) == 'Vorwort':
            for t in s.find_all(class_='toc'): t.decompose()
            lead = s.find(class_='lead'); leadh = lead.decode_contents(); lead.decompose()
            s.find(class_='kicker').decompose(); h1.decompose()
            chapters.append(dict(slug='vorwort', no='', kicker='Vorwort', title=title, lead=leadh, body=s))
        elif title.startswith('Quellen'):
            h1.decompose()
            chapters.append(dict(slug='quellen', no='', kicker='Anhang', title=title, lead='', body=s))
    i += 1

def slugify(t):
    t = t.lower()
    for a, b in (('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'), ('ß', 'ss'), ('₂', '2')):
        t = t.replace(a, b)
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')
    return t[:60].rstrip('-') or 'abschnitt'

# Abschnitts-IDs vergeben
appendix_ids = {}  # 'B7' -> 'anhang-b.html#b7'
for ch in chapters:
    body = ch['body']
    for r in body.find_all(class_='runner'): r.decompose()
    used = set(); ch['heads'] = []
    for h in body.find_all(['h2', 'h3']):
        anr = h.find(class_='anr')
        hid = anr.get_text(strip=True).lower() if anr else slugify(h.get_text(' ', strip=True))
        base, k = hid, 2
        while hid in used: hid = f'{base}-{k}'; k += 1
        used.add(hid); h['id'] = hid
        if anr: appendix_ids[anr.get_text(strip=True)] = f"{ch['slug']}.html#{hid}"
        if h.name == 'h2':
            ch['heads'].append((hid, h.get_text(' ', strip=True), anr.get_text(strip=True) if anr else ''))

slugs = {c['slug'] for c in chapters}

# ---------- Querverweise klickbar machen ----------
NB = r'[  ]+'
pat = re.compile(r'(Kapitel' + NB + r'([1-9])(?![0-9]))|(Anhang' + NB + r'([ABC])([1-9])?(?![0-9]))|((?<![\w\-/.])([ABC][1-9])(?![\w\-]))')
def linkify(ch):
    for tn in list(ch['body'].find_all(string=True)):
        if not isinstance(tn, NavigableString) or tn.parent is None: continue
        if tn.find_parent(['a', 'h1', 'h2', 'h3', 'svg', 'script', 'style']) is not None: continue
        if tn.parent.get('class') and 'anr' in tn.parent.get('class'): continue
        txt = str(tn)
        if not pat.search(txt): continue
        out, last = [], 0
        for m in pat.finditer(txt):
            href = None
            if m.group(1):
                href = f'kapitel-{m.group(2)}.html'
            elif m.group(3):
                L, n = m.group(4), m.group(5)
                href = appendix_ids.get(L + n) if n else f'anhang-{L.lower()}.html'
            elif m.group(6):
                href = appendix_ids.get(m.group(7))
            if not href: continue
            if href.split('#')[0] == ch['slug'] + '.html':
                href = '#' + href.split('#')[1] if '#' in href else '#top'
            out.append(html.escape(txt[last:m.start()], quote=False))
            out.append(f'<a class="xref" href="{href}">{html.escape(m.group(0), quote=False)}</a>')
            last = m.end()
        if not out: continue
        out.append(html.escape(txt[last:], quote=False))
        tn.replace_with(BeautifulSoup(''.join(out), 'html.parser'))
    # Interne Verweise aus der Satzdatei (#anh-B5, #anh-C, #kap-7) auf die Seiten des Online-Buchs umlenken
    for a in ch['body'].find_all('a', href=re.compile(r'^#(anh|kap)-')):
        ref = a['href'][1:]
        m = re.match(r'anh-([ABC])([1-9])?$', ref)
        if m: href = appendix_ids.get(m.group(1) + m.group(2)) if m.group(2) else f'anhang-{m.group(1).lower()}.html'
        else:
            m = re.match(r'kap-([1-9])$', ref); href = f'kapitel-{m.group(1)}.html' if m else None
        if not href: continue
        if href.split('#')[0] == ch['slug'] + '.html': href = '#' + href.split('#')[1] if '#' in href else '#top'
        a['href'] = href; a['class'] = [c for c in (a.get('class') or []) if c != 'ref'] + ['xref']
    # URLs in Quellen
    for tn in list(ch['body'].find_all(string=re.compile(r'https?://'))):
        if tn.find_parent('a') is not None: continue
        t = str(tn)
        new = re.sub(r'(https?://[^\s<)\]]+[^\s<)\].,;:])', lambda m: f'<a href="{m.group(1)}" rel="noopener">{m.group(1)}</a>', html.escape(t, quote=False))
        tn.replace_with(BeautifulSoup(new, 'html.parser'))
    # Externe Links (Quellen): neuer Tab, als extern erkennbar
    for a in ch['body'].find_all('a', href=re.compile(r'^https?://')):
        a['target'] = '_blank'; a['rel'] = 'noopener'
        a['class'] = (a.get('class') or []) + ['ext']

for ch in chapters: linkify(ch)
# dieselben Verweise im Vorspann eines Kapitels
def _lead_ref(m):
    ref = m.group(1); mm = re.match(r'anh-([ABC])([1-9])?$', ref)
    if mm: return 'class="xref" href="' + ((appendix_ids.get(mm.group(1) + mm.group(2)) or 'anhang-' + mm.group(1).lower() + '.html') if mm.group(2) else 'anhang-' + mm.group(1).lower() + '.html') + '"'
    return 'class="xref" href="kapitel-' + ref[4:] + '.html"'
for ch in chapters: ch['lead'] = re.sub(r'class="ref" href="#((?:anh-[ABC][1-9]?)|(?:kap-[1-9]))"', _lead_ref, ch['lead'])

# ---------- Rechner-Verweise ----------
R = '../steuerrechner/'
def rbox(title, text, links):
    btn = ''.join(f'<a class="rbtn" href="{R}#{a}">{t}</a>' for a, t in links)
    return BeautifulSoup(f'<aside class="rechner"><div><strong>{title}</strong><p>{text}</p></div><div class="rbtns">{btn}</div></aside>', 'html.parser')
for ch in chapters:
    b = ch['body']
    for h in b.find_all('h2'):
        t = h.get_text(' ', strip=True)
        if 'CO₂' in t or 'CO2' in t:
            h.insert_after(rbox('Selbst ausprobieren', 'Im Rechner kannst du CO₂-Preis, Rückgabe als Klimageld und Haushaltsgröße selbst einstellen.', [('co2', 'CO₂-Abgabe rechnen')]))
            break
END = {
 'kapitel-5': ('Was heißt das für dich?', 'Gib dein Einkommen und deinen Haushalt ein und vergleiche heute mit dem Vorschlag.', [('haushalt', 'Meinen Haushalt rechnen')]),
 'kapitel-7': ('Selbst nachrechnen', 'Alle Ergebnisse dieses Kapitels lassen sich im Rechner nachvollziehen und mit eigenen Annahmen verändern.', [('haushalt', 'Haushalt'), ('staat', 'Staatsfinanzen bis 2070')]),
 'anhang-a': ('Selbst nachrechnen', 'Die Fälle aus diesem Anhang sind im Rechner als Beispiele hinterlegt.', [('haushalt', 'Beispielhaushalte öffnen')]),
 'anhang-b': ('Selbst nachrechnen', 'Die Bausteine lassen sich im Rechner einzeln ein- und ausschalten.', [('staat', 'Bausteine und Staatsfinanzen'), ('co2', 'CO₂-Abgabe')]),
 'anhang-c': ('Selbst nachrechnen', 'Die Simulation bis 2070 mit den drei Szenarien steckt auch im Rechner.', [('staat', 'Staatsschulden bis 2070')]),
}
for ch in chapters:
    if ch['slug'] in END: ch['body'].append(rbox(*END[ch['slug']]))

# Tabellen scrollbar
for ch in chapters:
    for t in ch['body'].find_all('table'):
        w = soup.new_tag('div', attrs={'class': 'twrap'}); t.wrap(w)

def ser(node):
    s = node.decode_contents()
    return s.replace('viewbox=', 'viewBox=').replace('preserveaspectratio=', 'preserveAspectRatio=')

# ---------- Seiten ----------
def toc_html(cur):
    out = ['<nav class="btoc" aria-label="Inhalt des Buchs"><a class="btoc-home" href="./">Inhaltsverzeichnis</a><ol>']
    for c in chapters:
        lab = f'<span class="no">{c["no"]}</span>' if c['no'] else '<span class="no"></span>'
        here = c['slug'] == cur
        out.append(f'<li{" class=\"cur\"" if here else ""}><a href="{c["slug"]}.html"{" aria-current=\"page\"" if here else ""}>{lab}<span>{html.escape(c["title"])}</span></a>')
        if here and c['heads']:
            out.append('<ol class="sub">' + ''.join(f'<li><a href="#{i}">{html.escape(t)}</a></li>' for i, t, _ in c['heads']) + '</ol>')
        out.append('</li>')
    out.append('</ol></nav>')
    return ''.join(out)

def page(title, desc, body, cur='', extra_head=''):
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../style.css">
<link rel="stylesheet" href="buch.css">
{extra_head}</head>
<body class="buch">
<header class="top" id="top"><div class="wrap"><a href="../" aria-label="Zur Startseite">{WORT}</a><nav aria-label="Hauptmenü"><a href="../">Start</a><a href="./" aria-current="page">Das Buch</a><a href="../steuerrechner/">Steuerrechner</a><a href="../eauto-rechner/">E-Auto-Rechner</a><a href="../heizungsrechner/">Heizungsrechner</a><a href="../energie-rechner/">Energie-Rechner</a><a href="../balkon-rechner/">Balkon-Rechner</a><a href="../ueber-mich.html">Über mich</a></nav></div></header>
{body}
<footer><div class="wrap"><span>© 2026 Tomas Hecker · Schuldenfrei 2070 · Alle Angaben ohne Gewähr</span><nav aria-label="Rechtliches"><a href="Schuldenfrei-2070.pdf" download>Buch als PDF</a><a href="../impressum.html#haftung">Haftungsausschluss</a><a href="../impressum.html">Impressum</a><a href="../datenschutz.html">Datenschutz</a></nav></div></footer>
<script src="buch.js" defer></script>
<script src="../satz.js" defer></script>
</body>
</html>
'''

SEARCHBOX = '<form class="suche" role="search" action="suche.html"><label class="sr" for="q">Im Buch suchen</label><input id="q" name="q" type="search" placeholder="Im Buch suchen …" autocomplete="off"></form>'

index_entries = []
for k, ch in enumerate(chapters):
    prev = chapters[k - 1] if k else None
    nxt = chapters[k + 1] if k + 1 < len(chapters) else None
    hero = f'''<div class="bhero"><div class="bwrap"><div class="bnum">{ch["no"]}</div><div><p class="eyebrow">{html.escape(ch["kicker"])}</p><h1>{html.escape(ch["title"])}</h1>{f'<p class="blead">{ch["lead"]}</p>' if ch["lead"] else ''}</div></div></div>'''
    pn = '<nav class="pn" aria-label="Blättern">'
    pn += f'<a class="prev" href="{prev["slug"]}.html"><small>Zurück</small>{html.escape(prev["title"])}</a>' if prev else '<a class="prev" href="./"><small>Zurück</small>Inhaltsverzeichnis</a>'
    pn += f'<a class="next" href="{nxt["slug"]}.html"><small>Weiter</small>{html.escape(nxt["title"])}</a>' if nxt else '<a class="next" href="../steuerrechner/"><small>Weiter</small>Zum Steuerrechner</a>'
    pn += '</nav>'
    body = f'''<div class="bbar"><button type="button" class="tocbtn" aria-expanded="false" aria-controls="seite">Inhalt</button><span class="bbar-t">{html.escape((ch["kicker"] + " · ") if ch["no"] else "")}{html.escape(ch["title"])}</span></div>
<div class="blayout" id="seite"><aside class="bside"><button type="button" class="sideclose">Schließen</button>{SEARCHBOX}{toc_html(ch["slug"])}</aside>
<main class="bmain">{hero}<article class="btext">{ser(ch["body"])}</article>{pn}</main></div>'''
    open(os.path.join(OUT, ch['slug'] + '.html'), 'w', encoding='utf-8').write(
        page(f'{ch["title"]} · Schuldenfrei 2070', f'{ch["kicker"]}: {ch["title"]}. Aus dem Buch „Schuldenfrei 2070“ von Tomas Hecker, online lesen.', body, ch['slug']))
    # Suchindex: Abschnitte
    cur_id, cur_t, buf = '', ch['title'], []
    def flush():
        txt = re.sub(r'\s+', ' ', ' '.join(buf)).strip()
        if txt: index_entries.append({'p': ch['slug'], 'i': cur_id, 't': cur_t, 'k': ch['title'], 'x': txt})
    lead_txt = BeautifulSoup(ch['lead'], 'html.parser').get_text(' ') if ch['lead'] else ''
    buf.append(lead_txt)
    for el in ch['body'].find_all(recursive=False):
        if el.name in ('h2',):
            flush(); cur_id, cur_t, buf = el['id'], el.get_text(' ', strip=True), []
        else:
            if el.name == 'aside': continue
            c = BeautifulSoup(str(el), 'html.parser')
            for sv in c.find_all('svg'): sv.decompose()
            buf.append(c.get_text(' '))
    flush()

open(os.path.join(OUT, 'suche-index.js'), 'w', encoding='utf-8').write('window.BUCH_INDEX=' + json.dumps(index_entries, ensure_ascii=False, separators=(',', ':')) + ';\n')

# ---------- Übersicht ----------
lis = []
for c in chapters:
    subs = ''.join(f'<li><a href="{c["slug"]}.html#{i}">{f"<b>{a}</b> " if a else ""}{html.escape(t[len(a):].strip() if a else t)}</a></li>' for i, t, a in c['heads'])
    lis.append(f'''<li class="kap"><details{" open" if c["no"] in ("5", "7") else ""}><summary><a href="{c["slug"]}.html"><span class="no">{c["no"]}</span><span class="tt">{html.escape(c["title"])}</span></a></summary>{f'<ol class="sub">{subs}</ol>' if subs else ''}</details></li>''')
uebersicht = f'''<div class="bhero big"><div class="bwrap"><div><p class="eyebrow">Das Buch online lesen</p><h1>Schuldenfrei 2070</h1><p class="blead">Warum wir uns auf die Zukunft freuen können. Das ganze Buch, Kapitel für Kapitel, mit allen Grafiken. Tippe auf ein Kapitel, um es zu lesen, oder auf den Pfeil, um seine Abschnitte zu sehen.</p>
<div class="btns"><a class="btn" href="vorwort.html">Mit dem Vorwort beginnen</a><a class="btn ghost" href="Schuldenfrei-2070.pdf" download>Als PDF herunterladen</a></div></div></div></div>
<main class="wrap uebersicht">{SEARCHBOX}<h2>Inhalt</h2><ol class="ktoc">{''.join(lis)}</ol>
<aside class="rechner"><div><strong>Selbst nachrechnen</strong><p>Was das Steuersystem aus Kapitel 5 für deinen Haushalt bedeutet, zeigt der Steuerrechner.</p></div><div class="rbtns"><a class="rbtn" href="../steuerrechner/">Zum Steuerrechner</a></div></aside></main>'''
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page('Das Buch online lesen · Schuldenfrei 2070', 'Schuldenfrei 2070 von Tomas Hecker: das ganze Buch online lesen, mit Inhaltsverzeichnis, Suche und Verweisen zum Nachrechnen.', uebersicht))

suche = f'''<main class="wrap uebersicht"><h1 class="sh">Im Buch suchen</h1>{SEARCHBOX}<p id="treffer-info" class="small"></p><ol id="treffer" class="treffer"></ol><p><a href="./">Zum Inhaltsverzeichnis</a></p></main>'''
open(os.path.join(OUT, 'suche.html'), 'w', encoding='utf-8').write(page('Im Buch suchen · Schuldenfrei 2070', 'Volltextsuche im Buch Schuldenfrei 2070.', suche, extra_head='<script src="suche-index.js" defer></script>\n'))
# ---------- Feste Buchstellen: stelle.html#anh-C2, #kap-7 oder jede id aus der Satzdatei ----------
import json as _json, glob as _glob
stellen = {}
for k, v in appendix_ids.items(): stellen['anh-' + k] = v
for b in 'ABC': stellen['anh-' + b] = f'anhang-{b.lower()}.html'
for i in range(1, 10):
    if os.path.exists(os.path.join(OUT, f'kapitel-{i}.html')): stellen[f'kap-{i}'] = f'kapitel-{i}.html'
for f in sorted(_glob.glob(os.path.join(OUT, '*.html'))):
    nm = os.path.basename(f)
    if nm in ('index.html', 'suche.html', 'stelle.html'): continue
    for i in re.findall(r' id="([^"]+)"', open(f, encoding='utf-8').read()):
        if i not in ('top', 'seite', 'q', 'treffer', 'treffer-info') and i not in stellen: stellen[i] = f'{nm}#{i}'
stelle = ('<main class="wrap uebersicht"><h1 class="sh">Buchstelle</h1><p id="st">Die Buchstelle wird geöffnet …</p><p><a href="./">Zum Inhaltsverzeichnis</a></p></main>'
  '<script>(function(){var S=' + _json.dumps(stellen, ensure_ascii=False) + ';var k=decodeURIComponent((location.hash||"").slice(1));'
  'if(S[k]){location.replace(S[k]);}else{document.getElementById("st").textContent=k?"Diese Buchstelle gibt es nicht: "+k:"Keine Buchstelle angegeben.";}})();</script>')
open(os.path.join(OUT, 'stelle.html'), 'w', encoding='utf-8').write(page('Buchstelle · Schuldenfrei 2070', 'Weiterleitung auf eine Stelle im Buch Schuldenfrei 2070.', stelle))
open(os.path.join(OUT, 'stellen.json'), 'w', encoding='utf-8').write(_json.dumps(stellen, ensure_ascii=False, indent=0))
print(len(chapters), 'Kapitel,', len(index_entries), 'Suchabschnitte,', len(appendix_ids), 'Anhang-Anker,', len(stellen), 'Buchstellen')
