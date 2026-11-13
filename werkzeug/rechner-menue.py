"""Setzt auf allen Rechner-Seiten oben dieselbe Menüleiste wie auf der Startseite ein (idempotent).
Aufruf: python3 werkzeug/rechner-menue.py  (aus dem Hauptordner der Homepage)"""
import re, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SEITEN = [('steuerrechner', 'Steuerrechner', False), ('eauto-rechner', 'E-Auto-Rechner', True), ('heizungsrechner', 'Heizung und Dämmung', True), ('energie-rechner', 'Energie-Rechner', True), ('balkon-rechner', 'Balkon-Rechner', True)]
LOGO = '<svg viewBox="0 0 100 100" width="34" height="34" aria-hidden="true"><circle cx="50" cy="50" r="44" fill="none" stroke="#f2b33d" stroke-width="3"/><path d="M30,64 A20,20 0 0 1 70,64 Z" fill="#f2b33d"/><path d="M50,64 L50,33" stroke="#fbf8f1" stroke-width="4" stroke-linecap="round"/><path d="M50,47 C41,46 33,39 31,28 C41,29 48,36 50,47 Z" fill="#9fd8b0"/><path d="M50,40 C57,37 65,30 68,19 C58,20 51,28 50,40 Z" fill="#9fd8b0"/><line x1="17" y1="64" x2="83" y2="64" stroke="#fbf8f1" stroke-width="3.5" stroke-linecap="round"/></svg>'
CSS = '''<style id="sitenav-css">
.sitenav{background:#12372a;color:#fbf8f1;font:600 15px/1.3 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .sitenav{background:#0a1913}}
:root[data-theme="dark"] .sitenav{background:#0a1913}
.sitenav.flush{margin:-28px calc(-1 * max(16px, env(safe-area-inset-left, 0px))) 24px}
.sitenav .sn-in{max-width:1180px;margin:0 auto;padding:10px max(16px, env(safe-area-inset-left, 0px));display:flex;align-items:center;justify-content:space-between;gap:10px 18px;flex-wrap:wrap}
.sitenav a{color:#fbf8f1;text-decoration:none}
.sitenav .sn-logo{display:flex;align-items:center;gap:10px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;font-size:14px}
.sitenav .sn-logo b{color:#f2b33d;font-weight:800}
.sitenav .sn-links{display:flex;align-items:center;gap:4px 16px;flex-wrap:wrap}
.sitenav .sn-links a{padding:5px 0;border-bottom:2px solid transparent}
.sitenav .sn-links a:hover,.sitenav .sn-links a[aria-current]{border-color:#f2b33d}
.sitenav .sn-links a.sn-buch{background:#f2b33d;color:#12372a;border:0;border-radius:999px;padding:6px 14px;font-weight:700}
.sitenav .sn-links a.sn-buch:hover{background:#ffc75a}
.sitenav a:focus-visible{outline:2px solid #f2b33d;outline-offset:3px}
.sitehinweis{max-width:1180px;margin:28px auto 8px;padding:0 max(16px, env(safe-area-inset-left, 0px));font:14px/1.45 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
.sitehinweis p{max-width:none;margin:0;padding:10px 14px;border:1px solid #e0a52b;border-left-width:5px;border-radius:8px;background:#fff6dd;color:#3d2e05}
.sitehinweis b{color:#7a4f00}
.sitehinweis a{color:inherit;text-decoration:underline}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .sitehinweis p{background:#2e2410;color:#f3e6c4;border-color:#a8790f}:root:not([data-theme="light"]) .sitehinweis b{color:#f2b33d}}
:root[data-theme="dark"] .sitehinweis p{background:#2e2410;color:#f3e6c4;border-color:#a8790f}
:root[data-theme="dark"] .sitehinweis b{color:#f2b33d}
.sitenav .sn-links button.sn-druck{font:inherit;color:#fbf8f1;background:none;border:1px solid rgba(251,248,241,.45);border-radius:999px;padding:5px 12px;cursor:pointer}
.sitenav .sn-links button.sn-druck:hover{border-color:#f2b33d}
.druckkopf{display:none}
.teil-druck{font:600 13px system-ui,sans-serif;border:1px solid currentColor;border-radius:999px;padding:4px 12px;background:none;color:inherit;opacity:.75;cursor:pointer;margin:0 0 10px}
.teil-druck:hover{opacity:1}
@media print{
@page{margin:14mm 12mm}
*{-webkit-print-color-adjust:exact;print-color-adjust:exact}
html,body{background:#fff!important}
#quellen,#fragen,#idee{display:none!important}
body.druck-teil main > section:not(.druck-dieser){display:none!important}
body.druck-teil header.top{display:none!important}
.teil-druck{display:none!important}
.sitenav,footer,.mbar,.tip,.ttip,.presets,.seg,button,.sn-druck{display:none!important}
.druckkopf{display:block;font:12px/1.4 system-ui,sans-serif;color:#444;border-bottom:1px solid #999;padding-bottom:6px;margin-bottom:12px}
.panel,.main > .panel{position:static!important;max-height:none!important;overflow:visible!important;box-shadow:none!important}
svg,table,.verdict,.tile,.sitehinweis{break-inside:avoid}
h1,h2,h3{break-after:avoid}
.sitehinweis{max-width:none!important;margin:20px 0 0!important;padding:0!important;font-size:11.5px}
.sitehinweis p{background:#fff6dd!important;color:#3d2e05!important;border-color:#e0a52b!important}
.sitehinweis b{color:#7a4f00!important}
}
/* Große Bildschirme: ganze Breite nutzen */
@media (min-width:1240px){.wrap,.sitenav .sn-in,.sitehinweis{max-width:none!important}.sitenav .sn-in,.sitehinweis{padding-left:max(32px, env(safe-area-inset-left, 0px));padding-right:max(32px, env(safe-area-inset-right, 0px))}}
/* Cockpit (Energie, E-Auto, Heizung): Eingaben links, Ergebnis rechts, beide Spalten bleiben stehen und scrollen einzeln */
@media (min-width:1200px) and (min-height:620px){
.sitenav.flush ~ .wrap{gap:14px}
.sitenav.flush ~ .wrap > header{display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 28px;align-items:end}
.sitenav.flush ~ .wrap > header .eyebrow{grid-column:1/-1}
.sitenav.flush ~ .wrap > header h1{font-size:26px;max-width:22em}
.sitenav.flush ~ .wrap > header .lead{font-size:13.5px;line-height:1.45;margin:0}
.sitenav.flush ~ .wrap .main{grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:16px}
.sitenav.flush ~ .wrap .main > .panel{position:sticky;top:10px;max-height:calc(100vh - 20px);overflow:auto;padding:14px;gap:12px;scrollbar-width:thin}
.sitenav.flush ~ .wrap .main .f label{font-size:12.5px}
.sitenav.flush ~ .wrap .main .f input,.sitenav.flush ~ .wrap .main .f select{font-size:14px;padding:4px 8px}
.sitenav.flush ~ .wrap .main .f small{font-size:11px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sitenav.flush ~ .wrap .main .row2{gap:8px}
.sitenav.flush ~ .wrap .main h2{font-size:18px}
.sitenav.flush ~ .wrap .main h3{font-size:15px}
.sitenav.flush ~ .wrap .main .verdict{font-size:15.5px;padding:10px 14px}
.sitenav.flush ~ .sitehinweis{margin-bottom:10px}
.sitenav.flush ~ .sitehinweis p{padding:6px 12px;font-size:12.5px}
}
@media (max-width:640px){.sitenav .sn-links{gap:2px 14px;font-size:14px}.sitenav .sn-logo span{display:none}}
</style>'''
def nav(cur, flush):
    links = [('../', 'Start'), ('../steuerrechner/', 'Steuerrechner'), ('../eauto-rechner/', 'E-Auto-Rechner'), ('../heizungsrechner/', 'Heizung und Dämmung'), ('../energie-rechner/', 'Energie-Rechner'), ('../balkon-rechner/', 'Balkon-Rechner'), ('../ueber-mich.html', 'Über mich')]
    a = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if t == cur else ""}>{t}</a>' for h, t in links)
    return (f'<nav class="sitenav{" flush" if flush else ""}" aria-label="Hauptmenü"><div class="sn-in"><a class="sn-logo" href="../" aria-label="Mut zur Zukunft, zur Startseite">{LOGO}<span>Mut zur <b>Zukunft</b></span></a>'
            f'<div class="sn-links"><a class="sn-buch" href="../buch/">Zum Buch</a>{a}<button type="button" class="sn-druck" onclick="print()" title="Eingaben und Ergebnisse drucken oder als PDF speichern">Drucken / PDF</button></div></div></nav>')
