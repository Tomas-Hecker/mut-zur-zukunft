#!/usr/bin/env python3
"""Schuldenprognose des Steuerrechners auf Buch Version 41 (wie schulden/kern19.py und zp19.py mit V37 bis V41, pfad39, regel39, kredit39).
Quelle: broschuere-mut-zur-zukunft/version-41/staat-schulden-umbau-v41.md (18.11.2026):
- Wachstum der Reform 1,4707 / 6,85 / 19,1075 % nach 20 Jahren, KI-Sockel 2027 bis 2041 und autonomes Fahren 2030 bis 2049 mit und ohne Reform,
  der alte KI-Schub ist aus; Chancen für alle (Wachstum und Erträge) im Zukunftsplan.
- Regel für den Überschuss: ab dem Jahr ab geht die Hälfte des Primärüberschusses als Entlastung an alle (höherer Freibetrag), nach der
  Schuldenfreiheit dazu der Ertrag des Fonds nach Inflation, mit Rückwirkung über den Einkauf; gerechnet bis 2100.
- ab ist das erste Jahr ab 2030, mit dem die Schuldenregel ohne Aufschlag auskommt und der Kredit für den Übergang nicht größer wird;
  sonst ein fester Aufschlag ab 2030, so dass die Schuldenregel keine weiteren Punkte braucht (vorsichtig 6,334).
- Kredit für den Übergang wie kredit39: ab dem ersten Jahr ab ab mit Primärüberschuss tilgt der Überschuss des Staates nach der Entlastung.
Läuft nach kern-v41.py. Ein zweiter Lauf ändert nichts."""
import re
p = 'steuerrechner/index.html'
s = open(p, encoding='utf-8').read()
if 'Prognose Version 41' in s:
    raise SystemExit
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)

rep('const A = structuredClone(ANNAHMEN);', '''// Prognose Version 41 (wie schulden/kern19.py und zp19.py mit V41=J): Wachstum der Reform ohne Kitas und Forschung, KI-Sockel und autonomes
// Fahren mit und ohne Reform (je Grundszenario), Chancen für alle im Zukunftsplan, Hälfte des Überschusses für alle ab dem Jahr ab
Object.assign(ANNAHMEN.Prognose.vorsichtig, { wachs: 0.014706719558586974, ki: 0, chancen: 0.48148148148148145, sockel: 0.0005, auto: 0 });
Object.assign(ANNAHMEN.Prognose.mittel, { wachs: 0.0685, ki: 0, chancen: 1, sockel: 0.0035, auto: 0.005 });
Object.assign(ANNAHMEN.Prognose.zuversichtlich, { wachs: 0.191075, ki: 0, chancen: 1.8518518518518519, sockel: 0.01, auto: 0.01 });
Object.assign(ANNAHMEN.Prognose, { Bis: 2100, Real: 0.03, AbVon: 2030, AbBis: 2070, SockelJahre: [2027, 2041], AutoJahre: [2030, 2049],
  CHANCEN: { staat: 0.4, schul: 0.0068, schulAb: 5, schulJahre: 45, schulExp: 1.85, ment: 0.00072, mentAb: 4, mentJahrgaenge: 16, mentMax: 45,
    absch: 0.00073, abschJahre: 10, lesen: 0.00022, lesenJahre: 10, werk: 0.00012, werkJahre: 20 } });
const A = structuredClone(ANNAHMEN);''')

