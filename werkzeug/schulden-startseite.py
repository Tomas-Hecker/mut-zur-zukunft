#!/usr/bin/env python3
"""Setzt die Schuldengrafik aus dem Buch (SVG und Reihen vom Buchfaden) in den Abschnitt #schulden der Startseite.
Aufruf: python3 werkzeug/schulden-startseite.py <grafik.svg> <schuldengrafik.json>
Ändert nur die Grafik und die Unterzeile; Überschrift, Text und Links bleiben."""
import json, re, sys
svg_p, js_p = sys.argv[1], sys.argv[2]
d = json.load(open(js_p, encoding='utf-8'))
svg = open(svg_p, encoding='utf-8').read()
svg = re.search(r'<svg.*</svg>', svg, re.S).group(0)
svg = re.sub(r'\s+xmlns:c2pa="[^"]*"', '', svg)
svg = re.sub(r'<metadata.*?</metadata>', '', svg, flags=re.S)
o = d['oben_ohne_reform_mittel']; u = d['unten_mit_reform_und_zukunftsplan']
# Zahlen 2070 ohne Reform aus den Beschriftungen der Grafik selbst (der obere Block im JSON kann älter sein als die Grafik)
num = lambda x: int(x.replace('−', '-'))
teile = [num(v) for v in re.findall(r'<text[^>]*x="369\.0"[^>]*>([0-9]+)</text>', svg)]
assert len(teile) == 3, teile
t = {'altschulden': teile[0], 'laenger_leben': teile[1], 'demografieschulden': teile[2], 'zusammen': num(re.search(r'>([0-9]+) % mittel<', svg).group(1))}
assert sum(teile) == t['zusammen'], (teile, t)
sp = {'vorsichtig': num(re.search(r'>([0-9]+) % vorsichtig<', svg).group(1)), 'zuversichtlich': num(re.search(r'>([0-9]+) % zuversichtlich<', svg).group(1))}
sf = u['schuldenfrei']; z = u['2070']
def stand2070(w):
    return f'2070 noch {w} % Schulden' if w > 0 else f'2070 {-w} % Vermögen im Zukunftsfonds'
label = (f'Staatsschulden in Prozent der Wirtschaftsleistung bis 2070. Oben ohne Reform im mittleren Fall: 2070 rund {t["zusammen"]} %, '
         f'davon {t["altschulden"]} Altschulden, {t["laenger_leben"]} weil wir länger leben und {t["demografieschulden"]} Demografieschulden, weil weniger Kinder geboren werden; '
         f'hellrot hinterlegt die Spanne von {sp["zuversichtlich"]} % im zuversichtlichen bis {sp["vorsichtig"]} % im vorsichtigen Fall. '
         f'Unten mit Reform und Zukunftsplan, hellgrün hinterlegt die Spanne: im mittleren Fall {stand2070(z["mittel"])}, schuldenfrei {sf["mittel"]}; '
         f'im zuversichtlichen Fall schuldenfrei {sf["zuversichtlich"]} und {stand2070(z["zuversichtlich"])}, im vorsichtigen Fall schuldenfrei {sf["vorsichtig"]}.')
svg = svg.replace('<svg ', f'<svg role="img" aria-label="{label}" ', 1)
p = 'index.html'; s = open(p, encoding='utf-8').read()
a = s.index('<section class="block" id="schulden">'); b = s.index('</div></section>', a)
sec = s[a:b]
sec2 = re.sub(r'<p class="sg-sub">.*?</p>', f'<p class="sg-sub">{d["untertitel"]}</p>', sec, count=1, flags=re.S)
sec2, n = re.subn(r'<svg.*?</svg>', lambda m: svg, sec2, count=1, flags=re.S); assert n == 1
sec2 = re.sub(r'<figcaption>.*?</figcaption>',
  '<figcaption>Eigene Rechnung auf Grundlage des <a href="https://dserver.bundestag.de/btd/20/112/2011235.pdf#page=7" target="_blank" rel="noopener">Sechsten Tragfähigkeitsberichts (BMF 2024)</a>. '
  'Die Linien zeigen den mittleren, wahrscheinlichsten Fall. Hell hinterlegt ist die Spanne vom vorsichtigen bis zum zuversichtlichen Fall, hellrot ohne Reform, hellgrün mit Reform. '
  'Schraffiert ist der Teil, der auf höhere Ausgaben für Krankenkasse und Pflege zurückgeht. Die drei Fälle und die Rechnung stehen in '
  '<a href="buch/kapitel-6.html">Kapitel&nbsp;6</a> und im <a href="buch/anhang-c.html#c9">Anhang&nbsp;C9</a>.</figcaption>', sec2, count=1, flags=re.S)
s = s[:a] + sec2 + s[b:]
open(p, 'w', encoding='utf-8').write(s)
print('schulden ok', len(svg))
