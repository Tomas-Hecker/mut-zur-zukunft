// Zweiter Schritt nach bevoelkerung.py: eicht die Abzüge in der Einkommensteuer, die der Rechenkern nicht einzeln kennt
// (Werbungskosten über der Pauschale, Sonderausgaben wie Kirchensteuer, Spenden, Riester und Rürup, außergewöhnliche Belastungen,
// steuerfreie Lohnteile wie Zuschläge, Entgeltumwandlung und Jobticket). Sie werden als einheitlicher Anteil q des Erwerbseinkommens
// (Löhne, Besoldung, Gewinne) angesetzt und q so gewählt, dass Lohn- und Einkommensteuer samt Soli dem Aufkommen 2025 entsprechen.
// Aufruf: node eichen.js   (schreibt die Spalte abzug in bevoelkerung.json)
const fs = require("fs");
const K = require("./kern.js");
const S = require("./simulation.js");
const datei = __dirname + "/bevoelkerung.json";
const pop = JSON.parse(fs.readFileSync(datei, "utf8"));
const sp = pop.spalten, n = pop.n;
// Lohnsteuer 262,7 (kassenmäßig, nach Kindergeld) + Kindergeld 54,6 + veranlagte Einkommensteuer 78,2 + Soli darauf rund 9,5 Mrd. €
const ZIEL = 405;
const basis = i => sp.lohn1[i] + sp.lohn2[i] + sp.gewinn[i] + (sp.beamter[i] && !sp.rentner[i] ? sp.pension[i] : 0);
function est(q) {
  sp.abzug = Array.from({ length: n }, (_, i) => Math.round(q * basis(i)));
  const e = S.rechne(K, pop, { eichung: "fest", a0fest: 0.1 });
  let s = 0; for (const r of e.R) s += sp.w[r.i] * r.heute.est; return s / 1e9;
}
let lo = 0, hi = 0.25;
console.log("ohne Abzüge", est(0).toFixed(1));
for (let k = 0; k < 14; k++) { const m = (lo + hi) / 2; if (est(m) > ZIEL) lo = m; else hi = m; }
const q = (lo + hi) / 2;
console.log("Abzugsquote", q.toFixed(4), "Einkommensteuer", est(q).toFixed(1), "Mrd. € (Ziel", ZIEL + ")");
let summe = 0; for (let i = 0; i < n; i++) summe += sp.w[i] * sp.abzug[i];
console.log("Abzüge zusammen", (summe / 1e9).toFixed(1), "Mrd. €");
pop.eckwerte.est_mrd = ZIEL; pop.eckwerte.abzug_quote = +q.toFixed(4);
fs.writeFileSync(datei, JSON.stringify(pop));
