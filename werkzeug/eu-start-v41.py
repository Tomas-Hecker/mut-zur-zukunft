#!/usr/bin/env python3
"""Nachträge vom 22.11.2026 zur Schuldenprognose im Steuerrechner (wie version-41/modell-v41/kette/schulden/zp19.py mit V41U und V41V):
- Start wie Bundesbank und EU-Kommission: der Primärsaldo ohne Reform ist je Fall so geeicht, dass die Schuldenquote 2024 bis 2028 die
  amtlichen Werte trifft; die höheren Ausgaben für Verteidigung gelten auch ohne Reform; Sondervermögen Infrastruktur 2029 bis 2036 mit
  0,7 % der Wirtschaftsleistung in beiden Pfaden; Schuldenregel ab 2035 kein Anstieg, ab 2050 höchstens 60 %; je Punkt Mehrwertsteuer
  steigen auch Grundsicherung, Bürgerjob, Rentenboden, Lernen und der Ausgleich (0,391 Mrd. € weniger netto).
- Klausel für die EU: Soweit Reform und Zukunftsplan den Primärsaldo gegenüber ohne Reform verschlechtern (gestundete Steuer zählt dabei
  nicht), deckt ein befristeter Zuschlag auf die Ausgabensteuer die Lücke; sein Ertrag zählt im Saldo der Reform.
Läuft nach start-stufen-v41.py. Ein zweiter Lauf ändert nichts."""
p = 'steuerrechner/index.html'
s = open(p, encoding='utf-8').read()
if 'Nachtrag 22.11.2026 (Start wie die EU)' in s:
    raise SystemExit
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)

GSPKT = 8.0 * 1010 / 31 / 1000 + 2.9 * 1010 / 31 / 1000 + 1.1 / 31
rep('const A = structuredClone(ANNAHMEN);', f'''// Nachtrag 22.11.2026 (Start wie die EU): Werte der Kette (v41/patch_v41u.py), Schuldenregel ab 2035 kein Anstieg, ab 2050 höchstens 60 %
Object.assign(ANNAHMEN.Prognose, {{ EU41: {{ ziele: {{ 2024: 0.622, 2025: 0.635, 2026: 0.643, 2027: 0.663, 2028: 0.689 }}, svik: 0.007, svikVon: 2029, svikBis: 2036, schwelle: 0.05, bis: 2060 }} }});
Object.assign(ANNAHMEN.Prognose.Plan, {{ RegelAb: 2035, RegelBis: 2050, RegelZiel: 0.60, NJP: 16.8 - {GSPKT!r} }});   // je Punkt steigen Grundsicherung, Bürgerjob, Rentenboden, Lernen und Ausgleich mit
const A = structuredClone(ANNAHMEN);''')

# gestundete Steuer auf den Mietwert am Start, für die Klausel der EU
rep('const ueb1 = uebergang(1, mietSt), bz1 = zulageBeamte(1), stund = stundungStart(mietSt);',
    'const ueb1 = uebergang(1, mietSt), bz1 = zulageBeamte(1), stund = stundungStart(mietSt); EU41.stundMiet0 = stund;   // Nachtrag 22.11.2026: für die Klausel der EU')

