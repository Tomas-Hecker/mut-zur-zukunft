/* HeCoAir-Seite: Rechner neutral zeigen. Blendet Reform-Vergleiche und Buch-Vorschläge aus,
   die die Rechner der Buch-Homepage zusätzlich zeigen. Rechnet nichts um: Ohne Klick auf „Reform“
   rechnen die Rechner ohnehin mit dem Recht von heute. */
(() => {
  const css = `[data-tab="t_ref"],[data-tab="t_hr"],[data-tab="t_reform"],#t_ref,#t_hr,#t_reform,#zumSteuer,#vorschlag,
#p_mzz,.hc-weg{display:none!important}`;
  document.head.insertAdjacentHTML("beforeend", `<style id="hc-neutral">${css}</style>`);
  const WORT = /\b(Reform|Buch|Buchs|Vorschlag)\b/;
  const SATZ = /[^.!?]*\b(Reform|Buch|Buchs|Vorschlag aus dem Buch)\b[^.!?]*[.!?]\s*/g;
  function aufraeumen() {
    // Gruppe „Rechtsstand: heute / mit der Reform“ im Heizungsrechner
    const rr = document.getElementById("r_reform");
    if (rr) (rr.closest(".grp, .blk") || rr.closest(".seg") || rr).classList.add("hc-weg");
    // Eingabefelder nur für den Vorschlag (z. B. Stunden ohne Netzentgelt)
    document.querySelectorAll("label").forEach(l => { if (/\(Vorschlag\)|Reform:/.test(l.textContent)) (l.closest(".f") || l).classList.add("hc-weg"); });
    // Tabellen: Spalten und Zeilen zur Reform
    document.querySelectorAll("table").forEach(t => {
      const kopf = t.querySelector("thead tr") || t.rows[0]; if (!kopf) return;
      [...kopf.cells].forEach((c, i) => {
        if (!WORT.test(c.textContent)) return;
        [...t.rows].forEach(r => { const z = r.cells[i]; if (z && r.cells.length === kopf.cells.length) z.classList.add("hc-weg"); });
      });
      [...t.rows].forEach(r => { const z = r.cells[0]; if (z && WORT.test(z.textContent)) r.classList.add("hc-weg"); });
    });
    // Balken-Zeilen (z. B. Dämmen und Fenster im Heizungsrechner)
    document.querySelectorAll(".dv .t").forEach(t => { if (WORT.test(t.textContent)) t.parentElement.classList.add("hc-weg"); });
    // Sätze in Ergebnistexten und Hinweisen
    document.querySelectorAll(".verdict, .note, .lead, p, li, figcaption, small").forEach(el => {
      if (el.closest(".hc-kopf, .hc-fuss, .ib-pop, .sitehinweis") || !WORT.test(el.textContent)) return;
      if (el.children.length === 0) { const n = el.textContent.replace(SATZ, "").trim(); if (n !== el.textContent.trim()) { if (n) el.textContent = n; else el.classList.add("hc-weg"); } return; }
      [...el.childNodes].forEach(k => { if (k.nodeType === 3 && SATZ.test(k.textContent)) { SATZ.lastIndex = 0; k.textContent = k.textContent.replace(SATZ, ""); } SATZ.lastIndex = 0; });
      if (el.tagName === "LI" && /^\s*(Vorschlag|Reform)/.test(el.textContent)) el.classList.add("hc-weg");
    });
  }
  let plan = 0;
  const los = () => { cancelAnimationFrame(plan); plan = requestAnimationFrame(() => { mo.disconnect(); aufraeumen(); mo.observe(document.body, { childList: true, subtree: true, characterData: true }); }); };
  const mo = new MutationObserver(los);
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", los); else los();
})();
