#!/usr/bin/env python3
"""Lädt für jeden Postleitzahlbereich (erste drei Ziffern) ein typisches meteorologisches Jahr aus PVGIS 5.3
(Europäische Kommission, JRC; © Europäische Union, CC BY 4.0) und schreibt es nach wetter/<bereich>.json.
Aufruf: python3 werkzeug/wetter-laden.py <regionen.json> <cache-ordner> [ziel-ordner]
regionen.json: {"653": {"n": "Eltville am Rhein", "lat": 50.04, "lon": 8.06}, ...}
Lage je Bereich: der größte Ort (Einwohner nach GeoNames cities500, CC BY 4.0), nicht der Mittelpunkt,
damit Bereiche in den Bergen nicht auf einem Gipfel liegen.
Format je Bereich wie das eingebaute Wetter der Energie-Rechner: Stunde für Stunde in MEZ,
t in Zehntel °C, rh in %, g (Global) und d (Diffus) waagrecht in W/m²."""
import json, os, sys, time, urllib.request, concurrent.futures as cf
REG, CACHE = sys.argv[1], sys.argv[2]
ZIEL = sys.argv[3] if len(sys.argv) > 3 else 'wetter'
os.makedirs(CACHE, exist_ok=True); os.makedirs(ZIEL, exist_ok=True)
R = json.load(open(REG, encoding='utf-8'))
N = 8760

def hole(p):
    c = os.path.join(CACHE, p + '.json')
    if os.path.exists(c): return p, json.load(open(c))
    r = R[p]; url = f"https://re.jrc.ec.europa.eu/api/v5_3/tmy?lat={r['lat']}&lon={r['lon']}&outputformat=json"
    for v in range(5):
        try:
            with urllib.request.urlopen(url, timeout=90) as f: T = json.load(f)
            h = T['outputs']['tmy_hourly']; assert len(h) >= N
            k = lambda key, s=1: [round(h[(i - 1) % N][key] * s) for i in range(N)]   # UTC -> MEZ: eine Stunde später
            o = {'z': T['inputs']['location']['elevation'], 't': k('T2m', 10), 'rh': k('RH'), 'g': k('G(h)'), 'd': k('Gd(h)')}
            json.dump(o, open(c, 'w')); return p, o
        except Exception as e:
            time.sleep(3 * (v + 1)); err = e
    raise RuntimeError(f'{p}: {err}')

idx = {}
with cf.ThreadPoolExecutor(6) as ex:
    for p, o in ex.map(hole, sorted(R)):
        r = R[p]
        t = [x / 10 for x in o['t']]
        idx[p] = {'n': r['n'], 'lat': r['lat'], 'lon': r['lon'], 'z': round(o['z']),
                  'tm': round(sum(t) / N, 1), 'gs': round(sum(o['g']) / 1000)}
        json.dump({'n': r['n'], 'lat': r['lat'], 'lon': r['lon'], 'z': round(o['z']), 't': o['t'], 'rh': o['rh'], 'g': o['g'], 'd': o['d']},
                  open(os.path.join(ZIEL, p + '.json'), 'w'), separators=(',', ':'), ensure_ascii=False)
json.dump(idx, open(os.path.join(ZIEL, 'bereiche.json'), 'w'), separators=(',', ':'), ensure_ascii=False)
print('Bereiche', len(idx))