NEU = r'''// Version 37: Chancen für alle, mehr Wirtschaftsleistung im mittleren Fall (kern19.py: chancen_w, chancen_niveau, chancen_gr, chancen_pb)
function chancenW(y) {
  const C = A.Prognose.CHANCEN, t = y - A.Prognose.ReformStart;
  if (!A.ChAn || t <= 0) return 0;
  return C.schul * Math.max(0, Math.min(1, (t - C.schulAb) / C.schulJahre)) ** C.schulExp + C.ment / C.mentJahrgaenge * Math.max(0, Math.min(t - C.mentAb, C.mentMax))
    + C.absch * Math.min(1, t / C.abschJahre) + C.lesen * Math.min(1, t / C.lesenJahre) + C.werk * Math.min(1, t / C.werkJahre);
}
const chancenNiveau = (c, y) => (c.chancen ?? 1) * chancenW(y);
const chancenGr = (c, y) => chancenNiveau(c, y) - chancenNiveau(c, y - 1);
const chancenPb = (c, y) => A.Prognose.CHANCEN.staat * chancenNiveau(c, y);
// Staatsschulden in % des BIP, 2023 bis 2100 (wie zp19.pfad39): fall = "ohne" | "reform" | "plan" | "regel"; ab: Jahr, ab dem die Hälfte des
// Überschusses an alle geht (null: erst nach der Schuldenfreiheit); fixPkt: fester Aufschlag auf den Normalsatz ab 2030 (nur regel)
function prognose(sz, fall, saldoPfad, fixPkt = 0, ab = null) {
  const P = A.Prognose, Q = P.Plan, c = P[sz];
  const reform = fall !== "ohne", plan = fall === "plan" || fall === "regel", regel = fall === "regel";
  const PB = [P.PBG, P.PBU, (P.PBG + P.PBU) / 2][c.grund - 1];
  const Demo = [P.DemoG, P.DemoU, (P.DemoG + P.DemoU) / 2][c.grund - 1];
  const alpha = A.VhEntlPlus, ps = A.VhPlusSofort, njp = Q.NJP - A.FBKoppMrd * A.FBKopp / 32;
  const cim = alpha * A.VhSteuerM * ps + (1 - alpha) * A.VhSteuerW * A.VhMinusSofort;
  let d = A.Schuld, dprev = d, nprev = 0, g = P.TBZins0, b = Q.AusgBasis, ang = 0, ruhe = 0, fehl = 0;
  const out = [{ jahr: P.Start, v: d, mw: 0, pb: 0, aus: 0, netto: 0, brutto: 0 }];
  for (let y = P.Start + 1; y <= P.Bis; y++) {
    const zNeu = plan && Q.ZinsR != null && y >= P.ReformStart ? Q.ZinsStart + (Q.ZinsR - Q.ZinsStart) * Math.min(1, (y - P.ReformStart) / Q.ZinsJahre) : interp(y, P.ZinsNeu);
    g = g + (zNeu - g) / P.TBLaufzeit;
    const wG = interp(y, P.WachsG), wU = interp(y, P.WachsU);
    let gr = [wG, wU, (wG + wU) / 2][c.grund - 1];
    if (y >= P.SockelJahre[0] && y <= P.SockelJahre[1]) gr += c.sockel || 0;   // Version 41: KI-Schub, mit und ohne Reform
    if (y >= P.AutoJahre[0] && y <= P.AutoJahre[1]) gr += (c.auto || 0) / (P.AutoJahre[1] - P.AutoJahre[0] + 1);   // autonomes Fahren
    if (reform && y >= P.ReformStart && y < P.ReformStart + P.WachsJahre) gr += c.wachs / P.WachsJahre;
    if (c.ki && y >= P.KI.von && y < P.KI.von + P.KI.jahre) gr += P.KI.dg;
    if (plan && y >= 2030 && y < 2045) gr += c.bild / 15;
    if (plan && y >= 2028 && y < 2048) gr += c.binnen / 20;
    if (plan) gr += kifoGr(c, y) + chancenGr(c, y);   // Kitas und Forschung, Chancen für alle
    const nom = (1 + gr) * (1 + P.Infl) - 1;
    let pb = PB - Demo * (interp(y, P.Altern) - interp(P.Start, P.Altern));
    const k = y - P.ReformStart + 1;
    if (reform && k >= 1) pb += (saldoPfad[k - 1] ?? saldoPfad[saldoPfad.length - 1]) / A.BIP + c.pbx * Math.min(1, k / P.WachsJahre);
    if (plan) {
      pb += Q.Rente * ramp(y, 2031, 2070) + Q.Ges * ramp(y, 2027, 2035) + 0.005 * ramp(y, 2030, 2045) + (Q.Verw ?? 10.7) / A.BIP * ramp(y, 2028, 2043) + (y >= 2032 ? 1.0 / A.BIP : 0) + 0.4 * c.bild * ramp(y, 2030, 2045);
      if (y >= 2030 && (d > Q.AusgBis || d > dprev + 1e-9 || nprev > 1e-9)) b = Math.max(Q.AusgBasis - Q.AusgMax, b * (1 + P.Infl) / (1 + nom));
      pb += Q.AusgBasis - b + Q.Subv * ramp(y, 2028, 2031) + c.ern * ramp(y, 2030, 2050);
      pb += kifoPb(c, y) + chancenPb(c, y);
    }
    // Verteidigung (1,5 % des BIP) aus Kürzungen und dem Überschuss der Reform (Blatt Sicherheit)
    if (reform && y >= P.ReformStart) pb -= Math.max(0, P.DefMehr * clamp((y - P.DefStart + 1) / P.DefJahre, 0, 1) - (A.SicherheitWerte.SubvAbbau + A.SecAuto * A.AutoKost + A.SecGruend * A.Gruend + A.SecFH * A.FinHilfen * ramp(y, 2028, 2031)) / A.BIP);
    if (regel && fixPkt > 0 && y >= Q.FixAb) pb += fixPkt * njp / A.BIP;   // fester Aufschlag auf den Normalsatz
    if (plan) pb += ((A.VhSteuerR * A.VhAusRuhe + A.VhStaatM * A.VhErbM) * ruhe + (A.VhSteuerW * A.VhMinusSpaeter + A.VhStaatW * A.VhErbW) * fehl) / A.BIP;   // Rückwirkung früherer Entlastung
    const r = (d > 0 || !plan) ? g : Q.Rendite;
    let aus = 0;
    if (plan && d <= 0) aus = -d * P.Real * (1 + P.Infl) / (1 + nom);   // Ertrag des Fonds nach Inflation
    if (plan && (d <= 0 || (ab !== null && y >= ab)) && Q.Ueb > 0 && pb > 0) aus += Q.Ueb * pb;   // Hälfte des Überschusses für alle
    let dn = d * (1 + r) / (1 + nom) - pb + aus, need = 0;
    if (regel && y >= Q.RegelAb) { const tgt = y < Q.RegelBis ? Math.max(Q.RegelZiel, d) : Q.RegelZiel; if (dn > tgt) { need = dn - tgt; dn = tgt; } }
    const netto = aus * A.BIP, brutto = netto / (1 - cim);
    if (plan) { const u = ang / A.VhJahreRuhe; [ang, ruhe, fehl] = [ang + (1 - ps) * alpha * brutto - u, ruhe + u - (A.VhAusRuhe + A.VhStaatM * A.VhErbM) * ruhe, fehl + (1 - A.VhMinusSofort) * (1 - alpha) * brutto - (A.VhMinusSpaeter + A.VhErbW) * fehl]; }
    dprev = d; nprev = need; d = dn;
    out.push({ jahr: y, v: d, mw: need * A.BIP / njp + (regel && y >= Q.FixAb ? fixPkt : 0), pb, aus, netto, brutto });
  }
  return out;
}
// Kredit für den Übergang (wie zp19.kredit39): bis zum ersten Jahr ab ab mit Primärüberschuss wächst er mit dem Saldo der Reform,
// danach tilgt ihn der Überschuss des Staates nach der Entlastung (ohne die Erträge der Chancen)
function kreditPlan(rows, saldoPfad, ab, sz) {
  const c = A.Prognose[sz]; let kr = 0, kmax = 0, jmax = 0, getilgt = null, an = false;
  for (let k = 1; k <= 45; k++) {
    const y = 2027 + k, r = rows.find(q => q.jahr === y);
    if (ab !== null && y >= ab && !an) an = r.pb > 0;
    const s = an ? Math.max(0, (r.pb - r.aus) * A.BIP - chancenPb(c, y) * A.BIP) : saldoPfad[k - 1] ?? saldoPfad[saldoPfad.length - 1];
    kr = Math.max(0, kr - s + (k === 1 ? 0 : kr * zinsJ(k)));
    if (kr > kmax) { kmax = kr; jmax = k; }
    if (kmax > 0 && kr === 0 && k > jmax) { getilgt = y; break; }
  }
  return { spitze: kmax, jahr: 2027 + jmax, getilgt };
}
const punkte = (rows, fix = 0) => rows.reduce((m, r) => Math.max(m, r.mw - (r.jahr >= 2030 ? fix : 0)), 0);
// Beginn der Entlastung, fester Aufschlag und Kredit je Szenario (wie zp19.regel39)
function regelPlan(sz, pf) {
  const P = A.Prognose, k0 = kreditPlan([], pf, null, sz);
  for (let a = P.AbVon; a <= P.AbBis; a++) {
    const rows = prognose(sz, "regel", pf, 0, a);
    if (punkte(rows) > 0.005) continue;
    const kb = kreditPlan(rows, pf, a, sz);
    if (kb.spitze <= k0.spitze + 0.05) return { ab: a, fix: 0, rows, kredit: kb };
  }
  let fix = 0;
  if (punkte(prognose(sz, "regel", pf)) > 0.005) {
    let lo = 0, hi = 40;
    for (let i = 0; i < 50; i++) { const m = (lo + hi) / 2; if (punkte(prognose(sz, "regel", pf, m), m) <= 0.005) hi = m; else lo = m; }
    fix = Math.round(hi * 1000) / 1000;   // wie zp19.json und die Linie des Buchs (variante_b28.py)
  }
  const rows = prognose(sz, "regel", pf, fix);
  return { ab: null, fix, rows, kredit: kreditPlan(rows, pf, null, sz) };
}
// Freibetrag im Monat aus der Entlastung bei gleichem Einkauf (brutto), wie variante_b28.entlastung: bis 1.500 €, darüber sinkt der Satz
const fbStart = () => (A.Grenze1 + A.GFB) / 12;
const freibetragMonat = brutto => Math.round(Math.min(1500, fbStart() + Math.max(0, brutto) / A.FBJeEuro));
const schuldenfreiJahr = rows => (rows.find(r => r.jahr >= 2030 && Math.round(r.v * 1000) / 10 <= 0.05) || {}).jahr ?? null;
'''
i = s.index('function prognose(sz, fall, saldoPfad, fixPkt = 0) {')
j = s.index('\n/* ===================== Darstellung', i)
s = s[:i] + NEU + s[j:]