HINWEIS = ('<div class="sitehinweis" role="note"><p><b>Prototyp, noch nicht unabhängig geprüft.</b> Dieser Rechner ist ein vereinfachtes Modell zum Buch „Wir können uns die Zukunft leisten“. '
           'Die Ergebnisse sind Größenordnungen, können Fehler enthalten und ersetzen keine Steuer-, Rechts-, Finanz- oder Energieberatung. '
           'Alle Angaben ohne Gewähr. <a href="../impressum.html#haftung">Haftungsausschluss</a></p></div>')
DRUCK = ('''<script id="druck-js">(() => {
  let alt = null, zu = [];
  addEventListener("beforeprint", () => {
    const r = document.documentElement; alt = r.getAttribute("data-theme"); r.setAttribute("data-theme", "light");
    zu = [...document.querySelectorAll("details:not([open])")].filter(d => d.querySelector("input,select") && !d.closest("#quellen,#fragen")); zu.forEach(d => d.open = true);
    if (!document.querySelector(".druckkopf")) { const k = document.createElement("div"); k.className = "druckkopf";
      k.textContent = `${document.title} · Ausdruck vom ${new Date().toLocaleDateString("de-DE")} · ${location.href.split("#")[0]}`; document.body.prepend(k); }
  });
  // Steuerrechner: jeden Rechner-Teil einzeln drucken
  document.querySelectorAll("section.block[id]").forEach(sec => { const h = sec.querySelector("h2"); if (!h || !sec.querySelector(".calc, form")) return;
    const b = document.createElement("button"); b.type = "button"; b.className = "teil-druck"; b.textContent = "Diesen Teil drucken";
    b.onclick = () => { document.body.classList.add("druck-teil"); sec.classList.add("druck-dieser"); print(); }; h.after(b); });
  addEventListener("afterprint", () => { document.body.classList.remove("druck-teil"); document.querySelectorAll(".druck-dieser").forEach(e => e.classList.remove("druck-dieser")); const r = document.documentElement; alt === null ? r.removeAttribute("data-theme") : r.setAttribute("data-theme", alt); zu.forEach(d => d.open = false); });
})();</script>''')
def einsetzen(pfad, cur, flush):
    s = open(pfad, encoding='utf-8').read()
    s = re.sub(r'<style id="sitenav-css">.*?</style>\n?', '', s, flags=re.S)
    s = re.sub(r'<nav class="sitenav[^"]*".*?</div></div></nav>\n?', '', s, flags=re.S)
    s = re.sub(r'<div class="sitehinweis".*?</p></div>\n?', '', s, flags=re.S)
    s = re.sub(r'<script id="druck-js">.*?</script>\n?', '', s, flags=re.S)
    s = s.replace('</head>', CSS + '\n</head>', 1)
    s = s.replace('<body>\n', '<body>\n' + nav(cur, flush) + '\n', 1)
    assert s.count('<footer') == 1, pfad
    s = s.replace('<footer', HINWEIS + '\n<footer', 1)
    s = s.replace('<script src="../satz.js" defer></script>\n', '')
    s = s.replace('</body>', DRUCK + '\n<script src="../satz.js" defer></script>\n</body>', 1)
    open(pfad, 'w', encoding='utf-8').write(s)
if __name__ == '__main__':
    for d, cur, flush in SEITEN:
        einsetzen(os.path.join(ROOT, d, 'index.html'), cur, flush); print('Menü:', d)
