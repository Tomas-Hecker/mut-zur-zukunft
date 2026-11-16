#!/usr/bin/env python3
"""Steuerrechner, Staatsschulden: Im mittleren Fall (wahrscheinlichster Wert) wird die Spanne vom vorsichtigen bis zum
zuversichtlichen Fall als helles Band hinter die Hauptlinien gelegt, hellrot um „Ohne Reform“, hellgrün um „Mit Zukunftsplan“
(Gestaltungsregel von Tomas, 16.11.2026, 13:44, präzisiert 13:45).
Läuft nach gen.py. Ein zweiter Lauf ändert nichts."""
p = 'steuerrechner/index.html'
s = open(p, encoding='utf-8').read()
if 'planFall(' in s:
    raise SystemExit
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)

# 1) Linie mit Zukunftsplan und Schuldenregel für einen Fall, wie im mittleren Fall gerechnet
rep('let chartRows = null;', '''// Linie mit Zukunftsplan und Schuldenregel für einen anderen Fall (für das Band der Spanne)
function planFall(sz, pf) {
  let pl = prognose(sz, "regel", pf);
  if (pl[pl.length - 1].v > 0.0005) {
    let lo = 0, hi = 40, x = hi; for (let i = 0; i < 60; i++) { x = (lo + hi) / 2; const v = prognose(sz, "regel", pf, x).at(-1).v; if (v >= 0 && v <= 0.0005) break; if (v > 0) lo = x; else hi = x; }
    pl = prognose(sz, "regel", pf, Math.round(x * 1000) / 1000);
  }
  return pl;
}
let chartRows = null;''')
rep('''    reihen = mit.map((r, i) => ({ jahr: r.jahr, quote: r.v, ohne: ohne[i].v, plan: pl[i].v, mw: pl[i].mw }));''',
    '''    reihen = mit.map((r, i) => ({ jahr: r.jahr, quote: r.v, ohne: ohne[i].v, plan: pl[i].v, mw: pl[i].mw }));
    if (szenario === "mittel") { const pz = planFall("zuversichtlich", pf), pv = planFall("vorsichtig", pf); const oz = prognose("zuversichtlich", "ohne", pf), ov = prognose("vorsichtig", "ohne", pf); reihen.forEach((r, i) => { r.pz = pz[i] ? pz[i].v : r.plan; r.pv = pv[i] ? pv[i].v : r.plan; r.oz = oz[i] ? oz[i].v : r.ohne; r.ov = ov[i] ? ov[i].v : r.ohne; }); }''')

# 2) Achsen schließen das Band ein, Band hinter den Linien
rep('''  const maxY = Math.max(0.8, ...rows.map(r => Math.max(r.quote, r.ohne, hatDemo ? r.demo : 0))) * 1.05;''',
    '''  const maxY = Math.max(0.8, ...rows.map(r => Math.max(r.quote, r.ohne, hatDemo ? r.demo : 0, r.ov ?? 0, r.oz ?? 0, r.pv ?? 0, r.pz ?? 0))) * 1.05;''')
rep('''  const minY = Math.min(0, ...rows.map(r => hatPlan ? r.plan : 0));''',
    '''  const hatBand = hatPlan && rows[0].pz !== undefined;
  const minY = Math.min(0, ...rows.map(r => hatPlan ? Math.min(r.plan, hatBand ? r.pz : 0, hatBand ? r.pv : 0) : 0));''')
rep('''  const path = k => rows.map((r, i) => (i ? "L" : "M") + x(r.jahr).toFixed(1) + "," + yy(r[k]).toFixed(1)).join("");''',
    '''  const path = k => rows.map((r, i) => (i ? "L" : "M") + x(r.jahr).toFixed(1) + "," + yy(r[k]).toFixed(1)).join("");
  if (hatBand) {
    // Spanne vom vorsichtigen bis zum zuversichtlichen Fall: hellrot ohne Reform, hellgrün mit Zukunftsplan
    const pt = (r, k) => x(r.jahr).toFixed(1) + "," + yy(r[k]).toFixed(1);
    const band = (a, b) => "M" + rows.map(r => pt(r, a)).join("L") + "L" + rows.slice().reverse().map(r => pt(r, b)).join("L") + "Z";
    g += `<path d="${band("ov", "oz")}" style="fill:var(--bad);fill-opacity:.16;stroke:none"/><path d="${band("pv", "pz")}" style="fill:var(--good);fill-opacity:.2;stroke:none"/>`;
  }''')
# 3) Erklärung unter dem Bild
rep('''  drawChart(reihen);''', '''  if (szenario === "mittel") $("chartNote").textContent += " Die Linien zeigen den wahrscheinlichsten Verlauf. Das helle Band dahinter zeigt die Spanne vom vorsichtigen bis zum zuversichtlichen Fall, hellrot ohne Reform, hellgrün mit Zukunftsplan.";
  drawChart(reihen);''')
open(p, 'w', encoding='utf-8').write(s)
print('Band der Spanne eingebaut')
