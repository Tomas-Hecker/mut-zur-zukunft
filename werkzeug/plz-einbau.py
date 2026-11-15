#!/usr/bin/env python3
"""Baut das Feld „Postleitzahl“ in Energie-, Balkon- und Heizungsrechner ein: Nach Eingabe lädt der Rechner
das Wetterjahr des Postleitzahlbereichs (wetter/<bereich>.json, siehe wetter-laden.py) und rechnet damit.
Ohne Postleitzahl bleibt alles wie bisher (Idstein). Einmal ausführen; ein zweiter Lauf bricht ab."""
import re, sys

def rep(s, a, b, n=1):
    c = s.count(a); assert c == n, (a[:80], c); return s.replace(a, b)

SKRIPT = '<script src="../wetter/ort.js"></script>\n'
ORT = '<span class="ortname">Idstein</span>'

# ---------- Energie-Rechner ----------
p = 'energie-rechner/index.html'; s = open(p, encoding='utf-8').read()
assert 'wetter/ort.js' not in s, 'schon eingebaut'
s = rep(s, '<title>Energie-Rechner Idstein</title>', '<title>Energie-Rechner</title>')
s = rep(s, 'content="Stündliche Simulation für Idstein:', 'content="Stündliche Simulation mit dem Wetter deines Orts (Postleitzahl):')
s = rep(s, '<div class="eyebrow">Stündliche Simulation · Idstein im Taunus</div>', f'<div class="eyebrow">Stündliche Simulation · Wetter für {ORT}</div>')
s = rep(s, 'Temperatur und Luftfeuchte in Idstein,', f'Temperatur und Luftfeuchte in {ORT},')
s = rep(s, '<div class="panel" id="eing">\n      <div class="grp"><h3>Haushalt</h3>',
        '<div class="panel" id="eing">\n      <div class="grp"><h3>Dein Ort</h3><div class="row2" id="g_ort"></div></div>\n      <div class="grp"><h3>Haushalt</h3>')
s = rep(s, 'mit dem Wetterjahr für Idstein.', f'mit dem Wetterjahr für {ORT}.')
s = rep(s, '<h2>Wetterjahr Idstein</h2>', f'<h2>Wetterjahr {ORT}</h2>')
s = rep(s, '<li><b>Wetter:</b> Idstein (50,22° N, 8,27° O, 273 m).', '<li id="wetterquelle"><b>Wetter:</b> Ohne Postleitzahl: Idstein (50,22° N, 8,27° O, 273 m).')
s = rep(s, 'const N = 8760, LAT = 50.219, LON = 8.268;', 'const N = 8760; let LAT = 50.219, LON = 8.268;   // mit Postleitzahl vom Wetter des Orts')
s = rep(s, '\n/* Ablauf */', '''
/* Wetter nach Postleitzahl */
async function ortLaden(p) {
  const w = await Ort.wetter(p); if (!w) return null;
  LAT = w.lat; LON = w.lon;
  setWetter(w.t, w.rh, w.g, w.d, Ort.quelle(w)); for (const k in PVC) delete PVC[k];
  document.querySelectorAll(".ortname").forEach(e => e.textContent = "Raum " + w.n);
  $("wetterquelle").innerHTML = "<b>Wetter:</b> " + Ort.quelle(w);
  $("wstatus").textContent = ""; run(); return w;
}
Ort.feld($("g_ort"), ortLaden, "Gib deine Postleitzahl ein, dann rechnet der Rechner mit dem Wetter deines Orts. Ohne: Idstein.");

/* Ablauf */''')
i = s.index('\n<script>\n') + 1; s = s[:i] + SKRIPT + s[i:]   # ort.js vor dem Rechenskript laden
open(p, 'w', encoding='utf-8').write(s)

# ---------- Balkon-Rechner ----------
p = 'balkon-rechner/index.html'; s = open(p, encoding='utf-8').read()
assert 'wetter/ort.js' not in s, 'schon eingebaut'
s = rep(s, 'Stunde für Stunde für Idstein simuliert,', 'Stunde für Stunde mit dem Wetter deines Orts simuliert,')
s = rep(s, '<div class="eyebrow">Für Mieter · Stündliche Simulation · Idstein im Taunus</div>', f'<div class="eyebrow">Für Mieter · Stündliche Simulation · Wetter für {ORT}</div>')
s = rep(s, '<div class="panel" id="eing">\n      <div class="grp"><h3>Haushalt</h3>',
        '<div class="panel" id="eing">\n      <div class="grp"><h3>Dein Ort</h3><div class="row2" id="g_ort"></div></div>\n      <div class="grp"><h3>Haushalt</h3>')
s = rep(s, 'mit dem Wetterjahr für Idstein.', f'mit dem Wetterjahr für {ORT}.')
s = rep(s, 'F("foerd", "Zuschuss der Stadt", "€", 10, "Idstein hat Balkonkraftwerke mit 30 %, höchstens 150 € gefördert, auch für Mieter mit Zustimmung des Eigentümers. Frag nach, ob das Programm noch läuft.")',
        'F("foerd", "Zuschuss der Stadt", "€", 10, "Manche Städte fördern Balkonkraftwerke, Idstein zum Beispiel mit 30 %, höchstens 150 €, auch für Mieter mit Zustimmung des Eigentümers. Frag bei deiner Stadt nach.")')
