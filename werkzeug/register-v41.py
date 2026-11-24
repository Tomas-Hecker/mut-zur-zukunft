#!/usr/bin/env python3
"""Ersetzt das Register „Woher die Zahlen kommen“ (const REG) im Steuerrechner durch das Register des Buchs
(version-41/modell-v41/annahmen-register.json). Zeile: [Name, Bezeichnung, Art, Anzeige, Herleitung, Quellen [[Text, URL]],
Buchstellen [[Stelle, Titel, URL]], aktiv (1/0), nicht verwendet, Einheit des Eingabefelds]. Die Einheit des Eingabefelds
bleibt wie bisher; neue Werte bekommen sie aus der Einheit im Register. Aufruf: python3 werkzeug/register-v41.py <annahmen-register.json>"""
import json, sys
p = 'steuerrechner/index.html'
s = open(p, encoding='utf-8').read()
R = json.load(open(sys.argv[1], encoding='utf-8'))
i = s.index('const REG = ') + 12
ALT, n = json.JSONDecoder().raw_decode(s[i:])
u_alt = {r[0]: r[9] for g in ALT['g'] for r in g['r']}
EINH = {'Mrd. €': 'mrd', '%': 'pct', '€': 'eur', '€/Jahr': 'eur', '€/Monat': 'eurm', 'Mio.': 'mio', 'Stunden': 'std', 'Jahre': 'jahre'}
gr = {g: [] for g in R['gruppen']}
for w in R['werte']:
    u = u_alt.get(w['name'], EINH.get(w.get('einheit') or '', '') if isinstance(w.get('wert'), (int, float)) and w.get('einheit') not in ('0/1',) else '')
    row = [w['name'], w['label'], w['art'], w['anzeige'], w['herleitung'],
           [[q.get('text', ''), q.get('url', '')] for q in w.get('quellen') or []],
           [[b['stelle'], b['titel'], b['url']] for b in w.get('buch') or []],
           1 if w.get('aktiv', True) else 0, w.get('nicht_verwendet') or '', u]
    gr.setdefault(w['gruppe'], []).append(row)
REG = {'stand': R['stand'], 'arten': [[a['art'], a['bedeutung']] for a in R['arten']], 'g': [{'t': t, 'r': r} for t, r in gr.items() if r]}
s = s[:i] + json.dumps(REG, ensure_ascii=False, separators=(',', ':')) + s[i + n:]
open(p, 'w', encoding='utf-8').write(s)
neu = [w['name'] for w in R['werte'] if w['name'] not in u_alt]
print('Register:', sum(len(g['r']) for g in REG['g']), 'Werte in', len(REG['g']), 'Gruppen; neu:', len(neu), neu[:30])
