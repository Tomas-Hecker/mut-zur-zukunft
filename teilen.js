/* Teilen (Wunsch Tomas, 22.11.2026): Ein Knopf mit data-teilen teilt eine Seite mit einem Tipp. Auf dem Handy öffnet sich das
   Teilen-Menü des Geräts (WhatsApp, Signal, E-Mail …), sonst eine kleine Auswahl: WhatsApp, E-Mail, Telegram, Link kopieren.
   data-url (Standard: diese Seite), data-titel, data-text. Keine Daten an Dritte, bevor jemand eine Auswahl antippt. */
(function () {
  "use strict";
  var st = document.createElement("style");
  st.textContent = ".teilen-menue{position:absolute;z-index:50;min-width:220px;background:var(--bg,#fff);color:var(--fg,#111);border:1px solid var(--line,#ccc);"
    + "border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.18);padding:6px;font-family:var(--font-body,system-ui)}"
    + ".teilen-menue a,.teilen-menue button{display:flex;align-items:center;gap:10px;width:100%;padding:10px 12px;border:0;background:none;color:inherit;"
    + "font:inherit;font-weight:600;text-align:left;text-decoration:none;border-radius:10px;cursor:pointer}"
    + ".teilen-menue a:hover,.teilen-menue button:hover,.teilen-menue a:focus-visible,.teilen-menue button:focus-visible{background:rgba(127,127,127,.15);outline:none}"
    + ".teilen-menue svg{width:20px;height:20px;flex:none}";
  document.head.appendChild(st);
  var ICON = {
    wa: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.3-.4.8-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.5-.3z"/></svg>',
    mail: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    tg: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.9 4.3 18.8 19c-.2 1-.8 1.3-1.7.8l-4.7-3.5-2.3 2.2c-.3.3-.5.5-1 .5l.3-4.8 8.8-8c.4-.3-.1-.5-.6-.2L6.8 12.9l-4.6-1.4c-1-.3-1-1 .2-1.5L20.6 3c.8-.3 1.6.2 1.3 1.3z"/></svg>',
    link: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/></svg>',
    mehr: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/></svg>'
  };
  var offen = null;
  function zu() { if (offen) { offen.m.remove(); offen.k.setAttribute("aria-expanded", "false"); offen = null; } }
  function daten(k) {
    return { url: new URL(k.getAttribute("data-url") || location.href.split("#")[0], location.href).href,
             titel: k.getAttribute("data-titel") || document.title, text: k.getAttribute("data-text") || "" };
  }
  function menue(k) {
    var d = daten(k), e = encodeURIComponent, satz = (d.text ? d.text + " " : "") + d.url;
    var m = document.createElement("div");
    m.className = "teilen-menue"; m.setAttribute("role", "menu"); m.setAttribute("aria-label", "Teilen");
    m.innerHTML = '<a role="menuitem" target="_blank" rel="noopener" href="https://wa.me/?text=' + e(satz) + '">' + ICON.wa + "WhatsApp</a>"
      + '<a role="menuitem" href="mailto:?subject=' + e(d.titel) + "&body=" + e((d.text ? d.text + "\n\n" : "") + d.url) + '">' + ICON.mail + "E-Mail</a>"
      + '<a role="menuitem" target="_blank" rel="noopener" href="https://t.me/share/url?url=' + e(d.url) + "&text=" + e(d.text || d.titel) + '">' + ICON.tg + "Telegram</a>"
      + '<button type="button" role="menuitem" data-a="kopieren">' + ICON.link + "Link kopieren</button>"
      + (navigator.share ? '<button type="button" role="menuitem" data-a="mehr">' + ICON.mehr + "Weitere Möglichkeiten</button>" : "");
    document.body.appendChild(m);
    var r = k.getBoundingClientRect(), w = m.offsetWidth;
    m.style.top = (window.scrollY + r.bottom + 6) + "px";
    m.style.left = Math.max(8, Math.min(window.scrollX + r.left, window.scrollX + document.documentElement.clientWidth - w - 8)) + "px";
    m.addEventListener("click", function (ev) {
      var b = ev.target.closest("button,a"); if (!b) return;
      if (b.getAttribute("data-a") === "kopieren") {
        ev.preventDefault();
        var fertig = function () { b.lastChild.textContent = "Link kopiert"; setTimeout(zu, 900); };
        if (navigator.clipboard) navigator.clipboard.writeText(d.url).then(fertig, function () { prompt("Link zum Kopieren:", d.url); zu(); });
        else { prompt("Link zum Kopieren:", d.url); zu(); }
      } else if (b.getAttribute("data-a") === "mehr") {
        ev.preventDefault(); zu(); navigator.share({ title: d.titel, text: d.text, url: d.url }).catch(function () {});
      } else setTimeout(zu, 50);
    });
    offen = { m: m, k: k }; k.setAttribute("aria-expanded", "true");
    var erstes = m.querySelector("a,button"); if (erstes) erstes.focus();
  }
  document.addEventListener("click", function (ev) {
    var k = ev.target.closest("[data-teilen]");
    if (!k) { if (offen && !offen.m.contains(ev.target)) zu(); return; }
    ev.preventDefault();
    if (offen && offen.k === k) { zu(); return; }
    zu();
    var d = daten(k);
    // Handy und Tablet: gleich das Teilen-Menü des Geräts
    if (navigator.share && window.matchMedia && matchMedia("(pointer: coarse)").matches) {
      navigator.share({ title: d.titel, text: d.text, url: d.url }).catch(function (err) { if (!err || err.name !== "AbortError") menue(k); });
      return;
    }
    menue(k);
  });
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape" && offen) { var k = offen.k; zu(); k.focus(); } });
  window.addEventListener("resize", zu);
})();
