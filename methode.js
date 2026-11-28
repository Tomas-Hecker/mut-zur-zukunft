/* „So wird gerechnet“: ein Knopf unter dem Ergebnis öffnet die Annahmen des Rechners mit den Werten, die gerade gelten.
   Im PDF (Drucken) steht der Abschnitt immer mit drin.
   Einbinden:  <script src="../methode.js"></script>, dann
     Methode.an(document.getElementById("verdict"), () => [["Überschrift", ["Punkt", "Punkt"]], …]);
     Methode.neu();   // am Ende jeder Rechnung, damit die Werte stimmen */
(function () {
  const css = `
.mt-knopf{display:inline-flex;align-items:center;gap:6px;margin:2px 0 0;padding:5px 12px;border-radius:999px;border:1px solid var(--line,#c9cfcb);
  background:var(--card,#fff);color:var(--ink,#1d2321);font:600 13px/1.2 "Source Sans 3",system-ui,sans-serif;cursor:pointer;justify-self:start}
.mt-knopf:hover,.mt-knopf[aria-expanded="true"]{border-color:var(--acc,var(--accent,#0b7a5c))}
.mt-knopf b{display:inline-flex;align-items:center;justify-content:center;width:16px;height:16px;border-radius:50%;border:1.5px solid currentColor;
  font:700 10px/1 Georgia,serif;font-style:italic}
.methode{background:#fff;color:#1d2321;color-scheme:light;border:1px solid #c9cfcb;border-radius:12px;padding:14px 16px;
  font:400 14px/1.45 "Source Sans 3",system-ui,sans-serif;position:relative}
.methode[hidden]{display:none}
.methode h3{margin:0 28px 8px 0;font:700 16px/1.25 Archivo,system-ui,sans-serif;color:#1d2321}
.methode h4{margin:12px 0 4px;font:700 14px/1.3 Archivo,system-ui,sans-serif;color:#0b6b51}
.methode ul{margin:0;padding-left:18px}.methode li{margin:2px 0;color:#1d2321}.methode b{color:#1d2321}
.methode .mt-zu{position:absolute;top:6px;right:8px;border:0;background:none;font-size:20px;line-height:1;color:#4a5550;cursor:pointer;padding:4px}
@media (min-width:900px){.methode .mt-spalten{columns:2;column-gap:24px}.methode .mt-spalten > div{break-inside:avoid}}
@media print{.methode,.methode[hidden]{display:block!important;break-inside:auto;border:1px solid #999}.mt-knopf,.methode .mt-zu{display:none!important}
  .methode .mt-spalten{columns:1}}`;
  document.head.insertAdjacentHTML("beforeend", `<style id="mt-stil">${css}</style>`);
  let box = null, knopf = null, quelle = null;
  function neu() {
    if (!box || !quelle) return;
    let teile = []; try { teile = quelle() || []; } catch (e) { return; }
    box.querySelector(".mt-spalten").innerHTML = teile.map(([t, l]) => `<div><h4>${t}</h4><ul>${l.filter(Boolean).map(x => `<li>${x}</li>`).join("")}</ul></div>`).join("");
  }
  function an(nach, fn, titel) {
    quelle = fn;
    knopf = document.createElement("button"); knopf.type = "button"; knopf.className = "mt-knopf";
    knopf.innerHTML = "<b>i</b>So wird gerechnet: Simulation und Annahmen"; knopf.setAttribute("aria-expanded", "false");
    box = document.createElement("div"); box.className = "methode"; box.id = "methode"; box.hidden = true;
    box.innerHTML = `<button type="button" class="mt-zu" aria-label="Schließen">×</button><h3>${titel || "So wird gerechnet"}</h3><div class="mt-spalten"></div>`;
    nach.after(knopf); knopf.after(box);
    const setze = auf => { box.hidden = !auf; knopf.setAttribute("aria-expanded", String(auf)); if (auf) neu(); };
    knopf.onclick = () => setze(box.hidden);
    box.querySelector(".mt-zu").onclick = () => { setze(false); knopf.focus(); };
    addEventListener("beforeprint", neu);
    neu();
  }
  window.Methode = { an, neu };
})();
