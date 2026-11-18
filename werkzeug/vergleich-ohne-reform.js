
/* ---------- Mit und ohne Reform bis 2070, auf die Lebenszeit (Entwurf, Grundlage wie im Buch: grundlage-vergleich-ohne-reform.json) ----------
   Ohne Reform: heutiges Recht; mit Demografieschulden zahlt der Haushalt seinen Anteil an den Kosten des Alterns seit 2025
   (drei Viertel über Sozialbeiträge samt Arbeitgeberanteil, ein Viertel über Steuern, je im Verhältnis zu allen Haushalten).
   Mit Reform: das Plus von heute, Übergangsregeln schmelzen ab, Freibetrag und Wachstum je Jahr wie im Jahrespfad des Buchs. */
const VGL = { jahre: 2028, daten: {"vorsichtig":{"beitr":[33.6,44.8,56.0,68.0,79.9,91.9,103.9,115.9,124.8,133.8,142.7,151.7,160.7,165.1,169.6,174.1,178.6,183.1,187.6,192.1,196.6,201.1,205.5,208.5,211.5,214.5,217.5,220.5,223.5,226.4,229.4,232.4,235.4,238.4,241.4,244.4,247.4,250.4,253.4,256.4,259.4,262.4,265.4],"st":[11.2,14.9,18.7,22.7,26.6,30.6,34.6,38.6,41.6,44.6,47.6,50.6,53.6,55.0,56.5,58.0,59.5,61.0,62.5,64.0,65.5,67.0,68.5,69.5,70.5,71.5,72.5,73.5,74.5,75.5,76.5,77.5,78.5,79.5,80.5,81.5,82.5,83.5,84.5,85.5,86.5,87.5,88.5],"eink":[0,0.1,0.2,0.3,0.4,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.2,1.3,1.4,1.5,1.6,1.7,1.7,1.7,1.7,1.8,1.8,1.8,1.8,1.8,1.8,1.9,1.9,1.9,1.9,1.9,1.9,1.9,1.9,1.9,1.9,1.9,1.9,1.9,1.9],"fb":[1200,1200,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217,1217]},"mittel":{"beitr":[23.5,31.3,39.2,47.5,55.9,64.3,72.6,80.9,87.2,93.5,99.8,106.1,112.3,115.4,118.6,121.7,124.8,127.9,131.1,134.2,137.4,140.5,143.6,145.7,147.8,149.9,152.0,154.1,156.1,158.2,160.4,162.4,164.6,166.6,168.7,170.8,172.9,175.0,177.1,179.2,181.3,183.3,185.4],"st":[7.8,10.4,13.1,15.8,18.6,21.4,24.2,27.0,29.1,31.2,33.2,35.4,37.4,38.5,39.5,40.6,41.6,42.6,43.7,44.8,45.8,46.8,47.9,48.6,49.3,50.0,50.7,51.4,52.0,52.8,53.5,54.1,54.9,55.5,56.2,56.9,57.6,58.3,59.0,59.7,60.4,61.1,61.8],"eink":[0,0.7,1,1.4,1.8,2.1,2.5,2.9,3.2,3.6,4,4.4,4.8,5.1,5.5,5.9,6.3,6.7,7.1,7.4,7.5,7.5,7.5,7.6,7.6,7.6,7.6,7.7,7.7,7.7,7.8,7.8,7.8,7.8,7.8,7.8,7.8,7.8,7.8,7.8,7.8,7.8,7.8],"fb":[1200,1200,1200,1200,1200,1200,1200,1215,1230,1244,1259,1272,1285,1305,1321,1337,1352,1357,1359,1361,1362,1363,1362,1364,1365,1366,1367,1369,1370,1371,1372,1372,1372,1373,1373,1373,1374,1375,1375,1375,1375,1375,1375]},"zuversichtlich":{"beitr":[13.4,17.9,22.3,27.1,31.8,36.6,41.3,46.0,49.7,53.2,56.8,60.4,63.9,65.7,67.5,69.3,71.0,72.8,74.6,76.4,78.2,79.9,81.8,82.9,84.2,85.3,86.5,87.7,88.9,90.1,91.3,92.5,93.7,94.8,96.0,97.2,98.4,99.6,100.8,101.9,103.1,104.3,105.5],"st":[4.5,6.0,7.4,9.0,10.6,12.2,13.8,15.3,16.6,17.7,18.9,20.1,21.3,21.9,22.5,23.1,23.7,24.3,24.9,25.5,26.1,26.6,27.2,27.6,28.1,28.4,28.8,29.2,29.6,30.0,30.4,30.8,31.2,31.6,32.0,32.4,32.8,33.2,33.6,34.0,34.4,34.8,35.2],"eink":[0,1.3,1.9,2.6,3.2,3.9,4.6,5.3,6,6.7,7.4,8.1,8.9,9.6,10.3,11,11.7,12.4,13.1,13.8,13.9,14,14,14.1,14.1,14.2,14.3,14.3,14.4,14.4,14.5,14.5,14.5,14.5,14.5,14.5,14.5,14.5,14.5,14.5,14.5,14.5,14.5],"fb":[1200,1200,1200,1200,1228,1276,1322,1368,1402,1431,1442,1452,1462,1476,1489,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500,1500]}},
  svSumme: 740, stSumme: 690,   // Mrd. €, Summen aller Haushalte 2025 (vorläufig, bis die Mikrosimulation ihre Nenner liefert)
  rest: [[0, 80.5], [10, 70.9], [20, 61.0], [30, 51.2], [40, 41.5], [50, 32.1], [60, 23.4], [70, 15.5], [80, 8.7], [90, 4.1], [100, 1.9]] };   // fernere Lebenserwartung, Sterbetafel 2021/23, Mittel aus Frauen und Männern
