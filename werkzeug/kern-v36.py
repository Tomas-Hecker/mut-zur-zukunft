#!/usr/bin/env python3
"""Steuerrechner: Staatsseite auf den Rechenkern Version 36 (modell-v36/modell_2_5_gesamtpaket_kern.py, Stand 16.11.2026),
nach staat-rechner-umbau-v36.md vom Buch. Neue und geänderte Annahmen, Übergangsregeln Jahr für Jahr aus der eigenen Mikrosimulation
(MIKRO, UebMikro), Stufe 4 aus der Mikrosimulation (S4Mikro), Freibetrag über FBGesamt (FBJeEuro), Lohnersatz, übrige Erben 60 %,
Plastik, Pestizide, Flug, Neuwagen in Stufen, Bürgerjob offen für alle, Rente +4 %, Stundung, Erziehung und Pflege als Bürgerjob.
Die Werte stehen in kern-v36-werte.json (aus dem Rechenkern gezogen). Läuft nach v36-vorab.py. Ein zweiter Lauf ändert nichts."""
import json, os
p = 'steuerrechner/index.html'
s = open(p, encoding='utf-8').read()
if 'Rechenkern Version 36' in s:
    raise SystemExit
W = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kern-v36-werte.json'), encoding='utf-8'))
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)

rep('const A = structuredClone(ANNAHMEN);', '''// Rechenkern Version 36 (Staatsseite): neue und geänderte Annahmen aus modell-v36 (Stand 16.11.2026)
Object.assign(ANNAHMEN, @A@);
// Version 36: Übergangsregeln Jahr für Jahr aus der eigenen Mikrosimulation, Mrd. € in heutigen Preisen, 2028 bis 2072 (MIKRO im Rechenkern)
const MIKRO = @M@;
const mikro = (key, k) => { const L = MIKRO[key]; return k > 0 && k <= L.length ? L[k - 1] : 0; };
// Stundung der Ausgabensteuer für heutige Rentner: neu gestundet und zurück, Mrd. € je Reformjahr (eigene Mikrosimulation)
const ASTUND = @S@;
const A = structuredClone(ANNAHMEN);'''.replace('@A@', json.dumps(W['A'], ensure_ascii=False)).replace('@M@', json.dumps(W['MIKRO'])).replace('@S@', json.dumps(W['ASTUND'])))

# abgeleitet: Raster der Hochrechnung und Anteil, der vom Plus sofort ausgegeben wird
rep('''  A.DaemL = A.HKL = A.EigL = A.AntL;''', '''  A.DaemL = A.HKL = A.EigL = A.AntL;
  A.Grenze1G = 12 * A.FBGesamt - A.GFB; A.Grenze2G = A.Grenze2 - (A.Grenze1 - A.Grenze1G);   // Version 36: Raster mit FBGesamt
  const _g = ["GS", "30", "60", "100", "Ueber", "Rent"];   // Version 35: Sparquote nach Einkommen, gewichtet mit dem Plus je Gruppe
  A.VhPlusSofort = 1 - _g.reduce((a, k) => a + A["VhSpar" + k] * A["VhGew" + k], 0) / _g.reduce((a, k) => a + A["VhGew" + k], 0);''')

# Stufe 4: Höhe aus der Mikrosimulation, Anstieg aus der Hochrechnung (s4_werte); Freibetrag über FBGesamt; übrige Erben
rep('''  if (A.Stufe4Jahre > 0) { const a0 = stufe4(false), am = stufe4(true) - a0; s4 = [a0 + am * (1 - A.Stundung), a0 + am]; }''',
    '''  if (A.Stufe4Jahre > 0) { const a0 = stufe4(false), am = stufe4(true) - a0; s4 = [a0 + am * (1 - A.Stundung), a0 + am]; if (A.S4Mikro > 0) s4 = [A.S4Mikro, A.S4Mikro * s4[1] / s4[0]]; }
  const fbPlus = (A.Grenze1 - A.Grenze1G) / 12 * A.FBJeEuro;   // Version 36: Freibetrag über FBGesamt (fb_plus)
  const erbAnd = lang => { const d = Math.max(0, A.ErbAnteilAnd - erbQuote()); return A.ErbVol * A.ErbBasis * (1 - A.FamAnteil - A.EheAnteil) * (1 - A.AndFreiQ) * d * (lang ? A.RealLang : A.RealStart) * (1 + A.J3An * A.Satz3 / (1 + A.Satz3)); };''')