rep('function prognose(sz, fall, saldoPfad, fixPkt = 0, ab = null) {', '''// Nachtrag 22.11.2026 (Start wie die EU, zp19.py mit V41U und V41V): Eichung auf Bundesbank und Kommission, Verteidigung auch ohne Reform,
// Sondervermögen Infrastruktur, Klausel für die EU mit dem Zuschlag auf die Ausgabensteuer (Ertrag im Saldo der Reform)
const EU41 = { stundMiet0: 0, eich: null, stempel: "", kl: new Map() };
const dv41 = y => A.Prognose.DefMehr * clamp((y - A.Prognose.DefStart + 1) / A.Prognose.DefJahre, 0, 1);
function eu41Stempel() { return JSON.stringify([A.Prognose, A.Schuld, A.BIP, EU41.stundMiet0, A.AStundAn, A.Jahre]); }
function eu41Pruefen() {
  const st = eu41Stempel();
  if (st === EU41.stempel) return;
  EU41.stempel = st; EU41.kl = new Map(); EU41.eich = {};
  for (const sz of ["vorsichtig", "mittel", "zuversichtlich"]) {
    EU41.eich[sz] = {};
    for (const y of Object.keys(A.Prognose.EU41.ziele).map(Number).sort((a, b) => a - b)) {
      EU41.eich[sz][y] = 0;
      EU41.eich[sz][y] = A.Prognose.EU41.ziele[y] - prognose(sz, "ohne", [0]).find(r => r.jahr === y).v;
    }
  }
}
function euPb41(sz, y, reform) { let x = (EU41.eich[sz] || {})[y] || 0; if (y < A.Prognose.ReformStart || !reform) x += dv41(y); return x; }
// gestundete Steuer im Reformjahr k, die beim Defizit der EU nicht zählt: heutige Rentner (neu minus zurück) und Mietwert (linear bis null)
function euStund(k) {
  if (k < 1) return 0;
  const r = A.AStundAn && k <= ASTUND.neu.length ? ASTUND.neu[k - 1] - ASTUND.zur[k - 1] : 0;
  return r + EU41.stundMiet0 * Math.max(0, 1 - (k - 1) / A.Jahre);
}
// Saldo der Reform samt Ertrag des Zuschlags (Klausel für die EU), wie zp19.klausel41; mrd: Jahr → Ertrag in Mrd. €
function klausel41(sz, sal) {
  if (sal.kl41) return sal;
  eu41Pruefen();
  const key = sz + "|" + sal.map(x => x.toFixed(6)).join(",");
  if (EU41.kl.has(key)) return EU41.kl.get(key);
  const E = A.Prognose.EU41, S = A.Prognose.ReformStart;
  let cur = sal.slice(); cur.kl41 = true; cur.mrd = {};
  for (let runde = 0; ; runde++) {
    if (runde >= 8) throw new Error("Klausel für die EU: keine Ruhe nach 8 Runden (" + sz + ")");
    const rg = regelPlan(sz, cur);
    const rr = prognose(sz, "regel", cur, rg.fix, rg.ab), ro = prognose(sz, "ohne", cur);
    const pr = Object.fromEntries(rr.map(r => [r.jahr, r.pb])), po = Object.fromEntries(ro.map(r => [r.jahr, r.pb]));
    const neu = [];
    for (let y = S; y <= E.bis; y++) { const v = (pr[y] - po[y]) * A.BIP + euStund(y - S + 1); if (v < -E.schwelle) neu.push([y, -v]); }
    if (!neu.length) break;
    const nxt = cur.slice(); nxt.kl41 = true; nxt.mrd = { ...cur.mrd };
    for (const [y, m] of neu) { nxt.mrd[y] = (nxt.mrd[y] || 0) + m; nxt[y - S] += m; }
    cur = nxt;
  }
  EU41.kl.set(key, cur);
  return cur;
}
function prognose(sz, fall, saldoPfad, fixPkt = 0, ab = null) {
  eu41Pruefen();
  if (fall !== "ohne") saldoPfad = klausel41(sz, saldoPfad);   // Nachtrag 22.11.2026: mit dem Ertrag des Zuschlags''')
rep('    let pb = PB - Demo * (interp(y, P.Altern) - interp(P.Start, P.Altern));\n',
    '    let pb = PB - Demo * (interp(y, P.Altern) - interp(P.Start, P.Altern));\n    pb -= euPb41(sz, y, reform);   // Nachtrag 22.11.2026: Start wie Kommission, Verteidigung auch ohne Reform\n')
rep('    let dn = d * (1 + r) / (1 + nom) - pb + aus, need = 0;\n',
    '    let dn = d * (1 + r) / (1 + nom) - pb + aus, need = 0;\n    if (y >= P.EU41.svikVon && y <= P.EU41.svikBis) dn += P.EU41.svik;   // Nachtrag 22.11.2026: Sondervermögen Infrastruktur in beiden Pfaden\n')
rep('function regelPlan(sz, pf) {\n  const P = A.Prognose, k0 = kreditPlan([], pf, null, sz);',
    'function regelPlan(sz, pf) {\n  pf = klausel41(sz, pf);   // Nachtrag 22.11.2026: Saldo samt Ertrag des Zuschlags\n  const P = A.Prognose, k0 = kreditPlan([], pf, null, sz);')
# Text unter der Grafik: Start wie die EU, Schuldenregel, Zuschlag für den Start
rep('Die Schuldenregel: ab 2035 steigen die Schulden nicht mehr gegenüber dem Vorjahr, ab 2040 liegen sie nie über 63 % der Wirtschaftsleistung. Für den Kredit der ersten Jahre braucht es eine eigene Übergangsregel im Grundgesetz. Reicht der Plan nicht, steigt der Normalsatz der Mehrwertsteuer um die nötigen Punkte. Die höheren Ausgaben für Verteidigung (1,5 % der Wirtschaftsleistung) sind eingerechnet, bezahlt aus Kürzungen und dem Überschuss der Reform.',
    'Die Schulden starten wie in den Zahlen der Bundesbank und der Herbstprognose der EU-Kommission, mit dem Sondervermögen für die Infrastruktur. Die Schuldenregel: ab 2035 steigen die Schulden nicht mehr, gemessen an der Wirtschaftsleistung, ab 2050 liegen sie bei höchstens 60 %. Für den Kredit der ersten Jahre braucht es eine eigene Übergangsregel im Grundgesetz. Soweit die Regeln der EU ihn nicht zulassen, kommt 2028 und 2029 ein Zuschlag für den Start auf die Ausgabensteuer. Reicht der Plan nicht, steigt der Normalsatz der Mehrwertsteuer ab 2030 um einen festen Aufschlag. Die höheren Ausgaben für Verteidigung (1,5 % der Wirtschaftsleistung) sind mit und ohne Reform eingerechnet; mit Reform bezahlt aus Kürzungen und dem Überschuss.')
open(p, 'w', encoding='utf-8').write(s)
print('Nachtrag 22.11.2026 (Start wie die EU) eingebaut')
