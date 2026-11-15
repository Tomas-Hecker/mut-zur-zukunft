/* Kleine Rechner (Balkon, E-Auto, Energie, Heizung, Gesundheit): Zeile „Im Buch nachlesen“ unter der Einleitung.
   Einbinden als letztes Skript vor </body>:  <script src="../tools-buchlinks.js"></script>  (Datei im Hauptordner). */
(() => {
  const L = {
    "balkon-rechner":  [["Kapitel 10: Strom und Wärme zu Hause", "kapitel-10.html#strom-zu-hause"], ["Kapitel 5: Strom aus Sonne und Wind", "kapitel-5.html#strom"], ["Anhang B5: Wohnen, Wärme und Strom", "anhang-b.html#b5"]],
    "eauto-rechner":   [["Kapitel 10: Strom und Wärme zu Hause", "kapitel-10.html#strom-zu-hause"], ["Anhang B5: Strom zur richtigen Stunde", "anhang-b.html#strom-simulation"], ["Anhang B7: CO₂-Preis", "anhang-b.html#b7"]],
    "energie-rechner": [["Kapitel 10: Strom und Wärme zu Hause", "kapitel-10.html#strom-zu-hause"], ["Kapitel 5: Strom aus Sonne und Wind", "kapitel-5.html#strom"], ["Anhang B5: Strom zur richtigen Stunde", "anhang-b.html#strom-simulation"]],
    "gesundheitsrechner": [["Kapitel 5: Gesundheitsabgabe und Gesundheitsbonus", "kapitel-5.html#7-gesundheitsabgabe-und-gesundheitsbonus"], ["Kapitel 6: Können wir uns das leisten?", "kapitel-6.html#koennen-wir-uns-das-leisten"]],
    "heizungsrechner": [["Kapitel 5: Wärmepumpe mit zinslosem Kredit", "kapitel-5.html#waermepumpe"], ["Anhang B5: Wärmepumpe mit zinslosem Kredit", "anhang-b.html#waermepumpe-kredit"], ["Kapitel 10: Strom und Wärme zu Hause", "kapitel-10.html#strom-zu-hause"]],
  };
  const teile = location.pathname.split("/").filter(Boolean);
  const ls = L[teile[teile.length - (location.pathname.endsWith("/") ? 1 : 2)]];
  const h1 = document.querySelector("h1"); if (!ls || !h1) return;
  const st = document.createElement("style");
  st.textContent = `.buchlinks{max-width:none!important;margin:.4rem 0 1rem;font-size:.92rem;display:flex;flex-wrap:wrap;gap:.25rem .9rem;align-items:baseline}
.buchlinks b{font-weight:600}.buchlinks a{font-weight:600;text-decoration:underline;text-underline-offset:2px}
.buchlinks a::before{content:"📖 ";display:inline-block;margin-right:.15em}@media print{.buchlinks{display:none}}`;
  document.head.append(st);
  const p = document.createElement("p"); p.className = "buchlinks";
  p.innerHTML = "<b>Im Buch nachlesen:</b> " + ls.map(([t, z]) => `<a href="../buch/${z}">${t}</a>`).join("");
  const lead = h1.nextElementSibling && h1.nextElementSibling.tagName === "P" ? h1.nextElementSibling : h1;
  lead.after(p);
})();