# Bürgerjob offen für alle, Fahrkarte und Kleidung, Sprache, Erziehung und Pflege im Bürgerjob
rep('''- A.BJheuteTn * A.BJheute / 1000 - A.BJVerw + A.BJAnr);''',
    '''- A.BJheuteTn * A.BJheute / 1000 - A.BJVerw + A.BJAnr
    + A.BJOfTn * (A.BJOfStd * 52 * A.BJML + A.BJAnl * A.BJOfStd / 20) / 1000 + (A.BJTn * (A.BJArb ?? 1) + A.BJOfTn) * A.BJKdA / 1000
    + (A.SprTn * A.SprHandy + (A.SprIKTn * A.SprIKUE + A.SprBSKTn * A.SprBSKUE) * A.SprKES) / 1000 + A.BJErzPfl * (A.BJPlus || 0) / 1000);''')
rep('const kasse = A.KVPausch - A.KVBZ - A.BGKV + A.ExMinPraem,', 'const kasse = A.KVPausch - A.KVBZ - A.BGKV + A.ExMinPraem + A.KVJung,')
rep('''["Neuwagen: Mehrwertsteuer auf die ersten 10.000 € eines Elektroautos erstattet", A.AutoKost * (A.Sicherheit ? 1 - A.SecAuto : 1), A.AutoKost * (A.Sicherheit ? 1 - A.SecAuto : 1)],''',
    '''["Neuwagen: Mehrwertsteuer auf die ersten 10.000 € eines Elektroautos erstattet, weniger, je mehr Elektroautos verkauft werden", A.AutoKost * A.AutoStufeS * (A.Sicherheit ? 1 - A.SecAuto : 1), A.AutoKost * A.AutoStufeL * (A.Sicherheit ? 1 - A.SecAuto : 1)],''')
rep('''["Ausgleichszulage für heutige Beamte und Pensionäre (schmilzt ab)", A.BeamtAusgl, 0],''', '''["Ausgleichszulage für heutige Beamte und Pensionäre (schmilzt ab)", bz1, 0],''')
rep('''    ["Altvermögenskonto: versteuertes Erspartes bleibt frei (läuft in " + fmt(A.AVKJahre) + " Jahren aus)", A.AltUeb, 0],''',
    '''    ["Lohnersatz vom neuen Lohn: Arbeitslosengeld, Krankengeld, Elterngeld, Wohngeld und weitere", A.LohnErs, A.LohnErs],
    [`Freibetrag ${eur((A.Grenze1 + A.GFB) / 12)} statt ${eur(A.FBGesamt)} im Monat (eigene Mikrosimulation)`, fbPlus, fbPlus],
    ["Altvermögenskonto: versteuertes Erspartes bleibt frei, mit Obergrenze (läuft aus)", nr1.avk, 0],''')
rep('''    ["Dienstwagen: private Nutzung an der Quelle besteuert", A.DienstwE, A.DienstwE],''', '''    ["Dienstwagen: private Nutzung an der Quelle besteuert", A.DienstwE, A.DienstwE],
    ["Plastik ohne Recycling: die Abgabe an die EU zahlen Hersteller und Importeure", A.PlastikE, A.PlastikE],
    ["Abgabe auf Pflanzenschutzmittel nach ihrem Risiko", A.PestizidE, A.PestizidE],
    ["Luftverkehrsteuer: die Senkung vom 1. Juli 2026 zurückgenommen", A.FlugE, A.FlugE],''')
