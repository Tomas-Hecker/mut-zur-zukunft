"""Setzt auf allen Rechner-Seiten oben dieselbe Menüleiste wie auf der Startseite ein (idempotent).
Aufruf: python3 werkzeug/rechner-menue.py  (aus dem Hauptordner der Homepage)"""
import re, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SEITEN = [('steuerrechner', 'Steuerrechner', False), ('eauto-rechner', 'E-Auto-Rechner', True), ('heizungsrechner', 'Heizungsrechner', True), ('energie-rechner', 'Energie-Rechner', True)]
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
.sitehinweis{max-width:1180px;margin:0 auto 20px;padding:0 max(16px, env(safe-area-inset-left, 0px));font:14px/1.45 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
.sitenav.flush + .sitehinweis{margin-top:-8px;padding:0}
.sitehinweis p{margin:0;padding:10px 14px;border:1px solid #e0a52b;border-left-width:5px;border-radius:8px;background:#fff6dd;color:#3d2e05}
.sitehinweis b{color:#7a4f00}
.sitehinweis a{color:inherit;text-decoration:underline}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .sitehinweis p{background:#2e2410;color:#f3e6c4;border-color:#a8790f}:root:not([data-theme="light"]) .sitehinweis b{color:#f2b33d}}
:root[data-theme="dark"] .sitehinweis p{background:#2e2410;color:#f3e6c4;border-color:#a8790f}
:root[data-theme="dark"] .sitehinweis b{color:#f2b33d}
.sitenav:not(.flush) + .sitehinweis{margin-top:14px}
@media (max-width:640px){.sitenav .sn-links{gap:2px 14px;font-size:14px}.sitenav .sn-logo span{display:none}}
</style>'''
def nav(cur, flush):
    links = [('../', 'Start'), ('../steuerrechner/', 'Steuerrechner'), ('../eauto-rechner/', 'E-Auto-Rechner'), ('../heizungsrechner/', 'Heizungsrechner'), ('../energie-rechner/', 'Energie-Rechner'), ('../ueber-mich.html', 'Über mich')]
    a = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if t == cur else ""}>{t}</a>' for h, t in links)
    return (f'<nav class="sitenav{" flush" if flush else ""}" aria-label="Hauptmenü"><div class="sn-in"><a class="sn-logo" href="../" aria-label="Mut zur Zukunft, zur Startseite">{LOGO}<span>Mut zur <b>Zukunft</b></span></a>'
            f'<div class="sn-links"><a class="sn-buch" href="../buch/">Zum Buch</a>{a}</div></div></nav>')
HINWEIS = ('<div class="sitehinweis" role="note"><p><b>Prototyp, noch nicht unabhängig geprüft.</b> Dieser Rechner ist ein vereinfachtes Modell zum Buch „Mut zur Zukunft“. '
           'Die Ergebnisse sind Größenordnungen, können Fehler enthalten und ersetzen keine Steuer-, Rechts-, Finanz- oder Energieberatung. '
           'Alle Angaben ohne Gewähr. <a href="../impressum.html#haftung">Haftungsausschluss</a></p></div>')
def einsetzen(pfad, cur, flush):
    s = open(pfad, encoding='utf-8').read()
    s = re.sub(r'<style id="sitenav-css">.*?</style>\n?', '', s, flags=re.S)
    s = re.sub(r'<nav class="sitenav[^"]*".*?</div></div></nav>\n?', '', s, flags=re.S)
    s = re.sub(r'<div class="sitehinweis".*?</p></div>\n?', '', s, flags=re.S)
    s = s.replace('</head>', CSS + '\n</head>', 1)
    s = s.replace('<body>\n', '<body>\n' + nav(cur, flush) + '\n' + HINWEIS + '\n', 1)
    open(pfad, 'w', encoding='utf-8').write(s)
if __name__ == '__main__':
    for d, cur, flush in SEITEN:
        einsetzen(os.path.join(ROOT, d, 'index.html'), cur, flush); print('Menü:', d)
