// Online-Hefte: Seiten an die Breite anpassen, aktives Kapitel im Inhalt markieren.
(function () {
  var heft = document.querySelector('.heft');
  if (!heft) return;
  var pages = heft.querySelectorAll('.page');
  if (!pages.length) return;
  var mm = pages[0].offsetWidth || 794; // 210 mm in CSS-Pixeln
  function fit() {
    var w = heft.clientWidth - (window.innerWidth < 600 ? 12 : 40);
    var z = Math.min(1.15, w / mm);
    heft.style.setProperty('--z', z.toFixed(4));
  }
  fit();
  window.addEventListener('resize', fit);

  // Sprung zu #anker nach dem Anpassen der Größe erneut ausführen
  if (location.hash) {
    var t = document.getElementById(location.hash.slice(1));
    if (t) setTimeout(function () { t.scrollIntoView(); }, 60);
  }

  // Aktives Kapitel im Randverzeichnis
  var links = Array.prototype.slice.call(document.querySelectorAll('.btoc a[href^="#p"]'));
  var starts = links.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });
  var on = null, tick = false;
  function mark() {
    tick = false;
    var cur = null;
    for (var i = 0; i < starts.length; i++) {
      if (starts[i] && starts[i].getBoundingClientRect().top < 160) cur = links[i];
    }
    if (cur === on) return;
    if (on) on.classList.remove('on');
    on = cur;
    if (on) on.classList.add('on');
  }
  window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(mark); } }, { passive: true });
  mark();
})();
