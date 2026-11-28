#!/usr/bin/env python3
"""Tomas 27.11.2026, 18:14 UTC: Umzug für eine neue Stelle, Werkzeug und Arbeitskleidung nach fester Liste und der Arbeitsplatz zu Hause
zählen nicht als Ausgabe, zusammen 6,2 Mrd. € 2028, gleicher Anteil am BIP, ab 2028 voll (Zeile KostArb wie im Rechenmodell).
Läuft nach mentoren-v41.py; zweiter Lauf ändert nichts."""
import sys
P = 'steuerrechner/index.html'
s = open(P, encoding='utf-8').read()
if 'KostArb' in s:
    print('schon drin'); sys.exit()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a)); s = s.replace(a, b)
rep("Object.assign(ANNAHMEN, { StartGrund: 5000, StartSatz: 0, VerfFam: 1.0, CoachN: 70000 * 750 / 900, MentNetz: 0.2 });",
    "Object.assign(ANNAHMEN, { StartGrund: 5000, StartSatz: 0, VerfFam: 1.0, CoachN: 70000 * 750 / 900, MentNetz: 0.2 });\n"
    "// Tomas 27.11.2026, 18:14: Kosten der Arbeit (Umzug für die Stelle 1,9, Werkzeug und Arbeitskleidung 2,0, Arbeitsplatz zu Hause 2,3 Mrd. €) frei von der Ausgabensteuer\n"
    "Object.assign(ANNAHMEN, { KostArb: 6.2 });")
rep('    ["Mentoren-Netz bei den Kammern: ein Mentor aus deinem Beruf, freiwillig", A.MentNetz, A.MentNetz],',
    '    ["Mentoren-Netz bei den Kammern: ein Mentor aus deinem Beruf, freiwillig", A.MentNetz, A.MentNetz],\n'
    '    ["Kosten der Arbeit zählen nicht als Ausgabe: Umzug für eine neue Stelle, Werkzeug und Arbeitskleidung, Arbeitsplatz zu Hause", A.KostArb, A.KostArb],')
for a, b, n in [
 ('ab 2037 bleibt ein Überschuss', 'ab 2038 bleibt ein Überschuss', 4),
 ('fehlen im ersten Jahr rund 54 Mrd.', 'fehlen im ersten Jahr rund 60 Mrd.', 4),
 ('im zweiten rund 61 Mrd.', 'im zweiten rund 67 Mrd.', 3),
 ('im dritten rund 48 Mrd.', 'im dritten rund 54 Mrd.', 2),
 ('2070 rund 39 Mrd.', '2070 rund 33 Mrd.', 1),
 ('2070 von rund 39 Mrd.', '2070 von rund 33 Mrd.', 1),
 ('rund 8,4 Punkte', 'rund 8,8 Punkte', 2),
 ('im zuversichtlichen Fall 2055 und im mittleren Fall 2092', 'im zuversichtlichen Fall 2055 und im mittleren Fall 2095', 1),
 ('im zuversichtlichen Fall ab 2032, im mittleren Fall ab 2037.', 'im zuversichtlichen Fall ab 2033, im mittleren Fall ab 2038.', 1),
]:
    rep(a, b, n)
open(P, 'w', encoding='utf-8').write(s); print('ok')
