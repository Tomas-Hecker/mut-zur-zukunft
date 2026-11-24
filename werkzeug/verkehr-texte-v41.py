#!/usr/bin/env python3
"""Verkehrspaket 24.11.2026: Register-Texte im Steuerrechner auf 65 % und die neuen Ergebnisse (2100, 8,9 Punkte).
Läuft nach register-v41.py und verkehr-v41.py; zweiter Lauf ändert nichts."""
import sys
P = 'steuerrechner/index.html'
s = open(P, encoding='utf-8').read()
if '65 % (186 % Aufschlag)' in s:
    print('schon drin'); sys.exit()
R = [
 ('"66,7 % (200 % Aufschlag)","Aufschlag von 200 % auf die Ausgaben über dem Beginn von Stufe 4: Von 100 €, die dafür ins Private fließen, gehen zwei Drittel an die Steuer, für ein Drittel wird eingekauft. Gewählt am 17.11.2026: zwei Drittel statt 60 %, dafür ein höherer Freibetrag für alle.',
  '"65 % (186 % Aufschlag)","Aufschlag von rund 186 % auf die Ausgaben über dem Beginn von Stufe 4: Von 100 €, die dafür ins Private fließen, gehen 65 € an die Steuer, für 35 € wird eingekauft. Gewählt am 17.11.2026: zwei Drittel statt 60 %, dafür ein höherer Freibetrag für alle; seit dem Verkehrspaket vom 24.11.2026 65 %, bezahlt vom Aufschlag auf die Kilometerabgabe. Der Staatshaushalt rechnet wie das Rechenmodell weiter mit zwei Dritteln und zieht die 65 % mit dem geringeren Ausweichen netto im Pfad des Verkehrspakets ab, rund 8,6 Mrd. € im Jahr.'),
 ('im mittleren Fall 2097 schuldenfrei. Im vorsichtigen Fall steigt der Normalsatz der Mehrwertsteuer ab 2030 um gut 8,7 Punkte',
  'im mittleren Fall 2100 schuldenfrei. Im vorsichtigen Fall steigt der Normalsatz der Mehrwertsteuer ab 2030 um gut 8,9 Punkte'),
 ('im vorsichtigen Fall aus Anhang C9 ab 2030 gut 8,7 Punkte', 'im vorsichtigen Fall aus Anhang C9 ab 2030 gut 8,9 Punkte'),
 ('Für den Teil der Ausgaben über 5.000 € im Monat gelten zwei Drittel (Stufe 4).', 'Für den Teil der Ausgaben über 5.000 € im Monat gelten 65 % (Stufe 4, bis zum Verkehrspaket zwei Drittel).'),
 ('zwei Drittel statt der Hälfte an die Steuer (Satz4)', '65 % statt der Hälfte an die Steuer (Satz4)'),
 ('im Monat zwei Drittel Ausgabensteuer und auf das übrige Drittel die Mehrwertsteuer von 50 %, zusammen rund 78 %', 'im Monat 65 % Ausgabensteuer und auf die übrigen 35 % die Mehrwertsteuer von 50 %, zusammen rund 77 %'),
]
for a, b in R:
    assert s.count(a) == 1, (a[:70], s.count(a)); s = s.replace(a, b)
open(P, 'w', encoding='utf-8').write(s); print('ok')
