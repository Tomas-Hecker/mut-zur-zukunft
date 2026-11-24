#!/usr/bin/env python3
"""Vorschlag für werkzeug/saeulenbild.py: baut das Säulenbild „Brutto, Abzüge und was im Portemonnaie bleibt“ in den Steuerrechner ein.
Ersetzt in updateHH() den Abschnitt „// Balken“ (alte oder neue Fassung aus balken-brutto.py) durch sbZeichnen() und sbAenderung(),
hängt saeulenbild.css an den ersten <style>-Block und saeulenbild.js vor function updateHH(). Ein zweiter Lauf ändert nichts.
Aufruf: python3 werkzeug/saeulenbild.py [steuerrechner/index.html] (Quellen in werkzeug/saeulenbild/, vom Prüf-Thread)"""
import re, sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "steuerrechner/index.html"
q = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saeulenbild")
s = open(p, encoding='utf-8').read()
if 'function sbZeichnen' in s:
    raise SystemExit
css = open(os.path.join(q, 'saeulenbild.css'), encoding='utf-8').read()
js = open(os.path.join(q, 'saeulenbild.js'), encoding='utf-8').read().replace('if (typeof module !== "undefined") module.exports = { sbDaten, sbSum };\n', '')
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b)
# 1) Abschnitt „// Balken“ bis zur geleerten Legende
m = re.findall(r'  // Balken\n.*?\n  \$\("legend"\)\.innerHTML = "";\n', s, flags=re.S)
assert len(m) == 1, len(m)
s = s.replace(m[0], '''  // Säulenbild: Brutto, Abzüge und was im Portemonnaie bleibt (saeulenbild.js)
  const sbd = sbDaten(h, r, { kst: A.KStS }), sbA = () => sbAenderung($("sbAend"), sbd);
  // Schieber „Investitionsquote“ (nur bei GmbH): setzt die Ausschüttung auf Gewinn × (1 − Körperschaftsteuer − Quote) und rechnet neu
  const sbInv = { setze: q => { zeigeGeld("aus", Math.max(0, h.gmbh * (1 - A.KStS - q))); if (aktiv !== -1) { aktiv = -1; renderPresets(); } updateHH(); postHeight(); } };
  sbZeichnen($("bars"), sbd, { praemieMonat: A.KVPraem / 12, namen: ["Heute", "Reform"], nachWechsel: sbA, invest: sbInv }); sbA();
  $("legend").innerHTML = "";
''')
# 2) Platz für „Was sich ändert“ unter dem Bild; die alte Rasterklasse des Balkens entfällt
rep('<div class="bars" id="bars"></div>', '<div id="bars"></div>\n        <div id="sbAend"></div>')
# 3) Stil und Skript
# mittlere Spalte darf nicht breiter werden als ihr Feld (1.150 bis 1.290 px): Rasterspur begrenzen, die zwei großen Zahlen umbrechen lassen
css += """
.panel.mitte { grid-template-columns: minmax(0, 1fr); }
.duo { grid-template-columns: repeat(auto-fit, minmax(min(100%, 140px), 1fr)); }
.duo > div { min-width: 0; }
.duo .v { overflow-wrap: anywhere; }
"""
i = s.index('</style>'); s = s[:i] + css + s[i:]
rep('\nfunction updateHH() {', '\n' + js + '\nfunction updateHH() {')
open(p, 'w', encoding='utf-8').write(s)
print('Säulenbild eingebaut')