rep('''    ["Erbe nach dem Staatsanteil gilt als versteuert (Altvermögenskonto)", -erbJ3(false), -erbJ3(true)],''', '''    ["Erbe nach dem Staatsanteil gilt als versteuert (Altvermögenskonto)", -erbJ3(false), -erbJ3(true)],
    [`Übrige Erben: Staatsanteil ${pct(A.ErbAnteilAnd, 0)} über ihrem Freibetrag`, erbAnd(false), erbAnd(true)],''')

# Übergangsregeln Jahr für Jahr aus der Mikrosimulation
rep('''  const n = k - 1, fr = freiAnteil(n, [A.HFR10, A.HFR20, A.HFR30]), fe = freiAnteil(n, [A.HFE10, A.HFE20, A.HFE30, A.HFE40]);''',
    '''  if (A.UebMikro) return { hf: A.HausFrei * mikro("hf", k) * miet / A.MikroMietSt, bs: A.BSAn * mikro("bs", k) };   // Version 36
  const n = k - 1, fr = freiAnteil(n, [A.HFR10, A.HFR20, A.HFR30]), fe = freiAnteil(n, [A.HFE10, A.HFE20, A.HFE30, A.HFE40]);''')
rep('''  const avk = A.AltUeb * Math.max(0, 1 - (k - 1) / A.AVKJahre);''', '''  const avk = A.UebMikro ? A.AVKGrenzeF * mikro("avk", k) : A.AltUeb * Math.max(0, 1 - (k - 1) / A.AVKJahre);   // Version 36''')
rep('''const zulageBeamte = k => A.BeamtAusgl * Math.max(0, 1 - (k - 1) / A.BZJahre) ** 3;''', '''const zulageBeamte = k => A.UebMikro ? mikro("zul", k) : A.BeamtAusgl * Math.max(0, 1 - (k - 1) / A.BZJahre) ** 3;''')
rep('''function hausregelPfad(ny) {
''', '''function hausregelPfad(ny, miet) {
  if (A.UebMikro) return Array.from({ length: ny }, (_, i) => A.HRAn * mikro("hr", i + 1) * miet / A.MikroMietSt);   // Version 36
''')
# Ausgleich: Rente +4 % aus der Mikrosimulation, Stundung, Erziehung und Pflege als Bürgerjob (ausgleich_pfad)
rep('''function ausgleichPfad(ny) {
  const hr = hausregelPfad(ny),''', '''// Version 35, Teil 8: Erziehung und Pflege als Bürgerjob für alle (ep_pfl, ep_kosten, erzpfl im Rechenkern)
function epPfl(jahr) { const y = Math.min(jahr, 2070); return y <= 2055 ? A.EPPfl2021 + (A.EPPfl2055 - A.EPPfl2021) * (y - 2021) / (2055 - 2021) : A.EPPfl2055 + (A.EPPfl2070 - A.EPPfl2055) * (y - 2055) / (2070 - 2055); }
function epKosten() {
  const L = A.EPLohn, geb = A.FamGeb * 1e6;
  const monate = geb * 12 * ((1 - A.EPKrippe0) + (1 - A.EPKrippe1) + (1 - A.EPKrippe2)) * (1 - A.EPGeschw);
  const eltern = (monate - A.EPGSElt * 12) * L - (geb * A.EPEGQuote * (A.EPEG - A.EPEGUeber) - A.EPGSElt * A.EPGSEltEG * 12 * A.EPEGMin);
  const je = [2, 3, 4, 5].reduce((a, g) => a + A["EPPG" + g] * Math.max(0, (g === 2 ? A.EPLohnPG2 : 1) * L - A.EPPGeldAnt * A["EPPGeld" + g]), 0);
  return [eltern / 1e9, (A.EPPflP * 1e6 - A.EPGSPfl) * je * 12 / 1e9];
}
function erzPfl(jahr) { if (!A.EPAn || jahr < A.EPAb) return 0; const [e, p] = epKosten(); return e + p * epPfl(jahr) / epPfl(A.Prognose.ReformStart); }
function ausgleichPfad(ny, miet) {
  const hr = hausregelPfad(ny, miet),''')
