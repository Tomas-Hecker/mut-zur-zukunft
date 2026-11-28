#!/usr/bin/env python3
"""Tomas 28.11.2026, 10:42/10:48 UTC: Erdwärme-Kredit des Bundes (Fassung 2: Kredit zum Zins des Bundes, Zuschuss nur bis zur Lücke zum Gas),
Zeile EWAn wie im Rechenmodell: 1,25 Mrd. € Kredit im Jahr 2029 bis 2045, 40 Jahre, 5 Jahre ohne Tilgung, Erkundung 0,15, Versicherung 0,05,
Zuschüsse 0,05 Mrd. €. Pfad (Saldo je Jahr) aus version-41/daten/erdwaerme-pfad-2026-11-28.json. Läuft nach kosten-der-arbeit-v41.py."""
import json, sys
P = 'steuerrechner/index.html'
s = open(P, encoding='utf-8').read()
if 'EW_PFAD' in s:
    print('schon drin'); sys.exit()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a)); s = s.replace(a, b)
pf = json.load(open('/mnt/project-files/broschuere-mut-zur-zukunft/version-41/daten/erdwaerme-pfad-2026-11-28.json'))
pf = {k: round(v, 6) for k, v in pf.items() if int(k) <= 2100}
rep('function verkehrJ(k) {',
    '// Tomas 28.11.2026: Erdwärme-Kredit des Bundes (EWAn), Auszahlung minus Rückzahlung im Saldo, Zinsen fließen zurück\n'
    'const EW_PFAD = ' + json.dumps(pf, separators=(',', ':')) + ';\n'
    'function erdJ(k) { if (!A.EWAn) return 0; const j = A.Prognose.ReformStart - 1 + k; return EW_PFAD[j] ?? 0; }\n'
    'function verkehrJ(k) {')
rep('Object.assign(ANNAHMEN, { KostArb: 6.2 });', 'Object.assign(ANNAHMEN, { KostArb: 6.2 });\nObject.assign(ANNAHMEN, { EWAn: 1 });   // Erdwärme-Kredit des Bundes, Tomas 28.11.2026')
rep('+ coachStufenJ(y) + kleinJ(y) + verkehrJ(y);', '+ coachStufenJ(y) + kleinJ(y) + verkehrJ(y) + erdJ(y);')
# Texte nach saldo-verlauf-v41.json vom 28.11. 10:58 UTC (2029 -68,9, 2030 -57,2, 2070 33,6 Mrd. €)
for a, b, n in [
 ('im zweiten rund 67 Mrd.', 'im zweiten rund 69 Mrd.', 3),
 ('im dritten rund 54 Mrd.', 'im dritten rund 57 Mrd.', 2),
 ('2070 rund 33 Mrd.', '2070 rund 34 Mrd.', 1),
 ('2070 von rund 33 Mrd.', '2070 von rund 34 Mrd.', 1),
]:
    rep(a, b, n)
open(P, 'w', encoding='utf-8').write(s); print('ok')
