/* Steuerrechner: Direktlinks mit Voreinstellung und Links ins Buch.
   Läuft als letztes Skript vor </body>, nach dem Hauptskript (nutzt BEISPIELE, SAN_BSP, setForm, renderPresets,
   updateHH, sanSetze, sanPresets, updateSan, updateGesamt, updateCO2, aktiv, sanAktiv, szenario, C bzw. A.CO2).

   Adressen, die das Buch verwendet (alle optional, beliebig kombinierbar):
     ?bsp=facharbeiter#haushalt          Beispielhaushalt wählen (Kurzname wie in BUCH.beispiele)
     ?lohn1=48000&std1=40&kinder=2       einzelne Felder, Beträge im Jahr wie in BEISPIELE
     ?sz=vorsichtig#staat                Szenario der Schuldengrafik (vorsichtig, mittel, zuversichtlich, basis)
     ?san=wohnung-aus-dem-buch#sanierung Sanierungsbeispiel
     ?co2=2030#co2                       Jahr im CO2-Pfad
     ?buch=kapitel-4.html%23wer-zahlt-wie-viel   zeigt oben „Zurück ins Buch“
*/
(() => {
  "use strict";
  const BUCHPFAD = "../buch/";

  /* ---------- Linkliste: Rechner -> Buch. Nur hier pflegen. ---------- */
  const BUCH = {
    // Abschnitte des Rechners: [Text, Ziel] ...
    abschnitte: {
      idee:      [["Kapitel 4: Der Grundgedanke", "kapitel-4.html#grundgedanke"], ["So hoch ist die Steuer", "kapitel-4.html#steuersatz"], ["Anhang A1: Was als investiert gilt", "anhang-a.html#a1"]],
      haushalt:  [["Kapitel 2: Was die Reform dir bringt", "kapitel-2.html"], ["Kapitel 4: Wer heute wie viel zahlt", "kapitel-4.html#wer-zahlt-wie-viel"], ["Anhang C3: Zehn Haushalte durchgerechnet", "anhang-c.html#c3"]],
      staat:     [["Kapitel 6: Können wir uns das leisten?", "kapitel-6.html#leisten"], ["Drei Szenarien", "kapitel-6.html#szenarien"], ["Der Zukunftsplan", "kapitel-6.html#zukunftsplan"], ["Anhang C10: Alle Annahmen", "anhang-c.html#c10"]],
      co2:       [["Kapitel 5: Weitere Maßnahmen", "kapitel-5.html#co2"], ["Anhang B7: CO₂-Preis und Klimageld", "anhang-b.html#b7"]],
      sanierung: [["Kapitel 5: Wärmepumpe mit zinslosem Kredit", "kapitel-5.html#waermepumpe"], ["Anhang B5: Wohnen, Wärme und Strom", "anhang-b.html#b5"]],
      fragen:    [["Sechs weitere Sorgen, kurz beantwortet", "auf-einen-blick.html#sorgen"], ["Kapitel 6: Wie belastbar ist die Rechnung?", "kapitel-6.html#belastbar"]],
      quellen:   [["Anhang A: das Steuersystem", "anhang-a.html"], ["Anhang C: die Simulation", "anhang-c.html"], ["Alle Quellen", "quellen.html"]],
    },
    // Beispielhaushalte: Kurzname (für ?bsp=) -> Buchstelle. Reihenfolge wie BEISPIELE im Rechner.
    beispiele: {
      "Grundsicherung":                 ["grundsicherung",   "Kapitel 5: Der Bürgerjob",            "kapitel-5.html#buergerjob"],
      "Bürgerjob":                      ["buergerjob",       "Kapitel 5: Der Bürgerjob",            "kapitel-5.html#buergerjob"],
      "Rentnerin mit Minijob":          ["rentnerin",        "Kapitel 5: Arbeit im Rentenalter",    "kapitel-5.html#arbeit-im-rentenalter"],
      "Alleinerziehende Pflegehelferin":["pflegehelferin",   "Anhang C3: Zehn Haushalte",           "anhang-c.html#c3"],
      "Verkäuferin, Mindestlohn":       ["verkaeuferin",     "Kapitel 4: Wer heute wie viel zahlt", "kapitel-4.html#wer-zahlt-wie-viel"],
      "Facharbeiter":                   ["facharbeiter",     "Kapitel 1: Von 100 € bleiben Jonas 41", "kapitel-1.html#lohn-heute"],
      "Familie, zwei Kinder":           ["familie",          "Kapitel 4: Wer heute wie viel zahlt", "kapitel-4.html#wer-zahlt-wie-viel"],
      "Familie, Tochter studiert":      ["familie-studium",  "Vertiefung: Familie, Tochter studiert", "../vertiefung/rechnung-im-einzelnen.html#nachgerechnet-eine-familie-deren-tochter-studiert"],
      "Handwerksmeister":               ["handwerksmeister", "Kapitel 6: Drei Beispiele", "kapitel-6.html#drei-beispiele"],
      "Führungskraft":                  ["fuehrungskraft",   "Kapitel 6: Drei Beispiele", "kapitel-6.html#drei-beispiele"],
      "Wohlhabender Ruheständler":      ["ruhestaendler",    "Kapitel 6: Drei Beispiele", "kapitel-6.html#drei-beispiele"],
      "Unternehmerin mit GmbH":         ["unternehmerin",    "Kapitel 4: Wer heute wie viel zahlt", "kapitel-4.html#wer-zahlt-wie-viel"],
    },
    sanierung: {
      "Wohnung aus dem Buch": ["wohnung-aus-dem-buch", "Kapitel 5: Wärmepumpe mit zinslosem Kredit", "kapitel-5.html#waermepumpe"],
    },
  };

  const $ = id => document.getElementById(id);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const slug = t => t.toLowerCase().replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const link = ([t, z]) => `<a href="${BUCHPFAD}${esc(z)}">${esc(t)}</a>`;
  const bspKurz = b => (BUCH.beispiele[b.name] || [slug(b.name)])[0];
  const sanKurz = b => (BUCH.sanierung[b.name] || [slug(b.name)])[0];

  /* ---------- Aussehen ---------- */
  const st = document.createElement("style");
  st.textContent = `
.buchlinks{margin:.2rem 0 1rem;font-size:.92rem;color:var(--muted);display:flex;flex-wrap:wrap;gap:.25rem .9rem;align-items:baseline}
.buchlinks b{font-weight:600;color:var(--fg)}
.buchlinks a,.preset-buch a,.zurueck-buch a{color:var(--accent);font-weight:600;text-decoration:underline;text-underline-offset:2px}
.buchlinks a::before,.preset-buch a::before{content:"📖 ";text-decoration:none;display:inline-block;margin-right:.15em}
.preset-buch{margin-top:.35rem;font-size:.9rem}
.zurueck-buch{position:sticky;top:0;z-index:30;background:var(--surface);border-bottom:1px solid var(--line);padding:8px 16px;font-size:.95rem;text-align:center}
.zurueck-buch button{font:inherit;background:none;border:0;color:var(--muted);cursor:pointer;margin-left:.6rem}
.linkkopie{font:inherit;font-weight:600;padding:8px 14px;border-radius:999px;border:1px solid var(--line);background:transparent;color:var(--fg);cursor:pointer}
@media (max-width:480px){.zurueck-buch{font-size:.85rem;padding:6px 10px}}
@media print{.buchlinks,.preset-buch,.zurueck-buch,.linkkopie{display:none!important}}`;
  document.head.append(st);

  /* ---------- 1. Jeder Abschnitt: „Im Buch nachlesen“ ---------- */
  Object.entries(BUCH.abschnitte).forEach(([id, ls]) => {
    const h2 = document.querySelector(`section#${id} h2`); if (!h2) return;
    const p = document.createElement("p"); p.className = "buchlinks"; p.dataset.nosatz = "";
    p.innerHTML = `<b>Im Buch nachlesen:</b> ${ls.map(link).join("")}`;
    const lead = h2.parentElement.querySelector(":scope > p.lead");
    (lead || h2).after(p);
  });

  /* ---------- 2. Beispielhaushalt und Sanierungsbeispiel: Link zur Buchstelle ---------- */
  function notiz(boxId, eintrag) {
    const note = $(boxId); if (!note) return;
    let el = note.nextElementSibling;
    if (!el || !el.classList.contains("preset-buch")) { el = document.createElement("div"); el.className = "preset-buch"; note.after(el); }
    el.innerHTML = eintrag ? `Im Buch nachlesen: ${link([eintrag[1], eintrag[2]])}` : "";
  }
  function adresse() {   // Adresszeile mitführen, damit man jede Rechnung als Link teilen kann
    const q = new URLSearchParams(location.search);
    ["bsp", "san", "sz", "co2"].forEach(k => q.delete(k));
    if (typeof aktiv === "number" && aktiv >= 0 && aktiv !== DEFAULT_BEISPIEL) q.set("bsp", bspKurz(BEISPIELE[aktiv]));
    if (typeof sanAktiv === "number" && sanAktiv > 0) q.set("san", sanKurz(SAN_BSP[sanAktiv]));
    if (typeof szenario === "string" && szenario !== "mittel") q.set("sz", szenario);
    const s = q.toString();
    try { history.replaceState(null, "", location.pathname + (s ? "?" + s : "") + location.hash); } catch (e) {}
  }
  if (typeof renderPresets === "function") {
    const alt = renderPresets;
    renderPresets = function () { alt.apply(this, arguments); notiz("presetNote", aktiv >= 0 ? BUCH.beispiele[BEISPIELE[aktiv].name] : null); adresse(); };
  }
  if (typeof sanPresets === "function") {
    const alt = sanPresets;
    sanPresets = function () { alt.apply(this, arguments); notiz("s_presetNote", sanAktiv >= 0 ? BUCH.sanierung[SAN_BSP[sanAktiv].name] : null); adresse(); };
  }
  if (typeof updateGesamt === "function") {
    const alt = updateGesamt;
    updateGesamt = function () { const r = alt.apply(this, arguments); adresse(); return r; };
  }

  /* ---------- 3. Voreinstellung aus der Adresse ---------- */
  const q = new URLSearchParams(location.search);
  let ziel = null;
  const bsp = q.get("bsp");
  const felder = [...q.keys()].filter(k => document.getElementById(k) && document.getElementById(k).closest("#hhForm"));
  if (bsp || felder.length) {
    const i = bsp ? BEISPIELE.findIndex(b => bspKurz(b) === bsp || slug(b.name) === bsp) : -1;
    const v = i >= 0 ? { ...BEISPIELE[i].v } : {};
    felder.forEach(k => { const x = q.get(k); v[k] = x === "" || x === "ja" ? 1 : x === "nein" ? 0 : parseFloat(x); if (k === "hb" && v[k] > 1) v[k] /= 100; });
    aktiv = felder.length ? -1 : i;
    setForm(v); renderPresets(); updateHH();
    ziel = "haushalt";
  }
  const sz = q.get("sz");
  if (sz && document.querySelector(`#szenarien [data-sz="${CSS.escape(sz)}"]`)) { szenario = sz; updateGesamt(); ziel = ziel || "staat"; }
  const san = q.get("san");
  if (san) {
    const i = SAN_BSP.findIndex(b => sanKurz(b) === san || slug(b.name) === san);
    if (i >= 0) { sanAktiv = i; sanSetze(SAN_BSP[i]); sanPresets(); updateSan(); ziel = ziel || "sanierung"; }
  }
  const co2 = +q.get("co2");
  if (co2) { const b = document.querySelector(`#c_jahre [data-j="${co2}"]`); if (b) { b.click(); ziel = ziel || "co2"; } }
  renderPresets(); sanPresets();

  /* ---------- 4. Wer aus dem Buch kommt, findet zurück ---------- */
  const von = q.get("buch");
  if (von && /^[a-z0-9-]+\.html(#[a-z0-9-]+)?$/.test(von)) {
    const bar = document.createElement("div"); bar.className = "zurueck-buch"; bar.dataset.nosatz = "";
    bar.innerHTML = `Du kommst aus dem Buch. <a href="${BUCHPFAD}${esc(von)}">Zurück zur Buchstelle</a><button type="button" aria-label="Hinweis schließen">✕</button>`;
    bar.querySelector("button").onclick = () => bar.remove();
    document.body.prepend(bar);
    st.textContent += "section.block{scroll-margin-top:48px}";
  }

  /* ---------- 5. Link zu dieser Rechnung kopieren (für eigene Angaben mit allen Feldern) ---------- */
  const knoepfe = document.querySelector("#teilen .knoepfe");
  if (knoepfe) {
    const b = document.createElement("button"); b.type = "button"; b.className = "linkkopie"; b.textContent = "Link zu dieser Rechnung";
    b.onclick = async () => {
      const u = new URL(location.href); u.hash = "haushalt";
      if (aktiv < 0) {
        u.searchParams.delete("bsp");
        const h = readForm();
        Object.entries(h).forEach(([k, x]) => { if (document.getElementById(k) && x) u.searchParams.set(k, typeof x === "boolean" ? 1 : Math.round(x * 100) / 100); });
      }
      try { await navigator.clipboard.writeText(u.href); b.textContent = "Link kopiert"; }
      catch (e) { prompt("Link zu dieser Rechnung:", u.href); }
      setTimeout(() => b.textContent = "Link zu dieser Rechnung", 2500);
    };
    knoepfe.append(b);
  }

  /* ---------- Zum Abschnitt springen, wenn alles gezeichnet ist ---------- */
  const hin = (location.hash || "").slice(1) || ziel;
  if (hin && $(hin)) requestAnimationFrame(() => setTimeout(() => $(hin).scrollIntoView({ block: "start" }), 60));
  if (typeof postHeight === "function") postHeight();
})();
