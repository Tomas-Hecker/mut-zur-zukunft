/* Satzumbruch: Ein Satz, der am Zeilenende beginnt und dann umbricht, aber in eine Zeile passen würde,
   beginnt in der nächsten Zeile. Längere Sätze laufen normal weiter. Läuft beim Laden, bei jeder Größenänderung
   und wenn ein Rechner neue Ergebnisse schreibt. */
(function () {
  "use strict";
  if (!window.ResizeObserver || !window.MutationObserver || !document.createRange) return;
  var SKIP = "script,style,svg,button,label,select,option,textarea,input,code,pre,nav,h1,h2,h3,h4,h5,h6,table,.logo,.sitenav,[data-nosatz]";
  var ABK = /(?:^|[\s(„"])(?:z|B|u|a|d|h|o|g|v|s|S|Nr|ca|bzw|vgl|Mio|Mrd|Tsd|etc|usw|ggf|evtl|inkl|zzgl|Abs|Art|Dr|Prof|St|Std|Min|max|min|rd|bspw|Jh|Kap|Tab|Abb|Anm|sog|gem|lt|Bd|Hrsg|ff|f)\.$/;
  var ENDE = /([.!?…])([“”"»)\]]*)(\s+)(?=[A-ZÄÖÜ„"»(0-9])/g;
  var st = document.createElement("style");
  st.textContent = ".sb{display:inline}.sb.on::before{content:'\\A';white-space:pre}";
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
    while ((n = tw.nextNode())) { nodes.push(n); starts.push(text.length); text += n.data; }
    var pos = [], m;
    ENDE.lastIndex = 0;
    while ((m = ENDE.exec(text))) {
      var vor = text.slice(Math.max(0, m.index - 12), m.index + 1);
      if (m[1] === "." && (ABK.test(vor) || /(?:^|\s)\d{1,2}\.$/.test(vor))) continue;
      pos.push(m.index + m[0].length);
    }
    var ms = [];
    for (var k = pos.length - 1; k >= 0; k--) {
      var p = pos[k], j = nodes.length - 1;
      while (j > 0 && starts[j] > p) j--;
      var node = nodes[j], off = p - starts[j];
      if (off >= node.data.length) continue;
      var rest = off > 0 ? node.splitText(off) : node;
      var sp = document.createElement("span"); sp.className = "sb"; sp.setAttribute("aria-hidden", "true");
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
      if (!/[.!?…]\S*\s+\S/.test(n.data) && !/[.!?…]["“”»)]*\s*$/.test(n.data)) continue;
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

  function start() {
    scannen(document.body);
    beobachten();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(offenAlle);
  }
  function offenAlle() { document.querySelectorAll("p,li,div,dd,figcaption,blockquote").forEach(function (b) { var d = daten.get(b); if (d && d.sichtbar) { d.w = -1; planen(b); } }); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
