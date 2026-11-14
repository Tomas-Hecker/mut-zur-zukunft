// Aufruf: node lauf.js [annahmen.json]  — rechnet alles und schreibt ergebnis.json
const fs = require("fs");
const K = require("./kern.js");
const { rechne, auswerten } = require("./simulation.js");
const t0 = Date.now();
const pop = JSON.parse(fs.readFileSync(__dirname + "/bevoelkerung.json", "utf8"));
const opt = process.argv[2] ? JSON.parse(fs.readFileSync(process.argv[2], "utf8")) : {};
const erg = rechne(K, pop, opt);
const a = auswerten(erg);
a.sekunden = (Date.now() - t0) / 1000;
fs.writeFileSync(process.argv[3] || __dirname + "/ergebnis.json", JSON.stringify(a, null, 1));
const r1 = x => typeof x === "number" ? Math.round(x * 10) / 10 : x;
console.log(JSON.stringify({ ...a, stufen: undefined, zehntel: undefined }, (k, v) => r1(v), 1));
console.table(a.stufen.map(s => Object.fromEntries(Object.entries(s).map(([k, v]) => [k.slice(0, 14), typeof v === "number" ? Math.round(v * 100) / 100 : v]))));
console.table(a.zehntel.map(s => Object.fromEntries(Object.entries(s).map(([k, v]) => [k.slice(0, 14), Math.round(v * 100) / 100]))));
