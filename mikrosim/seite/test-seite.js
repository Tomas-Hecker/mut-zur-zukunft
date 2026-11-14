// Prüft die Seite im Browser: lädt sie über file:// mit eingebetteten Haushalten und rechnet zwei Einstellungen
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");
(async () => {
  const html = fs.readFileSync(path.join(__dirname, "index.html"), "utf8");
  const pop = fs.readFileSync(path.join(__dirname, "bevoelkerung.json"), "utf8");
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1300, height: 1800 } });
  const fehler = [];
  pg.on("pageerror", e => fehler.push(e.message));
  await pg.route("**/bevoelkerung.json", r => r.fulfill({ body: pop, contentType: "application/json" }));
  await pg.route("**/seite.html", r => r.fulfill({ body: "<!doctype html><meta charset=utf-8>" + html, contentType: "text/html" }));
  await pg.goto("http://localhost/seite.html");
  const fertig = () => pg.waitForFunction(() => /Gerechnet|Fehler|ließen/.test(document.getElementById("status").textContent), null, { timeout: 90000 });
  await fertig();
  console.log(await pg.textContent("#status"));
  console.log("Fehler:", fehler.join(" | ") || "keine");
  await pg.screenshot({ path: process.argv[2] || "/tmp/seite.png" });
  await pg.click("text=Reiche kürzen nicht");
  await pg.waitForTimeout(200);
  await fertig();
  console.log((await pg.textContent("#kacheln")).replace(/\s+/g, " "));
  await b.close();
})();
