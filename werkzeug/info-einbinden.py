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

# Hinweis unter der Tabelle „Euro pro Jahr“: sie rechnet anders als das Säulenbild darüber
s = open(p, encoding='utf-8').read()
a = '<div class="tbl-wrap"><table id="hhTable"></table></div>'
if 'id="hhHinweis"' not in s and s.count(a) == 1:
    s = s.replace(a, a + '\n        <p class="note" id="hhHinweis">Die Tabelle vergleicht bei gleichen Ausgaben in Euro: Heute und mit der Reform gibst du gleich viel Geld aus. Das Säulenbild darüber rechnet bei gleichem Einkauf wie heute, dann steigen mit der Reform die Preise und die Mehrwertsteuer. Deshalb weichen die Zahlen etwas ab. Das Ergebnis ganz oben rechnet wie das Säulenbild.</p>')
    open(p, 'w', encoding='utf-8').write(s)
    print('Hinweis unter der Tabelle')
# Drei Spalten erst ab 1.360 px: darunter bleiben dem Säulenbild in der Mitte zu wenig Platz (Prüfung 16.11.2026)
s = open(p, encoding='utf-8').read()
a = '@media (min-width: 1200px) and (min-height: 620px) {'
if a in s:
    assert s.count(a) == 1
    s = s.replace(a, '@media (min-width: 1360px) and (min-height: 620px) {')
# Bestandsschutz und Zuschlag zur Rente sind zwei Posten: der Bestandsschutz heißt nicht „Zuschlag zur Rente“
s = s.replace('Der Zuschlag zur Rente beträgt ${eur(r.bsz)} im Jahr;', 'Er beträgt ${eur(r.bsz)} im Jahr;')
open(p, 'w', encoding='utf-8').write(s)
