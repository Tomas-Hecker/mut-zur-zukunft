/* Gemeinsame Annahmen zur Wirtschaftlichkeit für alle Rechner: Zins, Inflation, Energiepreise.
   Vorgaben: Inflation 2 % wie im Buch; Energiepreise steigen mit der Inflation (real gleich, CO₂-Preis und Kilometerabgabe rechnen die Rechner eigens);
   Zins 3,8 % = was Unternehmen im Euroraum im Schnitt für neue Kredite zahlen (EZB, Indikator der Kreditfinanzierungskosten, August 2026: 3,77 %).
   Geändert gelten die Werte für alle Rechner: im Tab (sessionStorage) und, wenn „Angaben merken“ an ist, auch auf dem Gerät (mzz-profil).
   Einbinden:  <script src="../wirtschaft.js"></script>, dann
     Wirtschaft.an(document.querySelector(".col-more"), w => { V.zins = w.zins; V.steig = w.steig; run(); });   // w = { zins, infl, real, steig } in %
     Wirtschaft.werte()   // aktuelle Werte */
(function () {
  const BUCH = { zins: 3.8, infl: 2, real: 0 };
  const SK = "mzz-wirtschaft", PK = "mzz-profil";
  const ok = w => w && ["zins", "infl", "real"].every(k => typeof w[k] === "number" && isFinite(w[k]));
  function lies() {
    try { const p = JSON.parse(localStorage.getItem(PK)); if (p && p.an && p.gemeinsam && ok(p.gemeinsam.wirtschaft)) return p.gemeinsam.wirtschaft; } catch (e) {}
    try { const s = JSON.parse(sessionStorage.getItem(SK)); if (ok(s)) return s; } catch (e) {}
    return { ...BUCH };
  }
  function schreib(w) {
    try { sessionStorage.setItem(SK, JSON.stringify(w)); } catch (e) {}
    try { const p = JSON.parse(localStorage.getItem(PK)); if (p && p.an) { p.gemeinsam = p.gemeinsam || {}; p.gemeinsam.wirtschaft = w; localStorage.setItem(PK, JSON.stringify(p)); } } catch (e) {}
  }
  const mitSteig = w => ({ ...w, steig: Math.round(((1 + w.infl / 100) * (1 + w.real / 100) - 1) * 10000) / 100 });
  let W = lies();
  const werte = () => mitSteig(W);
  const istBuch = () => ["zins", "infl", "real"].every(k => W[k] === BUCH[k]);
  function an(spalte, beiAenderung) {
    if (!spalte) return werte();
    const d = document.createElement("details"); d.className = "wirt"; d.dataset.k = "wirt";
    const F = [["zins", "Zins", "Was Geld kostet, das im Auto, in der Anlage oder in der Heizung steckt: so viel zahlen Unternehmen im Euroraum im Schnitt für neue Kredite (EZB, August 2026: 3,77 %). Künftige Kosten und Ersparnisse werden damit auf ihren heutigen Wert abgezinst."],
      ["infl", "Inflation", "Wie im Buch: 2 % im Jahr. Versicherung, Wartung und andere Preise steigen damit."],
      ["real", "Energiepreise über der Inflation", "Wie viel Strom, Gas, Öl und Sprit im Jahr stärker steigen als die Inflation. Vorgabe 0 %: Sie steigen mit der Inflation. Den steigenden CO₂-Preis und die Kilometerabgabe aus dem Buch rechnen die Rechner zusätzlich."]];
    d.innerHTML = `<summary>Zins, Inflation, Energiepreise</summary>
      <div class="row2">${F.map(([k, l, t]) => `<div class="f"><label for="w_${k}" data-info="${t}">${l}</label><div class="in"><input id="w_${k}" type="number" inputmode="decimal" step="0.1"><span class="u">%</span></div></div>`).join("")}</div>
      <p class="note" id="w_note"></p><button type="button" class="link" id="w_buch" style="font:inherit;font-size:13px;border:0;background:none;color:inherit;text-decoration:underline;cursor:pointer;padding:0">Zurück auf die Annahmen des Buchs</button>`;
    const h = spalte.querySelector("h2, .colT, .blkT");
    if (h) h.after(d); else spalte.prepend(d);
    try { if (sessionStorage.getItem("wi-open") === "1") d.open = true; } catch (e) {}
    d.addEventListener("toggle", () => { try { sessionStorage.setItem("wi-open", d.open ? "1" : "0"); } catch (e) {} });
    const zeige = () => {
      F.forEach(([k]) => { const el = d.querySelector("#w_" + k); if (document.activeElement !== el) el.value = W[k]; });
      const w = werte();
      d.querySelector("#w_note").textContent = `Gilt für alle Rechner. Strom, Gas, Öl und Sprit steigen damit um ${String(w.steig).replace(".", ",")} % im Jahr. ${istBuch() ? "Das sind die Annahmen des Buchs." : "Eigene Werte, gelten auch in den anderen Rechnern."}`;
      d.querySelector("#w_buch").hidden = istBuch();
    };
    F.forEach(([k]) => d.querySelector("#w_" + k).addEventListener("input", e => {
      const x = parseFloat(String(e.target.value).replace(",", ".")); if (!isFinite(x)) return;
      W = { ...W, [k]: x }; schreib(W); zeige(); beiAenderung(werte());
    }));
    d.querySelector("#w_buch").onclick = () => { W = { ...BUCH }; schreib(W); zeige(); beiAenderung(werte()); };
    addEventListener("storage", e => { if (e.key === PK) { W = lies(); zeige(); beiAenderung(werte()); } });
    zeige();
    if (window.Info && Info.attribute) Info.attribute();
    return werte();
  }
  window.Wirtschaft = { an, werte, BUCH };
})();