s = rep(s, 'const N = 8760, LAT = 50.219, LON = 8.268;', 'const N = 8760; let LAT = 50.219, LON = 8.268;   // mit Postleitzahl vom Wetter des Orts')
s = rep(s, '"<b>Wetter:</b> Idstein (50,22° N, 8,27° O). Typisches', '"<b>Wetter:</b> <span id=\\"wetterquelle\\">Ohne Postleitzahl: Idstein (50,22° N, 8,27° O).</span> Typisches')
s = rep(s, 'function planeRun() { clearTimeout(tmr); tmr = setTimeout(run, 80); }\nrun();', '''function planeRun() { clearTimeout(tmr); tmr = setTimeout(run, 80); }
/* Wetter nach Postleitzahl */
async function ortLaden(p) {
  const w = await Ort.wetter(p); if (!w) return null;
  LAT = w.lat; LON = w.lon; SONNE = null; for (const k in PVC) delete PVC[k];
  W.t = Float64Array.from(w.t); W.g = Float64Array.from(w.g); W.d = Float64Array.from(w.d);
  document.querySelectorAll(".ortname").forEach(e => e.textContent = "Raum " + w.n);
  const q = $("wetterquelle"); if (q) q.textContent = `Postleitzahlbereich ${w.bereich}.. (${w.n}, ${fmt(w.lat, 2)}° N, ${fmt(w.lon, 2)}° O, ${w.z} m), Lage aus Ortskoordinaten von GeoNames (CC BY 4.0).`;
  run(); return w;
}
Ort.feld($("g_ort"), ortLaden, "Gib deine Postleitzahl ein, dann rechnet der Rechner mit dem Wetter deines Orts. Ohne: Idstein.");
run();''')
i = s.index('\n<script>\n') + 1; s = s[:i] + SKRIPT + s[i:]   # ort.js vor dem Rechenskript laden
open(p, 'w', encoding='utf-8').write(s)
print('energie, balkon ok')

# ---------- Heizungsrechner ----------
p = 'heizungsrechner/index.html'; s = open(p, encoding='utf-8').read()
assert 'wetter/ort.js' not in s, 'schon eingebaut'
s = rep(s, '      <div class="grp"><h3>Dein Haus</h3><div class="row2" id="haus"></div></div>',
        '      <div class="grp"><h3>Dein Ort</h3><div class="row2" id="g_ort"></div></div>\n      <div class="grp"><h3>Dein Haus</h3><div class="row2" id="haus"></div></div>')
s = rep(s, "  const q = new URLSearchParams({ waerme: Math.round(d.w1), vl: Math.round(d.vl1) });",
        "  const q = new URLSearchParams({ waerme: Math.round(d.w1), vl: Math.round(d.vl1) }); if (PLZ) q.set(\"plz\", PLZ);")
s = rep(s, '\nrun();\n</script>', r"""
/* Ort nach Postleitzahl: mittlere Temperatur der Heizzeit und Vorschlag für die Jahresarbeitszahl nach dem Wetter des Orts */
let PLZ = "";
const BH0 = { ...BH }, JAZ0 = V.wpJaz;
let jazEigen = new URLSearchParams(location.search).has("wpJaz");   // vom Energie-Rechner übernommen oder selbst eingetragen: bleibt
document.addEventListener("input", e => { if (e.target && e.target.id === "i_wpJaz") jazEigen = true; });
async function ortLaden(p) {
  const i = await Ort.info(p); if (!i) return null;
  const b = await Ort.bezug(); PLZ = p;
  BH.teMittel = BH0.teMittel + (i.th - b.th);
  if (!jazEigen) { V.wpJaz = Math.round(JAZ0 * i.jf * 10) / 10; const el = $("i_wpJaz"); if (el) el.value = V.wpJaz; }
  $("ort_note").textContent = `Jahresarbeitszahl ${fmt(V.wpJaz, 1)}${jazEigen ? " (deine Angabe)" : ` (für ${i.n} geschätzt: ${fmt(JAZ0, 1)} × ${fmt(i.jf, 2)}, gerechnet wie im Energie-Rechner mit dem Wetter des Orts)`}. `
    + `Mittel der Außentemperatur in der Heizzeit ${fmt(i.th, 1)} °C (Idstein ${fmt(b.th, 1)} °C). Wetter: PVGIS 5.3, © Europäische Union, CC BY 4.0.`;
  run(); return i;
}
Ort.feld($("g_ort"), ortLaden, "Gib deine Postleitzahl ein, dann schätzt der Rechner die Jahresarbeitszahl für deinen Ort. Ohne: Idstein.");
$("g_ort").insertAdjacentHTML("beforeend", '<small class="note" id="ort_note"></small>');
run();
</script>""")
i = s.index('\n<script>\n') + 1; s = s[:i] + SKRIPT + s[i:]
open(p, 'w', encoding='utf-8').write(s)

# ---------- Energie-Rechner: Postleitzahl an den Heizungsrechner weitergeben ----------
p = 'energie-rechner/index.html'; s = open(p, encoding='utf-8').read()
s = rep(s, '  $("hlink").innerHTML = `Mit Kauf, Förderung, CO₂-Preis und Öl:', '  { const pz = new URLSearchParams(location.search).get("plz"); if (pz) q.set("plz", pz); }\n  $("hlink").innerHTML = `Mit Kauf, Förderung, CO₂-Preis und Öl:')
open(p, 'w', encoding='utf-8').write(s)
print('heizung ok')
