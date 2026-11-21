#!/usr/bin/env python3
"""Nachträge vom 18. und 21.11.2026 zum Buch Version 41 im Steuerrechner (wie version-41/modell-v41, Liesmich.md):
- Hausregel für den beim Start offenen Teil (HRNurNeu = 0): im ersten Jahr zählt HRSatz / HRMietQ des Mietwerts, nur für die Fläche
  bis HRFlErst für die erste Person und HRFlWeitere für jede weitere (neues Feld Wohnfläche); Staatsseite mit den neuen Reihen hr und hrp.
- Gesundheitsaufschlag auf die Kilometerabgabe ab 2041 (gesundheitsaufschlag_j).
- Schuldenprognose: Mehr der Lkw-Maut je nach Fall (vorsichtig nichts, mittel die Hälfte, zuversichtlich voll), Staat zuerst (V41S) und
  die Hälfte an alle erst, wenn der Kredit für den Übergang nicht mehr wächst (V41E), wie kette/schulden/zp19.py.
Werte in nachtrag-v41-werte.json. Läuft nach kinder-600.py. Ein zweiter Lauf ändert nichts."""
import json, os
p = 'steuerrechner/index.html'
s = open(p, encoding='utf-8').read()
if 'Nachträge 21.11.2026' in s:
    raise SystemExit
W = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nachtrag-v41-werte.json'), encoding='utf-8'))
js = lambda x: json.dumps(x, ensure_ascii=False)
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)

# Annahmen und Reihen
rep('const A = structuredClone(ANNAHMEN);', f'''// Nachträge 21.11.2026 (Buch Version 41): Hausregel für den offenen Teil mit 60 m² und 20 m² je weiterer Person, Gesundheitsaufschlag,
// Lkw-Maut je nach Fall, Staat zuerst, die Hälfte an alle erst, wenn der Kredit für den Übergang nicht mehr wächst
Object.assign(ANNAHMEN, {js(W["A"])});
const A = structuredClone(ANNAHMEN);''')
rep('const mikro = (key, k) => {', f'''Object.assign(MIKRO, {js(W["MIKRO"])});   // Nachtrag 21.11.2026: Hausregel mit den neuen Flächen (hr), davon beim Plus (hrp)
const STRF_GA = {js(W["STRF"])};   // Nachtrag 21.11.2026: Sätze und kWh für den Gesundheitsaufschlag, Reformjahr 2028 bis 2072
const LKW = {js(W["LKW"])};   // Nachtrag 21.11.2026: Mehr der Lkw-Maut (Mrd. €), Anteil je Fall
const lkwFehlt = (sz, y) => y < LKW.ab ? 0 : (1 - (LKW.anteil[sz] ?? 1)) * (LKW.mehr[y] ?? LKW.mehr[Math.max(...Object.keys(LKW.mehr).map(Number))]);
const mikro = (key, k) => {{''')

# Haushalt: Hausregel für den offenen Teil
rep('  const mietw = A.Nutzwert > 0 ? h.miet * (1 - A.HausFrei * (h.hb || 0)) : 0;   // eigenes Haus frei: Mietwert nur auf den Teil, der beim Start nicht bezahlt war',
    '''  const hrFa = !(h.fl > 0) ? 1 : Math.min(1, (A.HRFlErst + A.HRFlWeitere * (h.erw + h.kinder - 1)) / h.fl);   // Anteil der Fläche unter der Hausregel
  const mietw = A.Nutzwert > 0 ? h.miet * (1 - A.HausFrei * (h.hb || 0)) - h.miet * (1 - (h.hb || 0)) * A.HRAn * (1 - A.HRNurNeu) * hrFa * (1 - A.HRSatz / A.HRMietQ) : 0;   // eigenes Haus frei, soweit beim Start bezahlt; für den offenen Teil die Hausregel (im ersten Jahr HRSatz / HRMietQ des Mietwerts)''')
