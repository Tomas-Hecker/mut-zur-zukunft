// Soll/Ist-Abgleich: jede Summe des Modells neben der amtlichen Zahl. Aufruf: node abgleich.js  ->  abgleich.md
const fs = require("fs"); const K = require("./kern.js"); const S = require("./simulation.js");
const pop = require("./bevoelkerung.json"); const sp = pop.spalten; const n = pop.n;
const e = S.rechne(K, pop, {}); const a = S.auswerten(e);
const M = f => { let s = 0; for (let i = 0; i < n; i++) s += sp.w[i] * f(i); return s / 1e9; };
const P = f => { let s = 0; for (let i = 0; i < n; i++) if (f(i)) s += sp.w[i]; return s / 1e6; };
const R = f => { let s = 0; for (const r of e.R) s += sp.w[r.i] * f(r); return s / 1e9; };
const aktivB = i => sp.beamter[i] && !sp.rentner[i];
const VGR = "VGR 2025, Destatis Fachserie 18 Reihe 1.4 (Stand 02.06.2026)";
const zeilen = [
  ["Bevölkerung", "Haushalte (Mio.)", 41.1, P(i => sp.typ[i] !== "kind_erw"), "Mikrozensus 2025", "geeicht"],
  ["Bevölkerung", "Erwachsene (Mio.)", 69.6, M(i => sp.erw[i]) * 1000, "Bevölkerungsstatistik 2025, 18 Jahre und älter", "fehlt: Heime, Teil der erwachsenen Kinder"],
  ["Bevölkerung", "Kinder unter 18 (Mio.)", 14.3, M(i => sp.kinder[i]) * 1000, "Bevölkerungsstatistik 2025", ""],
  ["Bevölkerung", "Haushalte im Eigentum (Anteil %)", 41.9, 100 * P(i => sp.eigen[i] > 0 && sp.typ[i] !== "kind_erw") / P(i => sp.typ[i] !== "kind_erw"), "Mikrozensus 2022", "geeicht"],
  ["Einkommen", "Bruttolöhne und -gehälter (Mrd. €)", 2036.3, M(i => sp.lohn1[i] + sp.lohn2[i] + sp.mini[i] + (aktivB(i) ? sp.pension[i] : 0)), VGR + ", Tab. 2.1.8", "geeicht (Faktor 1,11 auf die Löhne der Umfrage)"],
  ["Einkommen", "Renten der Rentenversicherung und Betriebsrenten (Mrd. €)", null, M(i => sp.rente[i]), "Alterssicherungsbericht; VGR enthält sie in 836,7 Mrd. € Sozialleistungen", "kein direkter Vergleich"],
  ["Einkommen", "Gewinne der Selbständigen und Ausschüttungen (Mrd. €)", 539.9, M(i => sp.gewinn[i] + sp.aus[i]), VGR + ", Konto II.1.2: Selbständigeneinkommen 175,6 + Ausschüttungen und Entnahmen 364,3", "Modell niedriger: Entnahmen aus Personengesellschaften nur teilweise erfasst"],
  ["Einkommen", "Verfügbares Einkommen (Mrd. €)", 2583.7, e.verfSumme, VGR + ", Konto II.2", "Modell ohne Organisationen ohne Erwerbszweck (rund 67), ohne unterstellte Zinsen (FISIM, rund 51) und Versicherungserträge (rund 38): vergleichbar rund 2.428"],
  ["Steuern", "Lohn- und Einkommensteuer samt Soli (Mrd. €)", 405, a.aufkommen.est_heute, "Kassenstatistik 2025: Lohnsteuer 262,7 + Kindergeld 54,6 + veranlagte 78,2 + Soli rund 9,5", "geeicht über Abzüge von 6,8 % des Erwerbseinkommens"],
  ["Steuern", "Mehrwertsteuer der Haushalte (Mrd. €)", null, a.aufkommen.mwst_heute, "Umsatzsteuer gesamt 310,2 (auch Staat, Vereine, Wohnungsbau)", "Anteil der Haushalte plausibel"],
  ["Konsum", "Konsum ohne Mietwert (Mrd. €)", 2085.7, a.aufkommen.konsum, VGR + ": Haushalte 2.305,4 − Mietwert 214,5 (Version 31: 2.300,2 − 214,5)", "geeicht"],
  ["Vermögen", "Restschuld auf das eigene Heim (Bio. €)", 1.15, M(i => sp.eigen[i] ? sp.hauswert[i] * (1 - sp.hb[i]) : 0) / 1000, "Bundesbank: Wohnungsbaukredite an private Haushalte rund 1,58 Bio. € (2025), davon rund drei Viertel für das eigene Heim (Schätzung)", "geeicht; davor 3,8 Bio. € (Fehler, zu hoch)"],
  ["Vermögen", "Mietwert, der nach der Reform besteuert wird (Anteil %)", null, 100 * M(i => sp.miet[i] * (1 - sp.hb[i])) / M(i => sp.miet[i]), "Regel „Eigenes Haus frei“: nur der beim Start noch nicht bezahlte Teil", ""],
  ["Konsum", "Mietwert selbst genutzter Wohnungen (Mrd. €)", 214.5, M(i => sp.miet[i]), "Eurostat, wie Version 31", "geeicht"],
  ["Vermögen", "Nettovermögen der Haushalte (Bio. €)", 16.6, M(i => sp.W[i]) / 1000, "Eichpunkt: PHF 2023 plus Zuschätzung der Reichsten", "geeicht"],
  ["Erbschaft", "Erbschaftsteuer heute (Mrd. €)", 21.4, a.erbschaft.erbst_heute_mrd, "festgesetzte Erbschaft- und Schenkungsteuer 2025", "Modell etwas niedriger"],
  ["Erbschaft", "Nachlässe und Schenkungen (Mrd. €)", "300–400", a.erbschaft.nachlass_mrd + a.erbschaft.schenkungen_mrd, "DIW-Schätzung", "im Bereich"],
];
const f = x => x == null ? "–" : typeof x === "string" ? x : x.toLocaleString("de-DE", { maximumFractionDigits: 1, minimumFractionDigits: 1 });
let md = "# Soll/Ist-Abgleich der Mikrosimulation\n\nStand " + new Date().toISOString().slice(0, 10) + ". Erzeugt mit `node abgleich.js`. „Soll“ ist die amtliche Zahl, „Ist“ die Summe der künstlichen Haushalte.\n\n";
md += "| Bereich | Größe | Soll | Ist | Abweichung | Quelle | Bemerkung |\n|---|---|---|---|---|---|---|\n";
for (const [b, g, s, i, q, bem] of zeilen) {
  const ab = typeof s === "number" ? (100 * (i - s) / s).toFixed(1).replace(".", ",") + " %" : "–";
  md += `| ${b} | ${g} | ${f(s)} | ${f(i)} | ${ab} | ${q} | ${bem} |\n`;
}
md += "\n## Sparen nach Gruppen (EVS 2018, Fachserie 15 Heft 4, Tabelle 1.2)\n\nAnteil der Konsumausgaben am Haushaltsnettoeinkommen, mit Mietwert auf beiden Seiten, Haushalte unter 18.000 € netto im Monat. Die EVS erfasst weniger Konsum als die VGR; verglichen wird deshalb der Abstand zu den Arbeitnehmerhaushalten.\n\n| Gruppe | EVS | Abstand zu Arbeitnehmern (EVS) | Modell | Abstand (Modell) |\n|---|---|---|---|---|\n";
const EVS = { "Arbeitnehmer": 2990 / 4214, "Ruhestand": 2389 / 2867, "Selbständige": 3429 / 5493 };
const g = { "Arbeitnehmer": [0, 0], "Ruhestand": [0, 0], "Selbständige": [0, 0] };
for (const r of e.R) { const i = r.i; if (sp.typ[i] === "kind_erw" || sp.bg[i] || sp.transfer[i] > 0) continue; const v = r.verf + sp.miet[i]; if (v > 216000) continue;
  const k = sp.rentner[i] ? "Ruhestand" : sp.selbst[i] ? "Selbständige" : "Arbeitnehmer"; g[k][0] += sp.w[i] * v; g[k][1] += sp.w[i] * (r.konsum + sp.miet[i]); }
const qm = k => g[k][1] / g[k][0];
for (const k in EVS) md += `| ${k} | ${(100 * EVS[k]).toFixed(1)} % | ${(100 * (EVS[k] - EVS.Arbeitnehmer)).toFixed(1)} Punkte | ${(100 * qm(k)).toFixed(1)} % | ${(100 * (qm(k) - qm("Arbeitnehmer"))).toFixed(1)} Punkte |\n`;
fs.writeFileSync(__dirname + "/abgleich.md", md.replace(/(\d)\.(\d) (Punkte|%)/g, "$1,$2 $3"));
console.log(md);
