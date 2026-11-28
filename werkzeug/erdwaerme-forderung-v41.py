#!/usr/bin/env python3
"""Buch 28.11.2026 12:45 UTC: Erdwärme-Kredit zählt wie alle Darlehen als Forderung; im Saldo nur Erkundung,
Versicherung und entgangene Zinsen. Pfad neu aus version-41/daten/erdwaerme-pfad-2026-11-28.json, Texte nach
saldo-verlauf-v41.json 12:37 UTC (2029 -67,8, 2030 -56,4, 2070 32,8 Mrd. €). Läuft nach eauto-auslauf-v41.py."""
import json, re
P = 'steuerrechner/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a)); s = s.replace(a, b)
pf = json.load(open('/mnt/project-files/broschuere-mut-zur-zukunft/version-41/daten/erdwaerme-pfad-2026-11-28.json'))
pf = {k: round(v, 6) for k, v in pf.items() if int(k) <= 2100}
s, n = re.subn(r'const EW_PFAD = \{.*?\};', 'const EW_PFAD = ' + json.dumps(pf, separators=(',', ':')) + ';', s); assert n == 1
if 'im zweiten rund 69 Mrd.' in s:
    rep('im zweiten rund 69 Mrd.', 'im zweiten rund 68 Mrd.', 3)
    rep('im dritten rund 58 Mrd.', 'im dritten rund 56 Mrd.', 2)
    rep('2070 rund 34 Mrd.', '2070 rund 33 Mrd.', 1)
    rep('2070 von rund 34 Mrd.', '2070 von rund 33 Mrd.', 1)
    rep('schuldenfrei wird der Staat dann 2090 (Anhang C9)', 'schuldenfrei wird der Staat dann 2091 (Anhang C9)', 1)
open(P, 'w', encoding='utf-8').write(s); print('ok')