rep('''<span class="hint">auf diesen Teil keine Steuer auf den Mietwert, bis Verkauf oder Erbgang, bis 200 m² Wohnfläche; geerbt nach dem Start zählt nicht</span></div>''',
    '''<span class="hint">dieser Teil bleibt frei, bis Verkauf oder Erbgang, bis 200 m² Wohnfläche; für den offenen Teil gilt die Hausregel</span></div>
          <div class="field"><label for="fl">Wohnfläche, in m²</label><input id="fl" type="number" min="0" step="5"><span class="hint">für die Hausregel: 60 m² für die erste Person, 20 m² für jede weitere; leer heißt: ganz innerhalb</span></div>''')
rep('const FELDER = ["kid6", "kid3", "lohn1", "std1", "lohn2", "std2", "rente", "kap", "miet",', 'const FELDER = ["kid6", "kid3", "lohn1", "std1", "lohn2", "std2", "rente", "kap", "miet", "fl",')
rep('const LEER = { erw: 1, kinder: 0,', 'const LEER = { fl: 0, erw: 1, kinder: 0,')
rep('miet: 12000, hb: 0.5, spar: 0.08', 'miet: 12000, hb: 0.5, fl: 120, spar: 0.08')
rep('miet: 18000, hb: 0.7, kinderlos: 1, spar: 0.35', 'miet: 18000, hb: 0.7, fl: 100, kinderlos: 1, spar: 0.35')
rep('eigenes Haus, beim Start zur Hälfte bezahlt.", v:', 'eigenes Haus mit 120 m², beim Start zur Hälfte bezahlt.", v:')
rep('Eigentumswohnung, beim Start zu 70 % bezahlt.", v:', 'Eigentumswohnung mit 100 m², beim Start zu 70 % bezahlt.", v:')

# Staatsseite: Plus aus der Hausregel Jahr für Jahr, Gesundheitsaufschlag
rep('  const hr = hausregelPfad(ny, miet), bon =', '''  const hr = hausregelPfad(ny, miet), hrp = hausregelPlus(hr), bon =''')
rep('      plus: A.AusgBonusPlus * bon + A.HRPlus * hr[i] + A.AusgRPPlus * rp + A.EPPlus * ep,\n      minus: rent + (1 - A.AusgBonusPlus) * bon + (1 - A.HRPlus) * hr[i] + (1 - A.AusgRPPlus) * rp + (1 - A.EPPlus) * ep });',
    '      plus: A.AusgBonusPlus * bon + hrp[i] + A.AusgRPPlus * rp + A.EPPlus * ep,\n      minus: rent + (1 - A.AusgBonusPlus) * bon + hr[i] - hrp[i] + (1 - A.AusgRPPlus) * rp + (1 - A.EPPlus) * ep });')
rep('function ausgleichPfad(ny, miet) {', '''// Nachtrag 21.11.2026: Teil der Hausregel bei Haushalten, die auch ohne sie mehr haben als heute (Mikrosimulation hrp zu hr), sonst HRPlus
function hausregelPlus(hr) { return A.UebMikro ? hr.map((x, i) => mikro("hr", i + 1) ? x * mikro("hrp", i + 1) / mikro("hr", i + 1) : 0) : hr.map(x => A.HRPlus * x); }
function ausgleichPfad(ny, miet) {''')
rep('function strassenfondsJ(k) {', '''// Nachtrag 21.11.2026: Gesundheitsaufschlag auf die Kilometerabgabe (Mrd. €, kommt beim Haushalt an), höchstens bis alle drei Aufschläge
// einen Benziner mit GAVerbrB kWh je 100 km GAMaxKm ct je km kosten
function gesundheitJ(k) {
  const i = Math.min(Math.max(k, 1), STRF.length) - 1, kwh = STRF_GA.kwh[i];
  if (!(kwh > 0)) return 0;
  const smax = Math.max(0, A.GAMaxKm / (A.GAVerbrB / 100) - STRF_GA.satz_d[i] - STRF_GA.satz_v2[i]);
  return A.SFAn * A.GAAn * Math.min(Math.max(0, STRF[i]), smax * kwh / 100);
}
function strassenfondsJ(k) {''')
rep(' - strassenfondsJ(y);   // Version 38', ' - strassenfondsJ(y) + gesundheitJ(y);   // Nachtrag 21.11.2026: Gesundheitsaufschlag; Version 38')

