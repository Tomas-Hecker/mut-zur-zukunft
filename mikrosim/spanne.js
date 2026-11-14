// Ehrliche Spanne: Haushalte mit weniger im ersten Jahr unter anderen vertretbaren Eichungen, ohne und mit Ausgleich (Version 32).
// Aufruf: node spanne.js   (schreibt spanne.json)
const fs = require("fs"); const K = require("./kern.js"); const S = require("./simulation.js");
const pop = require("./bevoelkerung.json"); const sp = pop.spalten;
const orig = { aus: sp.aus.slice(), gewinn: sp.gewinn.slice(), kap: sp.kap.slice() };
// Faktoren auf Ausschüttungen, Gewinne aus der eigenen Firma und Kapitalerträge: den Haushalten fehlen gegenüber der VGR rund 150 Mrd. €
// Gewinne und Entnahmen; wo genau, ist offen. Dazu der zweite Anker der Eichung (Sparquote 10,4 % statt Konsum 2.050,2 Mrd. €) und der Konsum samt unterstellter
// Bankgebühren (2.085,7 Mrd. €, Eichung bis 14.11.).
const EICHUNGEN = [
  { name: "Standard", f: [1, 1, 1] },
  { name: "Ausschüttungen doppelt", f: [2, 1, 1] },
  { name: "Ausschüttungen × 1,5, Gewinne × 1,2", f: [1.5, 1.2, 1] },
  { name: "Kapitalerträge × 1,5", f: [1, 1, 1.5] },
  { name: "Konsum samt Bankgebühren (FISIM)", f: [1, 1, 1], o: { konsumZiel: 2085.7 } },
];
const AUSGLEICH = [
  { name: "ohne Ausgleich", o: {} },
  { name: "Version 32: Rentner bis 300 €, 10 € je Erwachsenem", o: { ausgleichRentnerMonat: 300, pauschaleErwMonat: 10 } },
];
const r1 = x => Math.round(10 * x) / 10;
const out = { stand: new Date().toISOString().slice(0, 10), hinweis: "Haushalte mit weniger als 0,50 € im Monat weniger, erstes Jahr, gleicher Einkauf", varianten: [] };
for (const a of AUSGLEICH) {
  const zeilen = [];
  for (const E of EICHUNGEN) {
    sp.aus = orig.aus.map(x => x * E.f[0]); sp.gewinn = orig.gewinn.map(x => x * E.f[1]); sp.kap = orig.kap.map(x => x * E.f[2]);
    for (const eichung of ["konsum", "sparquote"]) {
      const s = S.auswerten(S.rechne(K, pop, { ...a.o, ...(E.o || {}), eichung }));
      zeilen.push({ eichung: E.name, anker: eichung === "konsum" ? "Konsum" : "Sparquote", weniger_mio: r1(s.weniger.mio),
        anteil_prozent: r1(100 * s.weniger.mio / s.haushalte_mio), mittel_monat: Math.round(s.weniger.monat_mittel) });
    }
  }
  const w = zeilen.map(z => z.weniger_mio);
  out.varianten.push({ ausgleich: a.name, standard_mio: zeilen[0].weniger_mio, standard_prozent: zeilen[0].anteil_prozent,
    von_mio: Math.min(...w), bis_mio: Math.max(...w), zeilen });
}
fs.writeFileSync(__dirname + "/spanne.json", JSON.stringify(out, null, 1));
for (const v of out.varianten) {
  console.log(`${v.ausgleich}: Standard ${v.standard_mio} Mio. (${v.standard_prozent} %), Spanne ${v.von_mio} bis ${v.bis_mio} Mio.`);
  for (const z of v.zeilen) console.log(`  ${z.eichung.padEnd(38)} ${z.anker.padEnd(10)} ${String(z.weniger_mio).padStart(5)} Mio. ${String(z.anteil_prozent).padStart(5)} %  ${z.mittel_monat} €`);
}