let vglFall = "mittel", vglDemo = true, vglAlter = 40;
let vglE = { kwh: 3500, auto: "benzin", km: 13500, verbr: 7, alt: true, heiz: "gas", hmenge: 12000, pv: false, balkon: false };
// Klimageld, CO₂-Aufschlag, Kilometerabgabe und Produktabgabe je Jahr 2028 bis 2070 (energie-abgaben-je-haushalt-v41.json, Preise von heute)
VGL.abgaben = Object.assign({"kg":[101.6,94.3,174.0,159.6,145.2,130.9,116.5,127.7,115.8,104.0,92.2,80.3,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8,102.8],"benzin":[9.48,9.48,18.96,18.96,18.96,18.96,18.96,23.7,23.7,23.7,23.7,23.7,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55,35.55],"diesel":[10.6,10.6,21.2,21.2,21.2,21.2,21.2,26.5,26.5,26.5,26.5,26.5,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75],"oel":[10.6,10.6,21.2,21.2,21.2,21.2,21.2,26.5,26.5,26.5,26.5,26.5,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75,39.75],"gas":[0.8,0.8,1.61,1.61,1.61,1.61,1.61,2.01,2.01,2.01,2.01,2.01,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02,3.02],"satz":[0,0,21.62,19.59,18.7,18.19,18.37,18.7,19.16,19.69,20.49,21.59,22.73,23.98,25.25,26.54,27.79,28.85,29.7,30.33,30.81,31.13,31.35,31.35,31.35,31.35,31.35,31.35,31.35,31.35,31.35,31.35,31.35,31.35,31.35,31.35,31.35,31.35,31.35,31.35,31.35,31.35,31.35],"alt":[0.0,0.0,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0],"prod":[40.95,40.95,87.25,87.25,87.25,87.25,87.25,116.3,116.3,116.3,116.3,116.3,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45,174.45]}, { kwhJeL: { benzin: 8.857, diesel: 9.9 }, estCent: 65.45, dieselMehr: 18.41, mwst: 1.5 });
// Was Energie und Abgaben dem Haushalt im Jahr k gegenüber ohne Reform bringen (+) oder kosten (−)
function vglEnergie(k, fall, pers) {
  const E = VGL.energie, B = VGL.abgaben, e = vglE, t = {};
  t.strom = e.kwh * E.stromJeKwh;
  t.anlagen = (e.auto === "elektro" ? E.auto[fall] : 0) + (e.heiz === "wp" ? E.wp[fall] : 0) + (e.pv ? E.pv[fall] : 0) + (e.balkon ? E.balkon[fall] : 0);
  let auf = 0, liter = 0;
  if (e.auto === "benzin" || e.auto === "diesel") { liter = e.km * e.verbr / 100; auf += liter * B[e.auto][k] / 100; }
  if (e.heiz === "gas") auf += e.hmenge * B.gas[k] / 100;
  if (e.heiz === "oel") auf += e.hmenge * B.oel[k] / 100;
  t.klima = B.kg[k] * pers - auf * B.mwst;                                                      // Klimageld minus Aufschlag auf den eigenen Verbrauch
  let kmA = 0;
  if (e.auto === "elektro") kmA = e.km * e.verbr / 100 * B.satz[k] / 100 * (e.alt ? B.alt[k] : 1);
  if (liter) { const voll = liter * B.kwhJeL[e.auto] * B.satz[k] / 100, ueber = Math.max(0, voll - liter * B.estCent / 100);
    kmA = (B.satz[k] > 0 ? ueber * (e.alt ? B.alt[k] : 1) : 0) + (e.auto === "diesel" ? liter * B.dieselMehr / 100 : 0); }
  t.km = -kmA;
  t.produkt = -0.25 * B.prod[k] * pers;                                                          // im Durchschnitt das 1,25-Fache des Klimagelds über die Preise
  t.summe = t.strom + t.anlagen + t.klima + t.km + t.produkt;
  return t;
}
// Energie: nur was über das Plus von heute hinausgeht (Werte des Buchs): Strompreisvorteil je kWh ohne Ladestrom, dazu je Maßnahme der Zusatznutzen im Jahr
VGL.energie = { stromJeKwh: 340 / 3500,
  auto: { vorsichtig: 660, mittel: 686, zuversichtlich: 673 }, wp: { vorsichtig: 998, mittel: 729, zuversichtlich: 357 },
  pv: { vorsichtig: 74, mittel: -16, zuversichtlich: -48 }, balkon: { vorsichtig: -72, mittel: -113, zuversichtlich: -116 } };
