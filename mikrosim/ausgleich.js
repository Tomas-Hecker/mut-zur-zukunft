// Ausgleichsvarianten für Haushalte, die zum Start weniger haben: Kosten und wer danach noch weniger hat. Konsum wie Version 31.
const K = require("./kern.js"); const fs = require("fs"); const S = require("./simulation.js");
const pop = JSON.parse(fs.readFileSync(__dirname + "/bevoelkerung.json"));
const e = S.rechne(K, pop, { eichung: "konsum" }); const sp = pop.spalten; const A = K.A;
const t = A.Satz3 / (1 + A.Satz3);
const hh = i => sp.typ[i] !== "kind_erw";
// Überleben eines Haushalts t Jahre nach dem Start (wie der Bestandsschutz: Sterbetafel nach Gompertz, Paare bis zum zweiten Tod)
const opt = e.opt;
const qx = a => Math.min(1, opt.q65 * Math.exp(opt.gompertz * (a - 65)));
function ueberleben(i, t) {
  let s1 = 1, s2 = 1; const a = sp.alter[i];
  for (let k = 0; k < t; k++) { s1 *= 1 - qx(a + k); s2 *= 1 - opt.paarFaktor * qx(a + k + opt.paarVersatz); }
  return sp.erw[i] === 2 ? 1 - (1 - s1) * (1 - s2) : s1;
}
const JAHRE = [0, 5, 10, 15, 20, 30];
const r1 = x => +x.toFixed(1);
function gruppe(sel, extra) {
  let n = 0, sm = 0, n100 = 0, nH = 0;
  for (const r of e.R) {
    if (!hh(r.i) || !sel(r.i)) continue; const w = sp.w[r.i]; nH += w;
    const p = (r.plus + Math.max(0, extra(r))) / 12;
    if (p < -0.5) { n += w; sm += w * p; } if (p < -100) n100 += w;
  }
  return { haushalte_mio: r1(nH / 1e6), weniger_mio: r1(n / 1e6), anteil_prozent: Math.round(100 * n / nH), mittel_monat: Math.round(-sm / Math.max(n, 1)), ueber100_mio: r1(n100 / 1e6) };
}
const rentner = i => sp.rentner[i] > 0, uebrige = i => !(sp.rentner[i] > 0);
function bilanz(name, extra) {   // extra(r) = Ausgleich in € im Jahr für diesen Haushalt
  let kost = 0, kostR = 0, plus = 0, minus = 0, n = 0, sm = 0, n100 = 0, nH = 0;
  const lauf = JAHRE.map(() => 0);
  for (const r of e.R) {
    const w = sp.w[r.i], x = Math.max(0, extra(r)); kost += w * x;
    if (rentner(r.i)) { kostR += w * x; JAHRE.forEach((t, j) => { lauf[j] += w * x * ueberleben(r.i, t); }); }
    const nach = r.plus + x; if (nach > 0) plus += w * nach; else minus -= w * nach;
    if (!hh(r.i)) continue; nH += w;
    const p = nach / 12;
    if (p < -0.5) { n += w; sm += w * p; } if (p < -100) n100 += w;
  }
  const uebrigKost = (kost - kostR) / 1e9;
  return { name, kosten_mrd: r1(kost / 1e9), kosten_rentner_mrd: r1(kostR / 1e9), kosten_uebrige_mrd: r1(uebrigKost),
    auslauf_rentneranteil_mrd: Object.fromEntries(JAHRE.map((t, j) => [t, r1(lauf[j] / 1e9)])),
    plus_nach_mrd: r1(plus / 1e9), minus_nach_mrd: r1(minus / 1e9),
    weniger_mio: r1(n / 1e6), anteil: Math.round(100 * n / nH), monat: Math.round(-sm / n), ueber100_mio: r1(n100 / 1e6),
    rentner: gruppe(rentner, extra), uebrige: gruppe(uebrige, extra) };
}
const V = [];
V.push(bilanz("ohne Ausgleich (Version 32)", () => 0));
// A: Altvermögenskonto deckt auch den höheren Preis: Wer aus Erspartem kauft, zahlt auf den Mehrpreis keine Ausgabensteuer, und die
//    Mehrwertsteuer auf diesen Einkauf wird erstattet (das Konto wird um den Preisanstieg aufgestockt)
const altPreis = r => r.alt * r.pq * (r.ueberS ? 1 + A.Satz3 : 1);
V.push(bilanz("A: Erspartes kauft so viel wie heute (Konto um den Preisanstieg aufgestockt)", altPreis));
// B: Freibetrag für ausgegebene Zinsen, Dividenden und Mieten: 1.000 € je Erwachsenem (wie Sparer-Pauschbetrag) bzw. 3.000 €
const kapFrei = g => r => Math.min(r.kapKons, g * sp.erw[r.i]) * (r.ueberS ? t : 0);
V.push(bilanz("B1: Zinsen und Mieten bis 1.000 € je Erwachsenem frei", kapFrei(1000)));
V.push(bilanz("B2: Zinsen und Mieten bis 3.000 € je Erwachsenem frei", kapFrei(3000)));
// C: Bestandsschutz für alle heutigen Rentner auch auf Kapitalerträge und Erspartes (nur Rentner, voller Ausgleich)
V.push(bilanz("C: Rentner beim Start: voller Ausgleich", r => sp.rentner[r.i] ? -r.plus : 0));
// D: Härteausgleich auf Antrag, höchstens 500 / 1.000 € im Monat, schmilzt ab (hier erstes Jahr)
V.push(bilanz("D1: Härteausgleich bis 500 € im Monat", r => Math.min(-r.plus, 6000)));
V.push(bilanz("D2: Härteausgleich bis 1.000 € im Monat (wie Version 30)", r => Math.min(-r.plus, 12000)));
// E: Kombination A + B1 + Ausgleich bis 50 €
V.push(bilanz("E: A + B1", r => altPreis(r) + kapFrei(1000)(r)));
V.push(bilanz("F: A + B1, dazu Rest bis 50 € im Monat ohne Antrag", r => { const x = altPreis(r) + kapFrei(1000)(r); const rest = -(r.plus + x); return x + (rest > 0 && rest <= 600 ? rest : 0); }));
console.table(V.map(v => ({ name: v.name.slice(0, 46), kosten: v.kosten_mrd, rentner: v.kosten_rentner_mrd, in10J: v.auslauf_rentneranteil_mrd[10], weniger: v.weniger_mio, anteil: v.anteil, monat: v.monat, plus: v.plus_nach_mrd, minus: v.minus_nach_mrd })));
fs.writeFileSync(__dirname + "/ausgleich.json", JSON.stringify(V, null, 1));
