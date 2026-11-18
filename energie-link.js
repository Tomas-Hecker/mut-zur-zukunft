/* Ersparnis eines Rechners in den Steuerrechner übernehmen (Entwurf).
   Wurde der Rechner aus dem Steuerrechner geöffnet, geht die Zahl per Nachricht an dieses Fenster zurück;
   sonst öffnet der Knopf den Steuerrechner mit der Zahl im Link. Gespeichert wird nichts. */
(function () {
  const eur = x => Math.round(x).toLocaleString("de-DE") + " €";
  const sign = x => (x >= 0.5 ? "+" : x <= -0.5 ? "−" : "") + eur(Math.abs(x));
  function senden(d) {
    const op = window.opener;
    try {
      if (op && !op.closed && op.location.origin === location.origin && op.location.pathname.includes("/steuerrechner/")) {
        op.postMessage({ typ: "energie-ersparnis", heute: d.heute, reform: d.reform, quelle: d.quelle }, location.origin);
        op.focus(); return "zurück";
      }
    } catch (e) {}
    const q = new URLSearchParams({ eHeute: Math.round(d.heute), eReform: Math.round(d.reform), eQuelle: d.quelle });
    location.href = "../steuerrechner/?" + q + "#energieBox"; return "neu";
  }
  window.ZumSteuerrechner = {
    zeige(el, d) {   // d: { quelle, heute, reform, was }
      if (!el) return;
      el.className = "zumsteuer";
      el.innerHTML = `<h3>Was das im Jahr bringt, heute und mit der Reform</h3>
        <p>${d.was}: <b>heute ${sign(d.heute)}</b> im Jahr, <b>mit der Reform ${sign(d.reform)}</b>. Mittel über die Laufzeit.</p>
        <p class="note">Reform = Vorschlag aus dem Buch, kein geltendes Recht. ${d.reformText || ""}</p>
        <button type="button" class="zumsteuer-knopf">Ersparnis in den Steuerrechner übernehmen</button> <span class="zumsteuer-ok" role="status"></span>`;
      el.querySelector("button").onclick = () => { const w = senden(d); if (w === "zurück") el.querySelector(".zumsteuer-ok").textContent = "Übernommen. Der Steuerrechner zeigt sie jetzt im Kasten „Energie und Auto“."; };
    },
  };
  const st = document.createElement("style");
  st.textContent = ".zumsteuer{margin:18px 0;padding:14px 16px;border:1px solid var(--line,#ddd);border-radius:12px}.zumsteuer h3{margin:0 0 6px;font-size:1rem}.zumsteuer p{margin:4px 0}.zumsteuer-knopf{margin-top:8px;padding:8px 14px;border-radius:999px;border:1px solid currentColor;background:transparent;color:inherit;font:inherit;font-weight:600;cursor:pointer}.zumsteuer-ok{font-size:.85rem;margin-left:8px}@media print{.zumsteuer-knopf{display:none}}";
  document.head.append(st);
})();
