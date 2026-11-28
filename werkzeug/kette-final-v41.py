#!/usr/bin/env python3
"""Buch 28.11.2026 13:37 UTC, Kette mit allen Stufen: Stromsteuer und Umlagen auf neuen Strom, Rohre bei Etagenheizungen,
Heizkörper und Einbau im Mietshaus, Warmwasser-Wärmepumpen, E-Lkw-Kredit, steigende Rate (+2 %). Pfad je Jahr
(summe; die steigende Rate steckt nach dem Abgleich mit kette-jahresreihe-v41.json schon darin) aus rechenmodell-mikrosim/strom-5-prozent-2026-11-28/unterschied-jahr-fuer-jahr-ab-eauto-mit-rate.json,
gleich der Zeile kette_final in saldo-verlauf-v41.json. Läuft nach erdwaerme-forderung-v41.py."""
import json, sys
P = 'steuerrechner/index.html'
s = open(P, encoding='utf-8').read()
if 'KF_PFAD' in s:
    print('schon drin'); sys.exit()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a)); s = s.replace(a, b)
d = json.load(open('/mnt/project-files/rechenmodell-mikrosim/strom-5-prozent-2026-11-28/unterschied-jahr-fuer-jahr-ab-eauto-mit-rate.json'))['jahre']
kf = {y: round(v['summe'], 4) for y, v in d.items() if int(y) <= 2110}
rep('function verkehrJ(k) {',
    '// Buch 28.11.2026: letzte Stufen der Kette (Strom, Etagenheizung, Mietshaus, Warmwasser-Wärmepumpe, E-Lkw, steigende Rate)\n'
    'const KF_PFAD = ' + json.dumps(kf, separators=(',', ':')) + ';\n'
    'function ketteJ(k) { const j = A.Prognose.ReformStart - 1 + k; return KF_PFAD[j] ?? KF_PFAD[Math.min(2110, Math.max(2028, j))]; }\n'
    'function verkehrJ(k) {')
rep('+ verkehrJ(y) + erdJ(y) + eautoJ(y);', '+ verkehrJ(y) + erdJ(y) + eautoJ(y) + ketteJ(y);')
# Texte nach saldo-verlauf-v41.json 13:09 UTC (2028 -61,0, 2029 -69,6, 2030 -58,7, 2039 +0,4, 2070 22,7 Mrd. €) und Kette 13:20 UTC
for a, b, n in [
 ('fehlen im ersten Jahr rund 60 Mrd.', 'fehlen im ersten Jahr rund 61 Mrd.', 4),
 ('im zweiten rund 68 Mrd.', 'im zweiten rund 70 Mrd.', 3),
 ('im dritten rund 56 Mrd.', 'im dritten rund 59 Mrd.', 2),
 ('2070 rund 33 Mrd.', '2070 rund 23 Mrd.', 1),
 ('2070 von rund 33 Mrd.', '2070 von rund 23 Mrd.', 1),
 ('ab 2038 bleibt ein Überschuss', 'ab 2039 bleibt ein Überschuss', 4),
 ('hat der ganze Staat ab 2038 einen Überschuss', 'hat der ganze Staat ab 2039 einen Überschuss', 1),
 ('im zuversichtlichen Fall ab 2033, im mittleren Fall ab 2038.', 'im zuversichtlichen Fall ab 2033, im mittleren Fall ab 2039.', 1),
 ('rund 8,8 Punkte', 'rund 9,2 Punkte', 2),
 ('im zuversichtlichen Fall 2055 und im mittleren Fall 2095', 'im zuversichtlichen Fall 2056 und im mittleren Fall 2101', 1),
 ('${frei ? "schuldenfrei " + frei + ", " : ""}mit Zukunftsplan', '${frei ? "schuldenfrei " + frei + ", " : e.plan > 0 ? "schuldenfrei erst nach 2100, " : ""}mit Zukunftsplan', 1),
 ('schuldenfrei wird der Staat dann 2091 (Anhang C9)', 'schuldenfrei wird der Staat dann 2092 (Anhang C9)', 1),
]:
    rep(a, b, n)
open(P, 'w', encoding='utf-8').write(s); print('ok')
