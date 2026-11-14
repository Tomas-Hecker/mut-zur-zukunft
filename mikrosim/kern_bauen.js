// Zieht den Rechenkern (Annahmen und haushalt()) unverändert aus dem Steuerrechner, damit beide immer gleich rechnen.
// Aufruf: node kern_bauen.js [../steuerrechner/index.html]  ->  kern.js
const fs = require("fs");
const quelle = process.argv[2] || __dirname + "/../steuerrechner/index.html";
const zeilen = fs.readFileSync(quelle, "utf8").split("\n");
const a = zeilen.findIndex(z => z.startsWith("const ANNAHMEN = {"));
const b = zeilen.findIndex(z => z.startsWith("const $ = id => document.getElementById(id);"));
if (a < 0 || b < 0) throw new Error("Rechenkern im Steuerrechner nicht gefunden");
let teil = zeilen.slice(a, b).join("\n");
// Einzige Ergänzung: Einkünfte aus Vermietung (h.vermiet) wie Gewinn in der Einkommensteuer, aber ohne als Verdienst im Rentenalter
// zu zählen. Ohne h.vermiet rechnet der Kern genau wie der Steuerrechner.
const ersetze = (alt, neu) => { if (teil.split(alt).length !== 2) throw new Error("Stelle nicht eindeutig: " + alt); teil = teil.replace(alt, neu); };
ersetze("const zvE = Math.max(0, Math.floor(lohn + h.gewinn + ", "const zvE = Math.max(0, Math.floor(lohn + h.gewinn + (h.vermiet || 0) + ");
ersetze("const verf = lohn + h.mini + h.rente + h.gewinn + h.kap + ", "const verf = lohn + h.mini + h.rente + h.gewinn + (h.vermiet || 0) + h.kap + ");
ersetze("gmbh: 0, aus: 0, verm: 0, transfer: 0, bs: 0, _cap: false", "gmbh: 0, aus: 0, verm: 0, vermiet: 0, transfer: 0, bs: 0, _cap: false");
ersetze("const einkommen = lohn + h.mini + h.rente + h.gewinn + h.kap + ", "const einkommen = lohn + h.mini + h.rente + h.gewinn + (h.vermiet || 0) + h.kap + ");
const sich = zeilen.find(z => z.startsWith("function sicherheitAnwenden()"));
const kopf = `// AUTOMATISCH ERZEUGT von kern_bauen.js aus ${require("path").basename(require("path").dirname(quelle))}/index.html. Nicht von Hand ändern.\n"use strict";\n`;
const fuss = `\n${sich}\nsicherheitAnwenden();\nmodule.exports = { A, A0, haushalt, gesamt, abgeleitet, tarif, xtInv, sicherheitAnwenden, BEISPIELE };\n`;
fs.writeFileSync(__dirname + "/kern.js", kopf + teil + fuss);
console.log("kern.js geschrieben, Zeilen", a + 1, "bis", b);
