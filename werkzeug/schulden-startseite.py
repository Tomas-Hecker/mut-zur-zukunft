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
label = ('Staatsschulden in Prozent der Wirtschaftsleistung bis 2070. Oben ohne Reform im mittleren Fall: 2070 rund 242 %, '
         'davon 26 Altschulden, 91 weil wir länger leben und 125 Demografieschulden, weil weniger Kinder geboren werden. '
         'Unten mit Reform und Zukunftsplan: schuldenfrei 2046 im zuversichtlichen, 2064 im mittleren und 2070 im vorsichtigen Fall, '
         '2070 im mittleren Fall 9 % Vermögen im Zukunftsfonds.')
svg = svg.replace('<svg ', f'<svg role="img" aria-label="{label}" ', 1)
p = 'index.html'; s = open(p, encoding='utf-8').read()
a = s.index('<section class="block" id="schulden">'); b = s.index('</div></section>', a)
sec = s[a:b]
sec2 = re.sub(r'<p class="sg-sub">.*?</p>', f'<p class="sg-sub">{d["untertitel"]}</p>', sec, count=1, flags=re.S)
sec2, n = re.subn(r'<svg.*?</svg>', lambda m: svg, sec2, count=1, flags=re.S); assert n == 1
sec2 = re.sub(r'<figcaption>.*?</figcaption>',
  '<figcaption>Eigene Rechnung auf Grundlage des <a href="https://dserver.bundestag.de/btd/20/112/2011235.pdf#page=7" target="_blank" rel="noopener">Sechsten Tragfähigkeitsberichts (BMF 2024)</a>. '
  'Schraffiert ist der Teil, der auf höhere Ausgaben für Krankenkasse und Pflege zurückgeht. Die drei Fälle und die Rechnung stehen in '
  '<a href="buch/kapitel-6.html">Kapitel&nbsp;6</a> und im <a href="buch/anhang-c.html#c9">Anhang&nbsp;C9</a>.</figcaption>', sec2, count=1, flags=re.S)
s = s[:a] + sec2 + s[b:]
open(p, 'w', encoding='utf-8').write(s)
print('schulden ok', len(svg))
