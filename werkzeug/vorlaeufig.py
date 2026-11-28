#!/usr/bin/env python3
"""Tomas 28.11.2026, 13:42 UTC: Der Abschnitt zu großen Gebäuden (Hallen, Schulen, Kliniken) wird neu geprüft,
weil Großwärmepumpen und neue Wärmeverteilung wohl teurer sind. Bis die neuen Zahlen da sind, steht im Online-Buch
ein Hinweis unter den Überschriften. Nach jedem buch-bauen.py laufen lassen; ohne Wirkung, wenn die Überschrift fehlt."""
import re
HINWEIS = ('<p class="vorlaeufig" role="note"><b>Vorläufig:</b> Die Zahlen in diesem Abschnitt werden gerade neu geprüft. '
           'Großwärmepumpen und eine neue Wärmeverteilung mit größeren Heizkörpern kosten in großen Gebäuden '
           'wohl deutlich mehr als hier gerechnet. Die geprüften Zahlen folgen.</p>')
STELLEN = {}
for f, anker in STELLEN.items():
    s = open(f, encoding='utf-8').read()
    if 'class="vorlaeufig"' in s and anker in s.split('class="vorlaeufig"')[0][-400:]:
        print(f, 'schon drin'); continue
    m = re.search(r'(<h[2-4] id="' + anker + r'">.*?</h[2-4]>)', s)
    if not m:
        print(f, 'Überschrift fehlt'); continue
    s = s[:m.end()] + HINWEIS + s[m.end():]
    open(f, 'w', encoding='utf-8').write(s); print(f, 'ok')
c = open('buch/buch.css', encoding='utf-8').read()
if '.vorlaeufig' not in c:
    c += ('\n/* Hinweis auf Abschnitte, die neu geprüft werden (werkzeug/vorlaeufig.py) */\n'
          '.vorlaeufig{margin:.6rem 0 1.2rem;padding:.7rem 1rem;border-left:4px solid #C8532C;background:rgba(200,83,44,.08);'
          'font-family:Inter,system-ui,sans-serif;font-size:.95rem;line-height:1.45}\n')
    open('buch/buch.css', 'w', encoding='utf-8').write(c)
