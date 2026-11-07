// Online-Buch: Inhalt-Menü am Handy, aktiver Abschnitt im Randverzeichnis, Suche.
(function () {
  var lay = document.querySelector('.blayout');
  var btn = document.querySelector('.tocbtn');
  if (btn && lay) {
    btn.addEventListener('click', function () {
      var open = lay.classList.toggle('open');
      btn.setAttribute('aria-expanded', open);
      btn.textContent = open ? 'Schließen' : 'Inhalt';
      document.body.style.overflow = open ? 'hidden' : '';
    });
    var sc = lay.querySelector('.sideclose');
    if (sc) sc.addEventListener('click', function () { btn.click(); btn.focus(); });
    lay.querySelectorAll('.bside a').forEach(function (a) {
      a.addEventListener('click', function () {
        if (lay.classList.contains('open')) { btn.click(); }
      });
    });
  }

  // Aktuelles Kapitel im Randverzeichnis sichtbar machen
  var side = document.querySelector('.bside'), cur = document.querySelector('.btoc li.cur');
  if (side && cur && window.innerWidth >= 1000) side.scrollTop = Math.max(0, cur.offsetTop - 120);

  // Aktuellen Abschnitt markieren
  var links = {};
  document.querySelectorAll('.btoc .sub a').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
  var heads = Array.prototype.slice.call(document.querySelectorAll('.btext h2[id]'));
  if (heads.length && 'IntersectionObserver' in window) {
    var on = null;
    var obs = new IntersectionObserver(function () {
      var cur = null;
      heads.forEach(function (h) { if (h.getBoundingClientRect().top < 140) cur = h; });
      if (on) on.classList.remove('on');
      on = cur && links[cur.id];
      if (on) on.classList.add('on');
    }, { rootMargin: '0px 0px -60% 0px', threshold: [0, 1] });
    heads.forEach(function (h) { obs.observe(h); });
  }

  // Suche
  var list = document.getElementById('treffer');
  if (!list) return;
  var input = document.getElementById('q');
  var info = document.getElementById('treffer-info');
  function norm(s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/ß/g, 'ss'); }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var idx = null;
  function prep() {
    if (idx || !window.BUCH_INDEX) return;
    idx = window.BUCH_INDEX.map(function (e) { return { e: e, n: norm(e.t + ' ' + e.x), nt: norm(e.t) }; });
  }
  function snippet(text, words) {
    var n = norm(text), pos = -1;
    for (var i = 0; i < words.length && pos < 0; i++) pos = n.indexOf(words[i]);
    var a = Math.max(0, pos - 80), b = Math.min(text.length, a + 240);
    var s = (a ? '… ' : '') + text.slice(a, b) + (b < text.length ? ' …' : '');
    var out = esc(s);
    words.forEach(function (w) {
      if (w.length < 2) return;
      var re = new RegExp('(' + w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
      out = out.replace(re, '<mark>$1</mark>');
    });
    return out;
  }
  function run() {
    prep();
    var q = (input.value || '').trim();
    var url = new URL(location.href); url.searchParams.set('q', q); history.replaceState(null, '', url);
    list.innerHTML = '';
    if (!q) { info.textContent = 'Gib ein Wort ein, zum Beispiel „Existenzminimum“, „Erbschaft“ oder „Pflege“.'; return; }
    if (!idx) { info.textContent = 'Suche wird geladen …'; return; }
    var words = norm(q).split(/\s+/).filter(Boolean);
    var hits = idx.filter(function (r) { return words.every(function (w) { return r.n.indexOf(w) >= 0; }); });
    hits.sort(function (a, b) {
      var sa = words.filter(function (w) { return a.nt.indexOf(w) >= 0; }).length;
      var sb = words.filter(function (w) { return b.nt.indexOf(w) >= 0; }).length;
      if (sb !== sa) return sb - sa;
      return (a.e.p === 'quellen') - (b.e.p === 'quellen');
    });
    info.textContent = hits.length ? hits.length + (hits.length === 1 ? ' Abschnitt gefunden' : ' Abschnitte gefunden') : 'Nichts gefunden. Versuch ein anderes Wort.';
    hits.slice(0, 60).forEach(function (r) {
      var e = r.e, li = document.createElement('li');
      li.innerHTML = '<a href="' + e.p + '.html' + (e.i ? '#' + e.i : '') + '">' + esc(e.t) + '</a>' +
        (e.t !== e.k ? '<div class="wo">' + esc(e.k) + '</div>' : '') + '<p>' + snippet(e.x, words) + '</p>';
      list.appendChild(li);
    });
  }
  var q0 = new URL(location.href).searchParams.get('q') || '';
  input.value = q0;
  var t;
  input.addEventListener('input', function () { clearTimeout(t); t = setTimeout(run, 150); });
  input.form.addEventListener('submit', function (ev) { ev.preventDefault(); run(); });
  if (window.BUCH_INDEX) run(); else window.addEventListener('load', run);
})();
