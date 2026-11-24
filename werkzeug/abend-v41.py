#!/usr/bin/env python3
"""Drei Regeln vom Abend des 21.11.2026 im Steuerrechner (wie version-41/modell-v41, Liesmich.md):
- Bürgerjob 18 Stunden zum Mindestlohn nach dem Wechsel (BJMLNeu 16,84 €, BJPlus, EPLohn 1.313,52 €, EPEGUeber, ChWerkstatt).
- Altvermögenskonto frei bis zur Rate nach der Restlebenszeit (AVKRate, Reihe avkr), Mehrentlastung zum Teil VhAVKPlus beim Plus.
- Erben geben ihren Teil nach derselben Rate aus (ErbRate, Reihen erbo und erbm), Ersparnis im Saldo bei gleichem Einkauf.
Werte in abend-v41-werte.json. Läuft nach nachtrag-v41.py. Ein zweiter Lauf ändert nichts."""
import json, os
p = 'steuerrechner/index.html'
s = open(p, encoding='utf-8').read()
if 'Regeln vom Abend 21.11.2026' in s:
    raise SystemExit
W = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'abend-v41-werte.json'), encoding='utf-8'))
js = lambda x: json.dumps(x, ensure_ascii=False)
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)

rep('const A = structuredClone(ANNAHMEN);', f'''// Regeln vom Abend 21.11.2026: Bürgerjob 18 Stunden zum Mindestlohn nach dem Wechsel, Altvermögenskonto mit der Rate nach der
// Restlebenszeit, Erben nach derselben Rate
Object.assign(ANNAHMEN, {js(W["A"])});
const A = structuredClone(ANNAHMEN);''')
rep('const mikro = (key, k) => {', f'''Object.assign(MIKRO, {js(W["MIKRO"])});   // Abend 21.11.2026: Altvermögenskonto mit der Rate (avkr), Erbteile auf einmal (erbo) und nach der Rate (erbm)
const mikro = (key, k) => {{''')
rep('  const avk = A.UebMikro ? A.AVKGrenzeF * mikro("avk", k) : A.AltUeb * Math.max(0, 1 - (k - 1) / A.AVKJahre);   // Version 36',
    '  const avk = A.UebMikro ? (A.AVKRate ? mikro("avkr", k) : A.AVKGrenzeF * mikro("avk", k)) : A.AltUeb * Math.max(0, 1 - (k - 1) / A.AVKJahre);   // Version 36; Abend 21.11.2026: Rate nach der Restlebenszeit')
rep('function neueRegeln(k) {', '''// Abend 21.11.2026: Mehrentlastung der Rate gegenüber der festen Grenze (Mrd. €), davon VhAVKPlus beim Plus, der Rest beim Minus
function avkMehrJ(k) { return A.UebMikro && A.AVKRate ? mikro("avkr", k) - A.AVKGrenzeF * mikro("avk", k) : 0; }
// Abend 21.11.2026: Erben nach der Rate, Ersparnis gegenüber dem Ausgeben auf einmal (Mrd. €, weniger Ausfall)
function erbenRateJ(k) {
  if (!(A.UebMikro && A.ErbRate)) return 0;
  const i = Math.min(Math.max(k, 1), MIKRO.erbo.length) - 1, o = MIKRO.erbo[i], m = MIKRO.erbm[i];
  if (!(o > 0)) return 0;
  return (erbJ3(false) + (erbJ3(true) - erbJ3(false)) * Math.min(1, (k - 1) / A.Jahre)) * (1 - m / o);
}
function neueRegeln(k) {''')
rep('''  const vh = verhalten(steuer, ag.map((a, i) => { const d = schonfristJ(i + 1) - schonfristPlusJ(i + 1); return { ...a, plus: a.plus - d, minus: a.minus + d }; }));''',
    '''  const fav = 1 - (A.VhAVKPlus || 0), dav0 = avkMehrJ(1);   // Abend 21.11.2026: Altvermögenskonto mit der Rate
  const vh = verhalten(steuer, ag.map((a, i) => { const d = schonfristJ(i + 1) - schonfristPlusJ(i + 1), dv = avkMehrJ(i + 1); return { ...a, plus: a.plus - d - fav * dv + dav0, minus: a.minus + d + fav * dv }; }));''')
rep('ag[i].rplus - ag[i].stund - ag[i].erzpfl);', 'ag[i].rplus - ag[i].stund - ag[i].erzpfl + erbenRateJ(i + 1));   // Abend 21.11.2026: Erben nach der Rate')
rep('+ A.BJOfTn * (A.BJOfStd * 52 * A.BJML +', '+ A.BJOfTn * (A.BJOfStd * 52 * (A.BJMLNeu ?? A.BJML) +')   # offener Bürgerjob zum Mindestlohn nach dem Wechsel
# Texte: Bürgerjob 18 Stunden zum Mindestlohn nach dem Wechsel
rep('verdient 21 Stunden in der Woche zum Mindestlohn, 1.265 € im Monat', 'verdient 18 Stunden in der Woche zum Mindestlohn von 16,84 €, 1.314 € im Monat')
rep('21 Stunden in der Woche zum Mindestlohn, 1.265 € im Monat (wer', '18 Stunden in der Woche zum Mindestlohn von 16,84 €, 1.314 € im Monat (wer')
rep('Vorschlag 21 Stunden in der Woche im Bürgerjob, 1.265 € im Monat', 'Vorschlag 18 Stunden in der Woche im Bürgerjob, 1.314 € im Monat')
open(p, 'w', encoding='utf-8').write(s)
print('Regeln vom Abend eingebaut')