rep('''    const rent = A.AusgAn * A.AusgRent0 * rentnerAnteil(i) + (A.AusgRPAn || 0) * A.AusgRP0 * rpAnteil(i);
    out.push({ rentner: rent, bonus: bon, haus: hr[i], sparen: sp, plus: A.AusgBonusPlus * bon + A.HRPlus * hr[i], minus: rent + (1 - A.AusgBonusPlus) * bon + (1 - A.HRPlus) * hr[i] });''',
    '''    const rent = A.AusgAn * A.AusgRent0 * rentnerAnteil(i);
    const rp = (A.AusgRPAn || 0) * (A.UebMikro ? mikro("rplus", i + 1) : A.AusgRP0 * rpAnteil(i));   // Rente +4 % für heutige Rentner
    const st = A.AStundAn && i < ASTUND.neu.length ? ASTUND.neu[i] - ASTUND.zur[i] : 0;   // Stundung: was der Kasse fehlt
    const ep = erzPfl(jahr);   // Erziehung und Pflege als Bürgerjob, aus dem Überschuss
    out.push({ rentner: rent, bonus: bon, haus: hr[i], sparen: sp, rplus: rp, stund: st, erzpfl: ep,
      plus: A.AusgBonusPlus * bon + A.HRPlus * hr[i] + A.AusgRPPlus * rp + A.EPPlus * ep,
      minus: rent + (1 - A.AusgBonusPlus) * bon + (1 - A.HRPlus) * hr[i] + (1 - A.AusgRPPlus) * rp + (1 - A.EPPlus) * ep });''')
rep('''  const ag = ausgleichPfad(ny), vh = verhalten(steuer, ag);
  const gleich = steuer.map((x, i) => x - ag[i].rentner - ag[i].bonus - ag[i].haus + ag[i].sparen);''',
    '''  const ag = ausgleichPfad(ny, miet), vh = verhalten(steuer, ag);
  const gleich = steuer.map((x, i) => x - ag[i].rentner - ag[i].bonus - ag[i].haus + ag[i].sparen - ag[i].rplus - ag[i].stund - ag[i].erzpfl);''')
rep('''      + (y <= A.Stufe4Jahre ? s4[0] + (s4[1] - s4[0]) * (y - 1) / A.Jahre : 0));''',
    '''      + (y <= A.Stufe4Jahre ? s4[0] + (s4[1] - s4[0]) * Math.min(1, (y - 1) / A.Jahre) : 0));   // Version 36: dauerhaft, nach der Übergangsphase gleich''')
# Saldo bei gleichem Einkauf ohne Ausgleich: mit der dauerhaften Stufe 4 (Blatt Kredit, Spalte Z), sonst wirkt der Start viel schlechter
rep('const ohneA = `Bei gleichem Einkauf und ohne Ausgleich wären es ${mrd(g.saldoS)} Mrd. €.`;',
    'const ohneA = `Bei gleichem Einkauf und ohne Ausgleich wären es ${mrd(g.saldoS + (A.Stufe4Jahre >= 99 ? g.s4[0] : 0))} Mrd. €.`;')
# Saldo langfristig mit der dauerhaften Stufe 4 (staat-v36.json: 249,6 Mrd. €)
rep('t += tile("Saldo langfristig", mrd(g.saldoL) + " Mrd. €", `${pct(g.saldoL / A.BIP, 1)} des BIP,',
    'const sL4 = g.saldoL + (A.Stufe4Jahre >= 99 ? g.s4[1] : 0);\n  t += tile("Saldo langfristig", mrd(sL4) + " Mrd. €", `${pct(sL4 / A.BIP, 1)} des BIP,')
rep('2070 rund ${mrd(j70.saldo)} Mrd. €` : ""), cl(g.saldoL));', '2070 rund ${mrd(j70.saldo)} Mrd. €` : ""), cl(sL4));')
open(p, 'w', encoding='utf-8').write(s)
print('Staatsseite auf Rechenkern Version 36')