# Szenarien in updateGesamt: Regel des Buchs mit Entlastung, Kredit und Freibetrag
a = s.index('    const mit = prognose(szenario, "reform", pf), ohne = prognose(szenario, "ohne", pf);')
b = s.index('    reihen = mit.map((r, i) =>', a)
s = s[:a] + '''    const mit = prognose(szenario, "reform", pf), ohne = prognose(szenario, "ohne", pf);
    regelAkt = regelPlan(szenario, pf); fixAuf = Math.round(regelAkt.fix * 1000) / 1000;
    const pl = regelAkt.rows;
''' + s[b:]
rep('    reihen = mit.map((r, i) => ({ jahr: r.jahr, quote: r.v, ohne: ohne[i].v, plan: pl[i].v, mw: pl[i].mw }));',
    '''    reihen = mit.map((r, i) => ({ jahr: r.jahr, quote: r.v, ohne: ohne[i].v, plan: pl[i].v, mw: pl[i].mw, brutto: pl[i].brutto })).filter(r => r.jahr <= 2070);
    reihen.frei = schuldenfreiJahr(pl);''')
rep('let fixAuf = 0;', 'let fixAuf = 0, regelAkt = null;')
# Band: andere Fälle mit derselben Regel
a = s.index('function planFall(sz, pf) {')
b = s.index('\n}\n', a) + 3
s = s[:a] + 'function planFall(sz, pf) { return regelPlan(sz, pf).rows; }\n' + s[b:]