# Schuldenprognose: Lkw-Maut je nach Fall, Staat zuerst, Hälfte an alle erst, wenn der Kredit nicht mehr wächst
rep('    if (reform && k >= 1) pb += (saldoPfad[k - 1] ?? saldoPfad[saldoPfad.length - 1]) / A.BIP + c.pbx * Math.min(1, k / P.WachsJahre);',
    '    if (reform && k >= 1) pb += ((saldoPfad[k - 1] ?? saldoPfad[saldoPfad.length - 1]) - lkwFehlt(sz, y)) / A.BIP + c.pbx * Math.min(1, k / P.WachsJahre);   // Nachtrag 21.11.2026: Lkw-Maut je nach Fall')
a = s.index('function kreditPlan(rows, saldoPfad, ab, sz) {')
b = s.index('\n}\n', a) + 3
s = s[:a] + '''function kreditPlan(rows, saldoPfad, ab, sz) {
  // Nachtrag 21.11.2026 (Staat zuerst): Jedes Jahr tilgt den Kredit der größere Betrag, der Saldo der Reform (ohne das fehlende Mehr der
  // Lkw-Maut) oder der Überschuss des ganzen Staates nach der Hälfte an alle (ohne die Erträge der Chancen)
  const c = A.Prognose[sz]; let kr = 0, kmax = 0, jmax = 0, getilgt = null; const pfad = {};
  for (let k = 1; k <= 45; k++) {
    const y = 2027 + k, r = rows.find(q => q.jahr === y);
    let s = (saldoPfad[k - 1] ?? saldoPfad[saldoPfad.length - 1]) - lkwFehlt(sz, y);
    if (r) s = Math.max(s, (r.pb - r.aus) * A.BIP - chancenPb(c, y) * A.BIP);
    kr = Math.max(0, kr - s + (k === 1 ? 0 : kr * zinsJ(k))); pfad[y] = kr;
    if (kr > kmax) { kmax = kr; jmax = k; }
    if (kmax > 0 && kr === 0 && k > jmax) { getilgt = y; break; }
  }
  return { spitze: kmax, jahr: 2027 + jmax, getilgt, pfad };
}
// Nachtrag 21.11.2026: wächst der Kredit für den Übergang in einem Jahr ab ab?
const waechst = (pfad, ab) => Object.entries(pfad).some(([y, v]) => +y >= ab && v > (pfad[+y - 1] ?? 0) + 1e-9);
''' + s[b:]
rep('    const kb = kreditPlan(rows, pf, a, sz);\n    if (kb.spitze',
    '    const kb = kreditPlan(rows, pf, a, sz);\n    if (waechst(kb.pfad, a)) continue;   // Nachtrag 21.11.2026: die Hälfte an alle erst, wenn der Kredit nicht mehr wächst\n    if (kb.spitze')
# Register: Zeilen der Hausregel wie im Register des Buchs vom 21.11.2026 (Bezeichnung, Anzeige, Herleitung)
i = s.index('const REG = ') + 12
REG, n = json.JSONDecoder().raw_decode(s[i:])
for g in REG['g']:
    for r in g['r']:
        if r[0] in W['REG']:
            r[1], r[3], r[4] = W['REG'][r[0]]
s = s[:i] + json.dumps(REG, ensure_ascii=False, separators=(',', ':')) + s[i + n:]
open(p, 'w', encoding='utf-8').write(s)
print('Nachträge 21.11.2026 eingebaut')
