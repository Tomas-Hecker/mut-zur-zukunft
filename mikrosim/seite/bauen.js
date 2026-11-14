// Baut seite/index.html aus der Vorlage, kern.js und simulation.js
const fs = require("fs"); const p = f => require("path").join(__dirname, f);
let h = fs.readFileSync(p("vorlage.html"), "utf8");
h = h.replace("/*KERN*/", () => fs.readFileSync(p("../kern.js"), "utf8")).replace("/*SIM*/", () => fs.readFileSync(p("../simulation.js"), "utf8"));
fs.writeFileSync(p("index.html"), h); fs.copyFileSync(p("../bevoelkerung.json"), p("bevoelkerung.json"));
console.log("seite/index.html", h.length);
