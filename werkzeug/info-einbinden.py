#!/usr/bin/env python3
"""Bindet die Info-Knöpfe (info.js im Hauptordner und info-texte.js im Ordner des Rechners) in den Steuerrechner ein.
Läuft nach jedem Neubau des Steuerrechners (gen.py); ein zweiter Lauf ändert nichts."""
p = 'steuerrechner/index.html'
s = open(p, encoding='utf-8').read()
if 'src="../info.js"' not in s:
    a = '<script src="buchlinks.js"></script>'
    assert s.count(a) == 1, 'buchlinks.js nicht gefunden'
    s = s.replace(a, a + '\n<script src="../info.js"></script>\n<script src="info-texte.js"></script>')
    open(p, 'w', encoding='utf-8').write(s)
    print('Info-Knöpfe eingebunden')
