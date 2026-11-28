/* Ort nach Postleitzahl: lädt das typische Wetterjahr des Postleitzahlbereichs (erste drei Ziffern).
   Daten: PVGIS 5.3 der Europäischen Kommission (JRC), © Europäische Union, CC BY 4.0;
   Lage der Bereiche aus Ortskoordinaten von GeoNames (CC BY 4.0). Baut: werkzeug/wetter-laden.py */
(function () {
  const BASIS = new URL(".", document.currentScript.src).href;
  let bereiche = null;
  async function ladeBereiche() {
    if (!bereiche) bereiche = await (await fetch(BASIS + "bereiche.json")).json();
    return bereiche;
  }
  // Infos zum Bereich (ohne Stundenwerte): n Ort, lat, lon, z Höhe, tm Jahresmittel, gs Globalstrahlung, th Mittel der Heizzeit, jf Faktor Jahresarbeitszahl
  async function info(plz) {
    const b = String(plz).slice(0, 3), B = await ladeBereiche();
    return /^\d{3}$/.test(b) && B[b] ? { bereich: b, ...B[b] } : null;
  }
  async function bezug() { return (await ladeBereiche())._bezug; }   // Idstein: das Wetter, mit dem die Rechner ohne Postleitzahl rechnen
  async function wetter(plz) {
    const i = await info(plz); if (!i) return null;
    const w = await (await fetch(BASIS + i.bereich + ".json")).json();
    return { ...i, t: w.t.map(v => v / 10), rh: w.rh, g: w.g, d: w.d };
  }
  const quelle = i => `Wetter für den Postleitzahlbereich ${i.bereich}.. (${i.n}, ${String(i.lat).replace(".", ",")}° N, ${String(i.lon).replace(".", ",")}° O, ${i.z} m): `
    + `typisches meteorologisches Jahr aus PVGIS 5.3 der Europäischen Kommission, Strahlung SARAH-3 und Wetter ERA5 2005 bis 2023, © Europäische Union, CC BY 4.0. `
    + `Gerechnet für den größten Ort des Bereichs, Koordinaten von GeoNames (CC BY 4.0). Zeit von UTC auf MEZ umgerechnet.`;
  // Eingabefeld: ruft beimLaden(plz) auf, sobald fünf Ziffern da sind; merkt sich die PLZ im Link (?plz=)
  // info: Erklärung hinter dem Info-Knopf am Feld (braucht info.js)
  function feld(box, beimLaden, text, info) {
    if (!document.getElementById("plzstil")) document.head.insertAdjacentHTML("beforeend", '<style id="plzstil">.plzfeld{grid-column:1/-1}.plzfeld .in{max-width:12em}.plzfeld small{white-space:normal!important;overflow:visible!important}</style>');
    const d = document.createElement("div"); d.className = "f plzfeld";
    d.innerHTML = `<label for="i_plz"${info ? ` data-info="${info.replace(/"/g, "&quot;")}"` : ""}>Postleitzahl</label><div class="in"><input id="i_plz" type="text" inputmode="numeric" autocomplete="postal-code" maxlength="5" pattern="[0-9]{5}" placeholder="z. B. 80331"></div><small id="plz_status">${text || "Lädt das Wetter für deinen Ort."}</small>`;
    box.prepend(d);
    const el = d.querySelector("input"), st = d.querySelector("small");
    let zuletzt = "";
    const los = async () => {
      const p = el.value.replace(/\D/g, "");
      if (p.length !== 5 || p === zuletzt) return;
      zuletzt = p; st.textContent = "Wetter wird geladen …";
      try {
        const r = await beimLaden(p);
        if (!r) { st.textContent = "Diese Postleitzahl kenne ich nicht."; return; }
        st.textContent = `Wetter von ${r.n} (${r.z} m) für die Postleitzahlen ${r.bereich}..`;
        try { const u = new URL(location.href); u.searchParams.set("plz", p); history.replaceState(null, "", u); } catch (e) {}
      } catch (e) { st.textContent = "Das Wetter ließ sich nicht laden."; zuletzt = ""; }
    };
    el.addEventListener("input", los);
    try { const p = new URLSearchParams(location.search).get("plz"); if (p) { el.value = p; los(); } } catch (e) {}
    return el;
  }
  window.Ort = { info, bezug, wetter, quelle, feld };
})();
