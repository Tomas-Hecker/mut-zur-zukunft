/* Info-Knöpfe für alle Rechner: ein kleines „i“ neben Eingabefeld, Kachel, Tabellenzeile oder Überschrift.
   Ein Klick zeigt eine Erklärung in einfachen Worten und, wenn es eine gibt, den Link zur passenden Stelle im Buch.
   Einbinden:  <script src="../info.js"></script>  (Datei im Hauptordner), dann zum Beispiel
     Info.felder({ km: ["Wie viele Kilometer du im Jahr fährst …", "kapitel-10.html#strom-zu-hause", "Kapitel 10"] });
       Schlüssel = id des Eingabefelds (mit oder ohne „i_“ davor); der Knopf kommt an sein <label>.
     Info.texte("#tiles", { "Ertrag am Modul": ["…"] });
       Schlüssel = Anfang des Texts einer Kachel-Überschrift, Tabellenzelle, Überschrift oder eines Labels im Bereich.
       Der Bereich darf sich neu aufbauen: die Knöpfe kommen von selbst wieder.
   Eintrag: [Erklärung, Buchstelle (Datei#Anker im Ordner buch/, oder volle Adresse), Name der Buchstelle].
   Die Erklärung darf einfaches HTML enthalten (<b>, <br>).
   Ohne Skript geht es auch mit Attributen:  <span data-info="Erklärtext" data-buch="kapitel-5.html#anker" data-buchname="Kapitel 5">Titel</span>
     Der Knopf kommt ans Ende des Elements, auch wenn es später neu eingefügt wird. */