# Kacheln
rep('''    const frei = reihen.find(r => r.jahr >= A.Prognose.ReformStart && r.plan <= 1e-9);
    t += tile("Staatsschulden 2070", sq(e.plan), `${frei ? "schuldenfrei " + frei.jahr + ", " : ""}mit Zukunftsplan; ohne Reform ${sq(e.ohne)}`, e.plan < e.ohne ? "good" : "bad");''',
    '''    const frei = reihen.frei;
    t += tile("Staatsschulden 2070", sq(e.plan), `${frei ? "schuldenfrei " + frei + ", " : ""}mit Zukunftsplan; ohne Reform ${sq(e.ohne)}`, e.plan < e.ohne ? "good" : "bad");
    const fbAt = j => freibetragMonat((reihen.find(r => r.jahr === j) || {}).brutto || 0), erst = reihen.find(r => r.brutto > 0.005);
    t += tile("Freibetrag", erst ? `${eur(fbAt(2045))} im Monat 2045` : eur(fbStart()) + " im Monat",
      erst ? `Ab ${erst.jahr} geht die Hälfte des Überschusses an alle zurück: der Freibetrag steigt von ${eur(fbStart())}, 2070 auf ${eur(fbAt(2070))} (heutige Preise)` : `Bis 2070 bleibt kein Überschuss, der an alle zurückgehen kann.`, erst ? "good" : "");''')
