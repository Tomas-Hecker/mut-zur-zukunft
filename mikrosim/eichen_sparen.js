// Eicht die Sparquoten von Rentner- und Selbständigenhaushalten relativ zu Arbeitnehmerhaushalten auf die EVS 2018
// (Statistisches Bundesamt, Fachserie 15 Heft 4, Tabelle 1.2: Konsumausgaben je Haushaltsnettoeinkommen). Verglichen werden nur
// Haushalte unter 18.000 € netto im Monat, weil die EVS reichere Haushalte nicht erfasst. Mietwert zählt wie in der EVS auf beiden Seiten.
// Aufruf: node eichen_sparen.js  -> gibt sparRentner und sparSelbst aus (in simulation.js STANDARD eintragen)
const K = require("./kern.js"); const S = require("./simulation.js"); const pop = require("./bevoelkerung.json"); const sp = pop.spalten;
const EVS = { an: 2990 / 4214, rentner: 2389 / 2867, selbst: 3429 / 5493 };
function quoten(o) {
  const e = S.rechne(K, pop, o); const g = { an: [0, 0], rentner: [0, 0], selbst: [0, 0] };
  for (const r of e.R) {
    const i = r.i; if (sp.typ[i] === "kind_erw" || sp.bg[i] || sp.transfer[i] > 0) continue;
    const v = r.verf + sp.miet[i]; if (v > 216000) continue;
    const k = sp.rentner[i] ? "rentner" : sp.selbst[i] ? "selbst" : "an";
    g[k][0] += sp.w[i] * v; g[k][1] += sp.w[i] * (r.konsum + sp.miet[i]);
  }
  const q = {}; for (const k in g) q[k] = g[k][1] / g[k][0]; return q;
}
let o = { sparRentner: 0, sparSelbst: 0 };
for (let it = 0; it < 6; it++) {
  const q = quoten(o);
  // Abstand der Konsumquoten wie in der EVS (in Prozentpunkten). Das Verhältnis statt des Abstands verlangte von Rentnern, mehr
  // auszugeben, als sie einnehmen und an Erspartem haben; der Abstand ist die vorsichtigere Lesart (siehe Annahmen.md).
  const zielR = q.an + (EVS.rentner - EVS.an), zielS = q.an + (EVS.selbst - EVS.an);
  console.log(it, "AN", q.an.toFixed(3), "Rentner", q.rentner.toFixed(3), "(Ziel", zielR.toFixed(3) + ")", "Selbst", q.selbst.toFixed(3), "(Ziel", zielS.toFixed(3) + ")", JSON.stringify(o));
  o = { sparRentner: +(o.sparRentner + (q.rentner - zielR)).toFixed(4), sparSelbst: +(o.sparSelbst + (q.selbst - zielS)).toFixed(4) };
}
console.log("Ergebnis", JSON.stringify(o));
