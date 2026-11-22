/* Satzumbruch: Ein Satz, der am Zeilenende beginnt und dann umbricht, aber in eine Zeile passen würde,
   beginnt in der nächsten Zeile. Längere Sätze laufen normal weiter. Ebenso ein Satzteil nach Komma, Semikolon,
   Doppelpunkt oder Gedankenstrich, wenn er in der hinteren Hälfte der Zeile beginnt (Wunsch Tomas, 16.11.2026).
   In Überschriften gilt das für jeden Satzteil, egal wo er beginnt: „Gleich satt.“ / „Ganz anders für den Bauch.“ (Wunsch Tomas, 22.11.2026). Läuft beim Laden, bei jeder Größenänderung
   und wenn ein Rechner neue Ergebnisse schreibt. */
(function () {
  "use strict";
  if (!window.ResizeObserver || !window.MutationObserver || !document.createRange) return;
  var SKIP = "script,style,svg,button,label,select,option,textarea,input,code,pre,nav,table,.logo,.sitenav,[data-nosatz]";
  var ABK = /(?:^|[\s(„"])(?:z|B|u|a|d|h|o|g|v|s|S|Nr|ca|bzw|vgl|Mio|Mrd|Tsd|etc|usw|ggf|evtl|inkl|zzgl|Abs|Art|Dr|Prof|St|Std|Min|max|min|rd|bspw|Jh|Kap|Tab|Abb|Anm|sog|gem|lt|Bd|Hrsg|ff|f)\.$/;
  var ENDE = /([.!?…])([“”"»)\]]*)(\s+)(?=[A-ZÄÖÜ„"»(0-9])/g;
  // Zahl und Einheit bleiben zusammen: „17,2 Mrd. €“, „74 von 100“, „4 %“
  var BINDE = /(\d) (?=(?:€|%|Mrd\.|Mio\.|Tsd\.|Prozent|Punkte|Stunden|Jahre|Jahren|Monate|kWh|kW|km|Wp|W)(?![A-Za-zÄÖÜäöüß]))/g;
  var VON = /(\d) von (\d)/g, MRD = /(Mrd\.|Mio\.|Tsd\.) €/g;
  var KOPF = "h1,h2,h3,h4,h5,h6";
  var TEIL = /([,;:])([“”"»)\]]*)(\s+)(?=\S)|(\s)(?=[–—]\s)/g;
  var st = document.createElement("style");
  // Ausgewogener Umbruch (Wunsch Tomas, 22.11.2026): Überschriften und Bildunterschriften ohne einzelnen Rest in der letzten Zeile
  st.textContent = ".sb{display:inline}.sb.on::before{content:'\\A';white-space:pre}"
    + "h1,h2,h3,h4,h5,figcaption,caption{text-wrap:balance;hyphens:manual}p,li,td{text-wrap:pretty}";
  document.head.appendChild(st);

  var blockCache = new WeakMap();
  function istBlock(el) {
    var d = blockCache.get(el);
    if (d === undefined) { d = !/^inline$|^contents$/.test(getComputedStyle(el).display); blockCache.set(el, d); }
    return d;
  }
  function blockVon(node) {
    var el = node.nodeType === 1 ? node : node.parentElement;
    if (!el || el.closest(SKIP)) return null;
    while (el && el !== document.body && !istBlock(el)) el = el.parentElement;
    return el && el !== document.body ? el : null;
  }

  var daten = new WeakMap(); // block -> {sig, ms, w, sichtbar}
  var mo, ro, io;

  function entferneMarker(block) {
    var alt = block.querySelectorAll("span.sb");
    for (var i = 0; i < alt.length; i++) { var p = alt[i].parentNode; p.removeChild(alt[i]); p.normalize(); }
  }

  function vorbereiten(block) {
    var d = daten.get(block);
    var sig = block.textContent;
    if (d && d.sig === sig && d.ms.every(function (m) { return m.isConnected && block.contains(m); })) return d;
    entferneMarker(block);
    var tw = document.createTreeWalker(block, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) { var p = n.parentElement; return p && p.closest(SKIP) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT; }
    });
    var nodes = [], starts = [], text = "", n;
    while ((n = tw.nextNode())) {
      var fest = n.data.replace(BINDE, "$1\u00a0").replace(VON, "$1\u00a0von\u00a0$2").replace(MRD, "$1\u00a0€");
      if (fest !== n.data) n.data = fest;
      nodes.push(n); starts.push(text.length); text += n.data;
    }
    var pos = [], m;
    ENDE.lastIndex = 0;
    while ((m = ENDE.exec(text))) {
      var vor = text.slice(Math.max(0, m.index - 12), m.index + 1);
      if (m[1] === "." && (ABK.test(vor) || /(?:^|\s)\d{1,2}\.$/.test(vor))) continue;
      pos.push(m.index + m[0].length);
    }
    var teil = new Set();
    TEIL.lastIndex = 0;
    while ((m = TEIL.exec(text))) { var q = m.index + m[0].length; if (pos.indexOf(q) < 0) { pos.push(q); teil.add(q); } }
    pos.sort(function (a, b) { return a - b; });
    var ms = [];
    for (var k = pos.length - 1; k >= 0; k--) {
      var p = pos[k], j = nodes.length - 1;
      while (j > 0 && starts[j] > p) j--;
      var node = nodes[j], off = p - starts[j];
      if (off >= node.data.length) continue;
      var rest = off > 0 ? node.splitText(off) : node;
      var sp = document.createElement("span"); sp.className = teil.has(p) ? "sb teil" : "sb"; sp.setAttribute("aria-hidden", "true");
      rest.parentNode.insertBefore(sp, rest);
      ms.unshift(sp);
    }
    d = { sig: block.textContent, ms: ms, w: -1, sichtbar: d ? d.sichtbar : false };
    daten.set(block, d);
    return d;
  }

  function zeilen(rects, lh) {
    var z = [];
    rects.forEach(function (r) {
      for (var i = 0; i < z.length; i++) if (Math.abs(z[i].top - r.top) < lh / 2) { z[i].l = Math.min(z[i].l, r.left); z[i].r = Math.max(z[i].r, r.right); return; }
      z.push({ top: r.top, l: r.left, r: r.right });
    });
    return z;
  }

  function setzen(block) {
    var d = daten.get(block);
    if (!d || !d.ms.length) return;
    var cs = getComputedStyle(block);
    var br = block.getBoundingClientRect();
    var links = br.left + parseFloat(cs.borderLeftWidth) + parseFloat(cs.paddingLeft);
    var W = block.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
    if (W <= 0) return;
    d.w = block.clientWidth;
    var lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.4;
    var kopf = block.matches(KOPF);
    d.ms.forEach(function (m) { m.classList.remove("on"); });
    for (var i = 0; i < d.ms.length; i++) {
      var m = d.ms[i];
      if (!m.isConnected) continue;
      var r = document.createRange();
      r.setStartAfter(m);
      if (i + 1 < d.ms.length && d.ms[i + 1].isConnected) r.setEndBefore(d.ms[i + 1]); else r.setEnd(block, block.childNodes.length);
      var rects = Array.prototype.filter.call(r.getClientRects(), function (x) { return x.width > 0 && x.height > 0; });
      if (!rects.length) continue;
      var z = zeilen(rects, lh);
      if (z.length < 2) continue;
      z.sort(function (a, b) { return a.top - b.top; });
      if (z[0].l <= links + 2) continue; // beginnt schon am Zeilenanfang
      if (m.classList.contains("teil") && !kopf && z[0].l - links < W / 2) continue; // Satzteil: nur aus der hinteren Hälfte der Zeile
      var breite = z.reduce(function (s, x) { return s + (x.r - x.l); }, 0);
      if (breite <= W - 4) m.classList.add("on");
    }
  }

  var offen = new Set(), geplant = false;
  function planen(block) { offen.add(block); if (!geplant) { geplant = true; requestAnimationFrame(abarbeiten); } }
  function abarbeiten() {
    geplant = false;
    var liste = Array.from(offen); offen.clear();
    mo.disconnect();
    liste.forEach(function (b) {
      if (!b.isConnected) return;
      var d = vorbereiten(b);
      if (d.sichtbar && d.ms.length) setzen(b);
    });
    beobachten();
  }

  function aufnehmen(block) {
    if (daten.has(block)) { planen(block); return; }
    daten.set(block, { sig: null, ms: [], w: -1, sichtbar: false });
    io.observe(block); ro.observe(block);
    planen(block);
  }

  function scannen(wurzel) {
    if (wurzel.nodeType === 3) { var b = blockVon(wurzel); if (b) aufnehmen(b); return; }
    if (wurzel.nodeType !== 1 || wurzel.closest(SKIP)) return;
    var tw = document.createTreeWalker(wurzel, NodeFilter.SHOW_TEXT, null), n, gesehen = new Set();
    while ((n = tw.nextNode())) {
      if (!/[.!?…,;:]\S*\s+\S/.test(n.data) && !/[.!?…,;:]["“”»)]*\s*$/.test(n.data) && !/\s[–—]\s/.test(n.data)) continue;
      var b = blockVon(n);
      if (b && !gesehen.has(b)) { gesehen.add(b); aufnehmen(b); }
    }
  }

  io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      var d = daten.get(e.target);
      if (d && e.isIntersecting && !d.sichtbar) { d.sichtbar = true; planen(e.target); }
    });
  }, { rootMargin: "1200px 0px" });
  ro = new ResizeObserver(function (es) {
    es.forEach(function (e) { var d = daten.get(e.target); if (d && d.sichtbar && e.target.clientWidth !== d.w) planen(e.target); });
  });
  mo = new MutationObserver(function (muts) {
    muts.forEach(function (mu) {
      if (mu.type === "characterData") { var b = blockVon(mu.target); if (b) aufnehmen(b); return; }
      var b2 = blockVon(mu.target); if (b2 && daten.has(b2)) planen(b2);
      mu.addedNodes.forEach(scannen);
    });
  });
  function beobachten() { mo.observe(document.body, { childList: true, subtree: true, characterData: true }); }

  // Browser ohne text-wrap: balance (ältere Safari): die Überschrift so schmal wie möglich, ohne eine Zeile mehr zu brauchen
  var BAL = !(window.CSS && CSS.supports && CSS.supports("text-wrap", "balance"));
  var balW = new WeakMap();
  function ausgleichen(h) {
    var w = h.parentElement ? h.parentElement.clientWidth : 0;
    if (!w || balW.get(h) === w) return;
    balW.set(h, w);
    h.style.maxWidth = "";
    var hoehe = h.getBoundingClientRect().height, lh = parseFloat(getComputedStyle(h).lineHeight) || hoehe;
    if (hoehe < lh * 1.5) return;   // eine Zeile: nichts zu tun
    var lo = w / 2, hi = w;
    for (var i = 0; i < 12 && hi - lo > 2; i++) {
      var m = (lo + hi) / 2; h.style.maxWidth = m + "px";
      if (h.getBoundingClientRect().height > hoehe + 1) lo = m; else hi = m;
    }
    h.style.maxWidth = Math.ceil(hi) + "px";
  }
  function alleAusgleichen() { if (BAL) document.querySelectorAll("h1,h2,h3,h4,h5,figcaption,caption").forEach(ausgleichen); }
  if (BAL) { window.addEventListener("resize", alleAusgleichen); window.addEventListener("load", alleAusgleichen); }

  function start() {
    scannen(document.body);
    beobachten();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { offenAlle(); alleAusgleichen(); });
  }
  function offenAlle() { document.querySelectorAll("p,li,div,dd,figcaption,blockquote,h1,h2,h3,h4,h5,h6").forEach(function (b) { var d = daten.get(b); if (d && d.sichtbar) { d.w = -1; planen(b); } }); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