rep('rund ${fmt(fixMrd(fixAuf), 1)} Mrd. € im Jahr; so sind die Schulden 2070 bei null`',
    'rund ${fmt(fixMrd(fixAuf), 1)} Mrd. € im Jahr; so hält der Staat die Schuldenregel ein`')
rep('function fixMrd(x) { return x * (A.Prognose.Plan.NJP - A.FBKoppMrd * A.FBKopp / 32); }',
    'function fixMrd(x) { return x * (A.Prognose.Plan.NJP - A.FBKoppMrd * A.FBKopp / 32); }   // Version 41: 16,8 − 2,0 = 14,8 Mrd. € je Punkt')
# Kredit für den Übergang: in den Szenarien wie im Buch (mit Zukunftsplan), in der einfachen Rechnung wie das Blatt Kredit
rep('  t += tilg;', '''  t += tilg;
  const tilgIdx = t.length - tilg.length;''')
rep('  $("tiles").innerHTML = t;', '''  if (regelAkt && szenario !== "basis" && !kr.unendlich) {
    const kp = regelAkt.kredit;
    const neu = kp.spitze <= 0.05 ? tile("Kredit für den Übergang", "keiner", "Das System trägt sich von Anfang an.", "good")
      : tile("Kredit für den Übergang", `${mrd(kp.spitze, 0)} Mrd. €`, `höchstens, Ende ${kp.jahr}; ${kp.getilgt ? "getilgt " + kp.getilgt : "bis 2072 nicht getilgt"}; danach tilgt der Überschuss nach der Hälfte für alle`, kp.getilgt && kp.getilgt - 2027 <= 30 ? "good" : "bad");
    t = t.slice(0, tilgIdx) + neu + t.slice(tilgIdx + tilg.length);
  }
  $("tiles").innerHTML = t;''')
# Titel der Grafik: schuldenfrei auch nach 2070
rep('  const frei = hatPlan ? rows.find(r => r.jahr >= A.Prognose.ReformStart && r.plan <= 1e-9) : rows.find(r => r.jahr >= A.Prognose.ReformStart && r.quote <= 1e-9);',
    '  const frei = hatPlan ? (rows.frei ? { jahr: rows.frei } : null) : rows.find(r => r.jahr >= A.Prognose.ReformStart && r.quote <= 1e-9);')
rep('`Mit der Reform ist der Staat ${frei.jahr} schuldenfrei, ohne Reform steigen die Schulden auf ${pct(last.ohne, 0)}`',
    '`Mit der Reform ist der Staat ${frei.jahr} schuldenfrei, ohne Reform steigen die Schulden bis 2070 auf ${pct(last.ohne, 0)}`')
open(p, 'w', encoding='utf-8').write(s)
print('Schuldenprognose auf Version 41')
