// Übergabe an das Buch-Rechenmodell: Haushalte mit weniger, Plus und Minus im ersten Jahr, Ausgleichsvarianten. Aufruf: node uebergabe.js
const fs = require("fs"); const K = require("./kern.js"); const S = require("./simulation.js");
const pop = require("./bevoelkerung.json"); const sp = pop.spalten;
require("./ausgleich.js");   // schreibt ausgleich.json neu
const V = JSON.parse(fs.readFileSync(__dirname + "/ausgleich.json", "utf8"));
const e = S.rechne(K, pop, {}); const a = S.auswerten(e);
const r1 = x => +x.toFixed(1);
const out = {
  stand: new Date().toISOString().slice(0, 10),
  grundlage: "Mikrosimulation, Standard: Konsum 2.085,7 Mrd. € wie VGR 2025, Löhne und Einkommensteuer auf 2025 geeicht, Sparen nach EVS; Rechenkern Version 31/32",
  hinweis: "Werte für das erste Jahr bei gleichem Einkauf, mit Bestandsschutz und Altvermögenskonto; Plus und Minus sind Summen über Haushalte (auch erwachsene Kinder als eigene Steuerfälle)",
  "1_haushalte_mit_weniger": { alle: { mio: V[0].weniger_mio, anteil_prozent: V[0].anteil, mittel_monat: V[0].monat, ueber100_mio: V[0].ueber100_mio }, rentner: V[0].rentner, uebrige: V[0].uebrige },
  "2_plus_minus_mrd": { plus: V[0].plus_nach_mrd, minus: V[0].minus_nach_mrd, saldo: r1(V[0].plus_nach_mrd - V[0].minus_nach_mrd),
    bestandsschutz_mrd: r1(a.bestandsschutz.mrd), beamte_zulage_mrd: r1(a.beamte_zulage.mrd),
    probe: "Plus minus Minus ist hier die Summe der Haushalte, nicht der Saldo des Staates; Unternehmen, Ausland, Staatsausgaben und Übergänge fehlen. Ein Abweichen von −12,7 ist deshalb kein Fehler, muss aber im Buch-Modell erklärt werden." },
  "3_ausgleich": V.slice(1).map(v => ({ name: v.name, kosten_erstes_jahr_mrd: v.kosten_mrd, davon_rentner_mrd: v.kosten_rentner_mrd, davon_uebrige_mrd: v.kosten_uebrige_mrd,
    rentneranteil_nach_jahren_mrd: v.auslauf_rentneranteil_mrd, auslauf: "Rentneranteil sinkt mit der Sterbetafel wie der Bestandsschutz; der Anteil der Übrigen bleibt, bis die Regel ausläuft oder abschmilzt (politische Entscheidung)",
    plus_nach_mrd: v.plus_nach_mrd, minus_nach_mrd: v.minus_nach_mrd, weniger_mio: v.weniger_mio, anteil_prozent: v.anteil, mittel_monat: v.monat, rentner: v.rentner, uebrige: v.uebrige })),
  spanne: "Mit anderen vertretbaren Eichungen (Sparquote statt Konsum als Anker, höhere Ausschüttungen, höhere Kapitalerträge; node spanne.js): ohne Ausgleich 16,2 bis 19,8 Mio. Haushalte mit weniger (Standard 17,7), mit dem Ausgleich von Version 32 9,9 bis 13,3 Mio. (Standard 11,2)",
};
fs.writeFileSync(__dirname + "/uebergabe-buch.json", JSON.stringify(out, null, 1));
console.log(JSON.stringify(out["1_haushalte_mit_weniger"]), JSON.stringify(out["2_plus_minus_mrd"]));
