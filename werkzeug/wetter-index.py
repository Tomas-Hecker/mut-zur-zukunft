#!/usr/bin/env python3
"""Ergänzt wetter/bereiche.json um Kennzahlen je Postleitzahlbereich, gerechnet aus dem Wetterjahr:
 th  Mittel der Außentemperatur in den Heizstunden (unter 15 °C, gewichtet mit der Heizlast)
 jf  Jahresarbeitszahl einer Luft-Wasser-Wärmepumpe im Bereich geteilt durch die im Bezugsort,
     gerechnet wie im Energie-Rechner (Wärme 15.000 kWh, davon 2.500 Warmwasser, Vorlauf 45 °C, Heizgrenze 15 °C)
Die Auslegungstemperatur bleibt überall −12 °C wie im Energie-Rechner: Ein typisches meteorologisches Jahr enthält
bewusst keine Extreme, seine kältesten Tage taugen deshalb nicht für die Norm-Außentemperatur.
Ein einzelnes typisches Jahr ist verrauscht (die Monate werden aus verschiedenen Jahren gewählt, Nachbarbereiche
weichen deshalb um bis zu 1,5 K ab). Deshalb geglättet: th = Höhengradient (Ausgleich über alle Bereiche) plus
Rest, der Rest gemittelt über die Nachbarbereiche (Gauß, 25 km). jf kommt aus dem Ausgleich JAZ ~ th über alle
Bereiche, bezogen auf den Bereich 655 (Idstein), und ist auf 0,05 gerundet. So bekommt Idstein mit und ohne
Postleitzahl dieselbe Jahresarbeitszahl.
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
BEZUG = '655'   # Idstein
roh = {b: kennzahlen(T[b]) for b in B}   # (jaz, th)
def ausgleich(xs, ys):
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    k = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); return my - k * mx, k
L = list(B)
a, k = ausgleich([B[b]['z'] for b in L], [roh[b][1] for b in L])           # th über Höhe
rest = {b: roh[b][1] - (a + k * B[b]['z']) for b in L}
def km(p, q):
    return math.hypot((B[p]['lat'] - B[q]['lat']) * 111.2, (B[p]['lon'] - B[q]['lon']) * 111.2 * math.cos(math.radians(B[p]['lat'])))
th = {}
for b in L:
    w = [(math.exp(-(km(b, q) / 25) ** 2 / 2), q) for q in L]; w = [(g, q) for g, q in w if g > 0.01]
    th[b] = a + k * B[b]['z'] + sum(g * rest[q] for g, q in w) / sum(g for g, _ in w)
aj, kj = ausgleich([roh[b][1] for b in L], [roh[b][0] for b in L])          # JAZ über th
jaz = lambda t: aj + kj * t
for b in L:
    B[b].pop('tk', None); B[b].pop('jaz', None)
    B[b]['th'] = round(th[b], 1); B[b]['jf'] = round(round(jaz(th[b]) / jaz(th[BEZUG]) / 0.05) * 0.05, 2)
B['_bezug'] = {'n': 'Idstein', 'bereich': BEZUG, 'th': B[BEZUG]['th'], 'jaz': round(jaz(th[BEZUG]), 3)}
print(f'Höhengradient {k*1000:.2f} K/1000 m, JAZ = {aj:.3f} + {kj:.3f} · th')
json.dump(B, open(os.path.join(ORD, 'bereiche.json'), 'w'), separators=(',', ':'), ensure_ascii=False)
v = sorted((B[b]['jf'], b, B[b]['n']) for b in L)
print('Bezug', B['_bezug'], 'jf von', v[0], 'bis', v[-1])