(function () {
  const BASIS = new URL("buch/", document.currentScript.src).href;
  const css = `
.ib{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;margin-left:5px;padding:0;border-radius:50%;
  border:1.5px solid currentColor;background:transparent;color:var(--muted,#667);font:700 11px/1 Georgia,serif;font-style:italic;cursor:pointer;
  vertical-align:middle;flex:none;opacity:.75;text-transform:none;letter-spacing:0}
.ib:hover,.ib:focus-visible,.ib[aria-expanded="true"]{opacity:1;color:var(--accent,#0b7a5c);outline:none}
.ib:focus-visible{box-shadow:0 0 0 3px rgba(11,122,92,.3)}
.ib-pop{position:absolute;z-index:1000;max-width:min(360px,calc(100vw - 24px));padding:12px 30px 12px 14px;border-radius:10px;
  background:var(--card,#fff);color:var(--fg,#1d2321);border:1px solid var(--line,#d9ddd8);box-shadow:0 8px 28px rgba(0,0,0,.18);
  font:400 14px/1.45 "Source Sans 3",system-ui,sans-serif;text-align:left;text-transform:none;letter-spacing:0;font-weight:400;white-space:normal}
.ib-pop p{margin:0}.ib-pop a{display:inline-block;margin-top:8px;font-weight:600;color:var(--accent,#0b7a5c)}
.ib-pop .x{position:absolute;top:4px;right:6px;border:0;background:none;font-size:18px;line-height:1;color:var(--muted,#667);cursor:pointer;padding:4px}
@media print{.ib,.ib-pop{display:none!important}}`;
  document.head.insertAdjacentHTML("beforeend", `<style id="ib-stil">${css}</style>`);

  let pop = null, offen = null;
  function zu() { if (pop) pop.remove(); pop = null; if (offen) { offen.setAttribute("aria-expanded", "false"); offen = null; } }
  function auf(btn, e) {
    if (offen === btn) { zu(); return; }
    zu(); offen = btn; btn.setAttribute("aria-expanded", "true");
    const [txt, buch, name] = e;
    pop = document.createElement("div"); pop.className = "ib-pop"; pop.setAttribute("role", "dialog");
    const href = buch ? (/^https?:/.test(buch) ? buch : BASIS + buch) : "";
    pop.innerHTML = `<button class="x" type="button" aria-label="Schließen">×</button><p>${txt}</p>`
      + (href ? `<a href="${href}" target="_blank" rel="noopener">Mehr im Buch${name ? ": " + name : ""} ›</a>` : "");
    document.body.append(pop);
    const r = btn.getBoundingClientRect(), w = pop.offsetWidth, sx = window.scrollX, sy = window.scrollY;
    let x = r.left + sx - 12; x = Math.max(sx + 12, Math.min(x, sx + document.documentElement.clientWidth - w - 12));
    let y = r.bottom + sy + 6;
    if (r.bottom + pop.offsetHeight + 12 > window.innerHeight && r.top > pop.offsetHeight + 12) y = r.top + sy - pop.offsetHeight - 6;
    pop.style.left = x + "px"; pop.style.top = y + "px";
    pop.querySelector(".x").onclick = () => { const b = offen; zu(); b && b.focus(); };
  }
  document.addEventListener("click", ev => { if (pop && !pop.contains(ev.target) && !ev.target.classList.contains("ib")) zu(); });
  document.addEventListener("keydown", ev => { if (ev.key === "Escape" && offen) { const b = offen; zu(); b.focus(); } });
  window.addEventListener("resize", zu);

  function knopf(e, titel) {
    const b = document.createElement("button"); b.type = "button"; b.className = "ib"; b.textContent = "i";
    b.setAttribute("aria-label", "Erklärung" + (titel ? ": " + titel : "")); b.setAttribute("aria-expanded", "false");
    b.addEventListener("click", ev => { ev.preventDefault(); ev.stopPropagation(); auf(b, e); });
    return b;
  }
  const text = el => [...el.childNodes].filter(n => !(n.classList && n.classList.contains("ib"))).map(n => n.textContent).join("").replace(/\s+/g, " ").trim();

  function felder(map) {
    for (const [k, e] of Object.entries(map)) {
      const el = document.getElementById(k) || document.getElementById("i_" + k); if (!el) continue;
      const lab = document.querySelector(`label[for="${el.id}"]`) || el.closest("label") || el.closest(".f")?.querySelector("label");
      if (!lab || lab.querySelector(":scope > .ib")) continue;
      lab.append(knopf(e, text(lab)));
    }
  }
  const SEL = ".k, th, td:first-child, h2, h3, h4, label, .t, summary, .lbl, dt";
  function texte(root, map) {
    const box = typeof root === "string" ? document.querySelector(root) : root; if (!box) return;
    const keys = Object.keys(map).sort((a, b) => b.length - a.length);
    const setze = () => {
      [...(box.matches(SEL) ? [box] : []), ...box.querySelectorAll(SEL)].forEach(el => {
        if (el.querySelector(":scope > .ib") || el.closest("[data-noinfo], .sb")) return;
        const t = text(el); if (!t) return;
        const k = keys.find(k => t.startsWith(k)); if (k === undefined) return;
        // in eine <b>/<span>-Überschrift einer Kachel hinein, sonst ans Ende
        el.append(knopf(map[k], t));
      });
    };
    setze();
    let plan = 0;
    new MutationObserver(m => { if (m.some(x => [...x.addedNodes].some(n => !(n.classList && (n.classList.contains("ib") || n.classList.contains("ib-pop")))))) { cancelAnimationFrame(plan); plan = requestAnimationFrame(setze); } })
      .observe(box, { childList: true, subtree: true });
  }
  function attribute() {
    document.querySelectorAll("[data-info]").forEach(el => {
      if (el.querySelector(":scope > .ib")) return;
      el.append(knopf([el.dataset.info, el.dataset.buch || "", el.dataset.buchname || ""], text(el)));
    });
  }
  const start = () => {
    attribute(); let plan = 0;
    new MutationObserver(m => { if (m.some(x => [...x.addedNodes].some(n => n.nodeType === 1 && (n.matches("[data-info]") || n.querySelector("[data-info]"))))) { cancelAnimationFrame(plan); plan = requestAnimationFrame(attribute); } })
      .observe(document.body, { childList: true, subtree: true });
  };
  if (document.body) start(); else document.addEventListener("DOMContentLoaded", start);
  window.Info = { felder, texte, attribute, zu };
})();