VGL.rentenAlter = 67; VGL.renteAnteil = 0.43;   // Regelaltersgrenze; Rente geschätzt als Anteil am Bruttolohn (Standardrente nach 45 Beitragsjahren, rund 43 %)
const vglRest = a => { const R = VGL.rest; a = clamp(a, 0, 100); for (let i = 1; i < R.length; i++) if (a <= R[i][0]) { const [a0, e0] = R[i - 1], [a1, e1] = R[i]; return e0 + (e1 - e0) * (a - a0) / (a1 - a0); } return R.at(-1)[1]; };
// Was der Haushalt in einer Lebensphase hat; fbV(Δ) misst den höheren Freibetrag direkt im Rechner (Stufe 1 um Δ € im Monat je Erwachsenem länger)
function vglPhase(h) {
  const r = haushalt(h), plus0 = r.vgl + r.entfall, memo = {};
  const fbV = d => { if (d <= 0) return 0; if (memo[d] !== undefined) return memo[d];
    const g1 = A.Grenze1, g2 = A.Grenze2; let v = 0;
    try { A.Grenze1 = g1 + d * 12; A.Grenze2 = g2 + d * 12; const r2 = haushalt(h); v = r2.vgl + r2.entfall - plus0; } finally { A.Grenze1 = g1; A.Grenze2 = g2; }
    return memo[d] = v; };
  return { h, r, plus0, fbV, schmelz: (r.ausgR || 0) + (r.rpz || 0), verf: Math.max(0, r.verf), konsum: r.konsum,
    svH: Math.max(0, r.heute.sv - h.pkv) + r.sv, stH: r.heute.est + r.heute.kap + r.heute.mwst };   // Beiträge samt Arbeitgeberanteil
}
function vglRente(h) {   // derselbe Haushalt ab der Regelaltersgrenze: Rente statt Lohn, Kinder aus dem Haus
  const ren = q => VGL.renteAnteil * Math.min(q, A.BBGRV);
  return Object.assign({}, h, { lohn1: 0, std1: 0, lohn2: 0, std2: 0, mini: 0, gewinn: 0, gmbh: 0, aus: 0, transfer: 0, kid6: 0, kid3: 0, kinder: 0, vollj: 0, unterhalt: 0,
    rente: h.rente + ren(h.lohn1) + ren(h.lohn2), rentner: true, bjob: false, kinderlos: h.kinderlos });
}
function vglRechne(h, r0, fall, alter) {
  const D = VGL.daten[fall], n = D.beitr.length, E = VGL.energie;
  const schonRente = h.rentner || alter >= VGL.rentenAlter;
  const jahrRente = schonRente ? 0 : 2026 + VGL.rentenAlter - alter;
  const P0 = vglPhase(h), PR = schonRente ? P0 : vglPhase(vglRente(h));
  let fix = 0;
  if (fall === "vorsichtig") { try { const g = gesamt(), kr = kredit(g.saldoS, g.saldoL, 45, g.s4); fix = regelPlan("vorsichtig", kr.rows.map(x => x.saldo)).fix; } catch (e) { fix = 0; } }
  const rows = [];
  for (let k = 0; k < n; k++) {
    const jahr = VGL.jahre + k, rente = !schonRente && jahr >= jahrRente, P = rente ? PR : P0;
    const last = D.beitr[k] * P.svH / VGL.svSumme + D.st[k] * P.stH / VGL.stSumme;   // Mrd. × Anteil = €
    const ueb = rente ? -P.schmelz : -P.schmelz * (1 - Math.max(0, 1 - k / 27) ** 2);   // Bestandsschutz und Zuschlag schmelzen wie im Buch; neue Rentner haben keinen
    const wachs = D.eink[k] / 100 * P.verf;                                             // mehr Einkommen nur mit Reform, einmal gezählt
    const fb = P.fbV(Math.round(D.fb[k] - D.fb[0]));                                     // höherer Freibetrag, Vorteil zum Satz der Stufe, in die die Ausgaben fallen
    const mw = jahr >= 2030 ? -fix / 100 * 0.7 * P.konsum : 0;                           // vorsichtig: fester Aufschlag auf den Normalsatz
    const en = vglEnergie(k, fall, P.h.erw + (P.h.kinder || 0)), energie = en.summe;
    rows.push({ jahr, rente, en, mit: P.plus0 + ueb + wachs + fb + mw + energie, last, teile: { plus0: P.plus0, ueb, wachs, fb, mw, energie } });
  }
  return rows;
}
function vglZeigen() {
  let box = $("vglBox");
  if (!box) { const calc = $("sidePanel") && $("sidePanel").parentElement; if (!calc) return; box = document.createElement("div"); box.className = "panel"; box.id = "vglBox"; box.style.marginTop = "18px"; calc.after(box); }
  if ($("zukunft")) $("zukunft").innerHTML = "";   // ersetzt „Auf 30 Jahre gerechnet“
  const h = readForm(), r = haushalt(h), rows = vglRechne(h, r, vglFall, vglAlter);
  const ende = Math.round(2026 + vglRest(vglAlter));   // Lebensende im Mittel
  const rente = !h.rentner && vglAlter < VGL.rentenAlter ? 2026 + VGL.rentenAlter - vglAlter : 0;
  const at = j => rows[Math.min(rows.length - 1, Math.max(0, j - VGL.jahre))];
  const summe = (bis, f) => { let s = 0; for (let j = VGL.jahre; j <= bis; j++) s += f(at(j)); return s; };
  const vor = x => x.mit + (vglDemo ? x.last : 0);
  const zeilen = [[10, 2037], [20, 2047], [30, 2057], [40, 2067], ["bis 2070", 2070], ["Lebenszeit", ende]];
  const zelle = x => `<td class="${x >= 0 ? "good" : "bad"}">${x >= 0 ? "+" : "−"}${eur(Math.abs(x))}</td>`;
  // Sparen: Vermögen aus der Sparquote, ohne Reform mit Abgeltungsteuer auf den Ertrag, mit Reform steuerfrei, solange angelegt
  const rr = A.RenditeReal, inf = 0.02, rOhne = (1 + (rr + inf) * (1 - 0.26375)) / (1 + inf) - 1, s = h.spar * Math.max(0, r.verf);
  const verm = (q, n) => q ? s * ((1 + q) ** n - 1) / q : s * n;
  const F = { vorsichtig: "Ungünstig", mittel: "Wahrscheinlich", zuversichtlich: "Günstig" };
  box.innerHTML = `<h3>Mit und ohne Reform bis 2070</h3>
    <p class="note">Verglichen wird nicht mit heute, sondern mit dem Weg ohne Reform. Ohne Reform steigen die Kosten für Rente, Pflege und Gesundheit; ${vglDemo ? "dieser Haushalt trägt seinen Anteil daran über höhere Beiträge und Steuern (Demografieschulden)." : "hier ausgeschaltet, also so, als blieben Beiträge und Steuern wie heute."} Mit Reform zählen das Wachstum, der steigende Freibetrag${typeof energieRechne === "function" ? ", die Ersparnis bei Energie und Auto" : ""} und das Auslaufen der Übergangsregeln. In heutigen Preisen, ohne Abzinsung, Haushalt wie oben eingegeben.</p>
    <div class="presets" role="group" aria-label="Fall">${Object.entries(F).map(([k, n]) => `<button type="button" class="chip" data-vf="${k}" aria-pressed="${k === vglFall}">${n}</button>`).join("")}</div>
    <div class="row" style="display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin:10px 0">
      <label><input type="checkbox" id="vglDemo" ${vglDemo ? "checked" : ""}> mit Demografieschulden</label>
      <label>Alter heute <input type="number" id="vglAlter" min="0" max="100" value="${vglAlter}" style="width:5em"> Jahre, Lebenserwartung im Mittel bis ${ende}${rente ? `, Rente ab ${rente}` : ""}</label>
    </div>
    <div class="row" style="display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin:0 0 10px">
      <label>Strom im Jahr <input type="number" id="vglKwh" min="0" max="50000" step="100" value="${vglE.kwh}" style="width:6em"> kWh ohne Ladestrom</label>
      ${[["pv", "Solar auf dem Dach (10 kWp)"], ["balkon", "Balkonkraftwerk"]].map(([k, n]) => `<label><input type="checkbox" data-ve="${k}" ${vglE[k] ? "checked" : ""}> ${n}</label>`).join("")}
    </div>
    <div class="row" style="display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin:0 0 10px">
      <label>Auto <select id="vglAuto">${[["kein", "keins"], ["benzin", "Benziner"], ["diesel", "Diesel"], ["elektro", "Elektroauto"]].map(([k, n]) => `<option value="${k}" ${vglE.auto === k ? "selected" : ""}>${n}</option>`).join("")}</select></label>
      ${vglE.auto !== "kein" ? `<label><input type="number" id="vglKm" min="0" max="100000" step="500" value="${vglE.km}" style="width:6em"> km im Jahr</label>
      <label><input type="number" id="vglVerbr" min="0" max="40" step="0.5" value="${vglE.verbr}" style="width:4.5em"> ${vglE.auto === "elektro" ? "kWh" : "Liter"} je 100 km</label>
      <label><input type="checkbox" id="vglAlt" ${vglE.alt ? "checked" : ""}> gekauft vor 2028</label>` : ""}
    </div>
    <div class="row" style="display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin:0 0 10px">
      <label>Heizung <select id="vglHeiz">${[["gas", "Gas"], ["oel", "Heizöl"], ["wp", "Wärmepumpe"], ["andere", "Fernwärme oder andere"]].map(([k, n]) => `<option value="${k}" ${vglE.heiz === k ? "selected" : ""}>${n}</option>`).join("")}</select></label>
      ${vglE.heiz === "gas" || vglE.heiz === "oel" ? `<label><input type="number" id="vglHM" min="0" max="100000" step="100" value="${vglE.hmenge}" style="width:6em"> ${vglE.heiz === "gas" ? "kWh Gas" : "Liter Heizöl"} im Jahr</label>` : ""}
    </div>
    <div class="tbl-wrap"><table><thead><tr><th>Zusammen</th><th>Ohne Reform: Demografieschulden</th><th>Mit Reform: Plus gegenüber heute</th><th>Vorteil der Reform</th></tr></thead><tbody>
    ${zeilen.map(([n, bis]) => `<tr><td>${typeof n === "number" ? "nach " + n + " Jahren" : n === "Lebenszeit" ? "auf die Lebenszeit (bis " + bis + ")" : n}</td>${zelle(-summe(bis, x => x.last))}${zelle(summe(bis, x => x.mit))}${zelle(summe(bis, vor))}</tr>`).join("")}
    </tbody></table></div>
    <div class="tbl-wrap"><table><thead><tr><th>Im Jahr</th>${[2030, 2040, 2050, 2060, 2070].map(j => `<th>${j}</th>`).join("")}</tr></thead><tbody>
      <tr><td>Vorteil der Reform im Monat</td>${[2030, 2040, 2050, 2060, 2070].map(j => zelle(vor(at(j)) / 12)).join("")}</tr></tbody></table></div>
    ${s > 0 ? `<h3>Was aus dem Gesparten wird</h3><p class="note">Dieser Haushalt spart ${pct(h.spar, 0)}, ${eur(s)} im Jahr, angelegt mit ${pct(rr, 0)} Rendite nach Inflation. Ohne Reform kostet die Abgeltungsteuer auf den Ertrag, mit Reform bleibt er steuerfrei, solange er angelegt bleibt.</p>
    <div class="tbl-wrap"><table><thead><tr><th>Vermögen nach</th><th>ohne Reform</th><th>mit Reform</th><th>mehr</th></tr></thead><tbody>${[10, 20, 30, 40].map(n => `<tr><td>${n} Jahren</td><td>${eur(verm(rOhne, n))}</td><td>${eur(verm(rr, n))}</td>${zelle(verm(rr, n) - verm(rOhne, n))}</tr>`).join("")}</tbody></table></div>` : ""}
    <p class="note">Entwurf. Mit ${VGL.rentenAlter} wechselt der Haushalt in die Rente: Rente geschätzt mit ${pct(VGL.renteAnteil, 0)} des Bruttolohns (bis zur Beitragsgrenze), Kinder aus dem Haus, kein Bestandsschutz für neue Rentner. Strom: Preisvorteil nach Verbrauch ohne Ladestrom, dazu je Anlage der Zusatznutzen im Jahr. Klimageld je Person minus CO₂-Aufschlag auf Sprit, Heizöl und Gas (mit 50 % Mehrwertsteuer der Reform), Kilometerabgabe ab 2030 (beim Verbrenner nur der Betrag über der Energiesteuer, für Autos von vor 2028 anteilig bis 2038), Produktabgabe im Durchschnitt das 1,25-Fache ihres Klimagelds; Werte der Version 41 je Jahr. Lebenserwartung nach der Sterbetafel 2021/23 (Mittel aus Frauen und Männern), nach 2070 wie 2070 gerechnet. Erbschaften sind nicht enthalten.</p>`;
  box.querySelectorAll("[data-vf]").forEach(b => b.onclick = () => { vglFall = b.dataset.vf; vglZeigen(); });
  $("vglDemo").onchange = e => { vglDemo = e.target.checked; vglZeigen(); };
  $("vglKwh").onchange = e => { vglE.kwh = clamp(+e.target.value || 0, 0, 50000); vglZeigen(); };
  $("vglAuto").onchange = e => { vglE.auto = e.target.value; vglE.verbr = vglE.auto === "elektro" ? 18 : vglE.auto === "diesel" ? 6 : 7; vglZeigen(); };
  $("vglHeiz").onchange = e => { vglE.heiz = e.target.value; vglE.hmenge = vglE.heiz === "oel" ? 1200 : 12000; vglZeigen(); };
  [["vglKm", "km", 100000], ["vglVerbr", "verbr", 40], ["vglHM", "hmenge", 100000]].forEach(([id, k, mx]) => { if ($(id)) $(id).onchange = e => { vglE[k] = clamp(+e.target.value || 0, 0, mx); vglZeigen(); }; });
  if ($("vglAlt")) $("vglAlt").onchange = e => { vglE.alt = e.target.checked; vglZeigen(); };
  box.querySelectorAll("[data-ve]").forEach(c => c.onchange = () => { vglE[c.dataset.ve] = c.checked; vglZeigen(); });
  $("vglAlter").onchange = e => { vglAlter = clamp(+e.target.value || 0, 0, 100); vglZeigen(); };
}
{ const alt = updateHH; updateHH = function () { const r = alt.apply(this, arguments); vglZeigen(); return r; }; }
