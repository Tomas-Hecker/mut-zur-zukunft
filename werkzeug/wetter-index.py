#!/usr/bin/env python3
"""Ergänzt wetter/bereiche.json um Kennzahlen je Postleitzahlbereich, gerechnet aus dem Wetterjahr:
 th  Mittel der Außentemperatur in den Heizstunden (unter 15 °C, gewichtet mit der Heizlast)
 jf  Jahresarbeitszahl einer Luft-Wasser-Wärmepumpe im Bereich geteilt durch die im Bezugsort,
     gerechnet wie im Energie-Rechner (Wärme 15.000 kWh, davon 2.500 Warmwasser, Vorlauf 45 °C, Heizgrenze 15 °C)
Die Auslegungstemperatur bleibt überall −12 °C wie im Energie-Rechner: Ein typisches meteorologisches Jahr enthält
bewusst keine Extreme, seine kältesten Tage taugen deshalb nicht für die Norm-Außentemperatur.
Bezug: das Wetterjahr Idstein, das im Energie-Rechner eingebaut ist und mit dem die Rechner ohne Postleitzahl rechnen.
Aufruf: python3 werkzeug/wetter-index.py [wetter-ordner]"""
import json, math, os, sys
ORD = sys.argv[1] if len(sys.argv) > 1 else 'wetter'
N = 8760
WW_P = [0,0,0,0,0,.5,1.5,1.5,1,.6,.4,.4,.6,.4,.3,.3,.4,.7,1.2,1.4,1.2,.8,.4,.1]

def kennzahlen(t, ausl=-12.0, waerme=15000, ww=2500, vl=45, heizgr=15):
    tm = t[0]; qh = []
    for x in t:
        tm = tm + (x - tm) / 18; te = 0.7 * tm + 0.3 * x; qh.append(max(0.0, heizgr - te))
    sg = sum(qh); raum = waerme - ww; qh = [q * raum / sg for q in qh]
    sw = sum(WW_P[i % 24] for i in range(N)); wwq = [WW_P[i % 24] * ww / sw for i in range(N)]
    el = 0.0
    for i, ta in enumerate(t):
        v = 28 if ta >= heizgr else min(vl, 28 + (vl - 28) * (heizgr - ta) / (heizgr - ausl))
        abt = 0.92 if -3 < ta < 5 else 1
        c = lambda T: min(7, max(1.4, 0.45 * (T + 5 + 273.15) / (T + 5 - (ta - 6)) * abt))
        el += qh[i] / c(v) + wwq[i] / c(52)
    jaz = waerme / el
    th = sum(q * x for q, x in zip(qh, t)) / raum
    return jaz, th

B = {k: v for k, v in json.load(open(os.path.join(ORD, 'bereiche.json'), encoding='utf-8')).items() if not k.startswith('_')}
T = {}
for b in B:
    T[b] = [x / 10 for x in json.load(open(os.path.join(ORD, b + '.json')))['t']]
_s = open('energie-rechner/index.html', encoding='utf-8').read(); _i = _s.index('const D = ') + 10
TB = [x / 10 for x in json.loads(_s[_i:_s.index(';\n', _i)])['t']]
j0, th0 = kennzahlen(TB)
for b in B:
    jaz, th = kennzahlen(T[b])
    B[b].pop('tk', None); B[b].update(th=round(th, 1), jaz=round(jaz, 3))
for b in B: B[b]['jf'] = round(B[b].pop('jaz') / j0, 3)
B['_bezug'] = {'n': 'Idstein', 'th': round(th0, 1), 'jaz': round(j0, 3)}
json.dump(B, open(os.path.join(ORD, 'bereiche.json'), 'w'), separators=(',', ':'), ensure_ascii=False)
v = sorted((B[b]['jf'], b, B[b]['n']) for b in B if not b.startswith('_'))
print('Bezug', B['_bezug'], 'jf von', v[0], 'bis', v[-1])
