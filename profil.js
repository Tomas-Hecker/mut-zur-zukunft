/* Angaben im Browser merken, für alle Rechner gemeinsam (Entwurf).
   Nichts geht an einen Server. Gespeichert wird nur, wenn der Nutzer „Angaben merken“ einschaltet.
   Speicher: localStorage „mzz-profil“ = { an: true, gemeinsam: {km, plz, …}, rechner: { eauto: {…}, … } }
   Einbinden:  <script src="../profil.js"></script>, dann
     const alt = Profil.laden("eauto");            // { eigene: {...}, gemeinsam: {...} } oder null
     Profil.merken("eauto", V, ["km", "plz"]);     // eigene Werte + gemeinsame Felder, nur wenn eingeschaltet
     Profil.leiste(el, { onLoeschen })             // kleine Leiste mit Schalter und „Löschen“ */
(function () {
  const KEY = "mzz-profil";
  const lies = () => { try { return JSON.parse(localStorage.getItem(KEY)) || null; } catch (e) { return null; } };
  const schreib = d => { try { localStorage.setItem(KEY, JSON.stringify(d)); return true; } catch (e) { return false; } };
  const an = () => !!(lies() || {}).an;
  function laden(name) {
    const d = lies(); if (!d || !d.an) return null;
    return { eigene: (d.rechner || {})[name] || null, gemeinsam: d.gemeinsam || {} };
  }
  let plan = 0;
  function merken(name, werte, gemeinsameFelder = []) {
    clearTimeout(plan);
    plan = setTimeout(() => {
      const d = lies(); if (!d || !d.an) return;
      d.rechner = d.rechner || {}; d.gemeinsam = d.gemeinsam || {};
      d.rechner[name] = { ...werte, _stand: new Date().toISOString() };
      gemeinsameFelder.forEach(k => { if (werte[k] !== undefined) d.gemeinsam[k] = werte[k]; });
      schreib(d);
    }, 400);
  }
  function einschalten(ja) { if (ja) schreib({ ...(lies() || {}), an: true }); else loeschen(); }
  function loeschen() { try { localStorage.removeItem(KEY); } catch (e) {} }
  function leiste(el, opt = {}) {
    if (!el) return;
    const css = `.pf{display:flex;flex-wrap:wrap;align-items:center;gap:6px 12px;font-size:12.5px;color:var(--muted,#667)}
.pf label{display:inline-flex;align-items:center;gap:6px;cursor:pointer}.pf input{accent-color:var(--ev,#0b7a5c)}
.pf button{font:inherit;border:0;background:none;color:inherit;text-decoration:underline;cursor:pointer;padding:0}@media print{.pf{display:none}}`;
    if (!document.getElementById("pf-stil")) document.head.insertAdjacentHTML("beforeend", `<style id="pf-stil">${css}</style>`);
    const zeichne = () => {
      el.className = "pf";
      el.innerHTML = `<label><input type="checkbox" ${an() ? "checked" : ""}> Angaben auf diesem Gerät merken</label>`
        + (an() ? `<button type="button">Gemerkte Angaben löschen</button>` : "")
        + `<span class="pf-i" data-info="Eingeschaltet merkt sich dein Browser deine Angaben, auch für die anderen Rechner (zum Beispiel die Kilometer). So musst du sie nur einmal eingeben. Gespeichert wird nur auf diesem Gerät, nichts geht an uns oder an andere. Ausschalten oder „Löschen“ entfernt alles."></span>`;
      el.querySelector("input").onchange = e => { einschalten(e.target.checked); if (e.target.checked && opt.onEin) opt.onEin(); zeichne(); };
      const b = el.querySelector("button"); if (b) b.onclick = () => { loeschen(); zeichne(); opt.onLoeschen && opt.onLoeschen(); };
    };
    zeichne();
  }
  window.Profil = { laden, merken, leiste, an, loeschen };
})();
