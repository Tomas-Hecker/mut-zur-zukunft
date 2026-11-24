#!/usr/bin/env python3
"""Verkehrspaket (Freigabe Tomas 24.11.2026) im Steuerrechner, Haushaltsteil:
zweite Stufe 66 % statt zwei Drittel, Aufschlag 4 ct je kWh auf die Kilometerabgabe ab 2030,
Arbeitsweg nie teurer als heute (Gutschrift bis 7,44 ct je kWh). Läuft nach prozente-ganz.py; zweiter Lauf ändert nichts."""
import sys
P = 'steuerrechner/index.html'
s = open(P, encoding='utf-8').read()
if 'VK_PFAD' in s:
    print('schon drin'); sys.exit()
import json
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a)); s = s.replace(a, b)
# 1. Stufe über 5.000 €: 65 % (Aufschlag 0,65/0,35)
rep('Object.assign(ANNAHMEN, {"Satz4": 2.0, ', 'Object.assign(ANNAHMEN, {"Satz4": 2.0, ')
i = s.index('Object.assign(ANNAHMEN, {"Satz4": 2.0, '); j = s.index('\n', i)
s = s[:j + 1] + ('// Verkehrspaket 24.11.2026: die Stufe über 5.000 € im Monat sinkt von zwei Dritteln auf 66 % (Aufschlag 0,66/0,34 auf den Einkauf; gewählt 10:16 UTC, weil Lkw über 3,5 t den Aufschlag nicht zahlen)\n'
                 'Object.assign(ANNAHMEN, { Satz4: 0.66 / 0.34 });\n') + s[j + 1:]
rep('Nur für den Teil der Ausgaben über 5.000 € im Monat je Erwachsenem gehen von 100 € zwei Drittel an die Steuer.',
    'Nur für den Teil der Ausgaben über 5.000 € im Monat je Erwachsenem gehen von 100 € 66 € an die Steuer.')
rep('sind das 50 %, auf den Teil über 5.000 € im Monat zwei Drittel, nie mehr.', 'sind das 50 %, auf den Teil über 5.000 € im Monat 66 %, nie mehr.')
rep('${A.Satz4 === 2 ? "zwei Drittel" : pct(A.Satz4 / (1 + A.Satz4), 0)} statt 60 %', '${A.Satz4 === 2 ? "zwei Drittel" : pct(A.Satz4 / (1 + A.Satz4), 0)} statt 60 %')
# 2. Eingabe: davon zur Arbeit
rep('<div class="field"><label for="e_km">Kilometer im Jahr</label><input id="e_km" type="number" min="0" step="500" value="13500"></div>',
    '<div class="field"><label for="e_km">Kilometer im Jahr</label><input id="e_km" type="number" min="0" step="500" value="13500"></div>\n'
    '            <div class="field"><label for="e_arb">davon zur Arbeit, km im Jahr</label><input id="e_arb" type="number" min="0" step="500" value="0">'
    '<span class="hint">hin und zurück; auf dem Arbeitsweg wird das Fahren nie teurer als heute</span></div>')
rep('km: n("e_km"), ', 'km: n("e_km"), arb: Math.min(n("e_arb"), n("e_km")), ')
# 3. Kilometerabgabe mit Aufschlag und Gutschrift für den Arbeitsweg
alt_a = s.index('function kmAbgabe(km) {'); alt_b = s.index('\nfunction energieRechne(e) {')
s = s[:alt_a] + '''// Verkehrspaket 24.11.2026: ab 2030 Aufschlag KM_AUF ct je kWh für alle Autos; auf dem Arbeitsweg kostet die Abgabe je kWh höchstens KM_DECKEL ct
// (heute die Steuer auf Benzin, 65,45 ct je Liter / 8,8 kWh), Gutschrift auf der Jahresrechnung nach der Meldung des Arbeitgebers
const KM_AUF = 4, KM_DECKEL = 7.44;
function kmAbgabe(km, arb = 0) {   // Mittel 2027 bis 2046 wie die übrigen Werte: { ev, v: was die Abgabe kostet; gutEv, gutV: Gutschrift für den Arbeitsweg }
  let ev = 0, v = 0, gutEv = 0, gutV = 0;
  const kwhV = KM_V_L * KM_KWH_L, estV = KM_V_L * KM_EST, a = KM_AUF / 100, d = KM_DECKEL / 100;
  for (let j = 2027; j <= 2046; j++) { const s = (KM_SATZ[j] || 0) / 100; if (!s) continue;
    const eKm = (s + a) * KM_EV_KWH, vKm = Math.max(0, s * kwhV - estV) * Math.min(1, 0.25 + 0.1 * (j - 2030)) + a * kwhV;
    ev += eKm * km; v += vKm * km;
    gutEv += Math.max(0, eKm - Math.min(s + a, d) * KM_EV_KWH) * arb;
    gutV += Math.max(0, vKm - Math.max(0, d * kwhV - estV)) * arb; }
  return { ev: ev / 20, v: v / 20, gutEv: gutEv / 20, gutV: gutV / 20 };
}''' + s[alt_b:]
rep('const ka = kmAbgabe(e.km);', 'const ka = kmAbgabe(e.km, e.arb || 0);')
rep('if (r === "reform" && e.ev) t.push(["Kilometerabgabe für das E-Auto (ab 2030)", -ka.ev]);\n'
    '    else if (r === "reform" && e.auto) t.push(["Kilometerabgabe für den Verbrenner, Mehrbetrag über seiner Energiesteuer (ab 2030, Übergang bis 2038)", -ka.v]);',
    'if (r === "reform" && e.ev) t.push(["Kilometerabgabe für das E-Auto (ab 2030, mit dem Aufschlag von 4 ct je kWh)", -ka.ev]);\n'
    '    else if (r === "reform" && e.auto) t.push(["Kilometerabgabe für den Verbrenner, Mehrbetrag über seiner Energiesteuer und Aufschlag von 4 ct je kWh (ab 2030, Übergang bis 2038)", -ka.v]);\n'
    '    if (r === "reform" && e.auto && (e.ev ? ka.gutEv : ka.gutV) > 0) t.push(["Gutschrift für den Arbeitsweg: dort nie teurer als heute", e.ev ? ka.gutEv : ka.gutV]);')
# 4. Staatshaushalt wie die Kette (pfad_lauf.py: kern19 + Ertragspfad): Stufe und Ausweichen wie bei zwei Dritteln, Paket als Pfad
pf = json.load(open('/mnt/project-files/rechenmodell-mikrosim/verkehr-2026-11-24/kette-ertragspfad-paket-ohne-lkw-stufe66.json'))
pf = {k: round(v, 3) for k, v in pf.items() if int(k) <= 2071}
rep('function s4Zwei(k) { return A.S4Mikro > 0 && k <= A.Stufe4Jahre ? mikro("p9", k) * (A.Satz4 - 1.5) / 0.5 : 0; }',
    '''// Verkehrspaket 24.11.2026: der Staatshaushalt rechnet wie die Kette (kern19 + Ertragspfad): Stufe und Ausweichen wie bei zwei Dritteln,
// die 66 % (netto mit weniger Ausweichen rund 3,5 Mrd. €) stecken zusammen mit Aufschlag (ohne Lkw über 3,5 t) und Gutschrift für den Arbeitsweg im Pfad VK_PFAD (Mrd. €, + = mehr Ertrag)
function s4Zwei(k) { return A.S4Mikro > 0 && k <= A.Stufe4Jahre ? mikro("p9", k) * ((A.Satz4Saldo ?? A.Satz4) - 1.5) / 0.5 : 0; }
const VK_PFAD = ''' + json.dumps(pf, separators=(',', ':')) + ''';
function verkehrJ(k) { if (!A.VkPaket) return 0; const j = A.Prognose.ReformStart - 1 + k; return VK_PFAD[j] ?? VK_PFAD[Math.min(2071, Math.max(2028, j))]; }''')
rep('Object.assign(ANNAHMEN, { Satz4: 0.66 / 0.34 });', 'Object.assign(ANNAHMEN, { Satz4: 0.66 / 0.34, Satz4Saldo: 2.0, VkPaket: 1 });')
rep('+ coachStufenJ(y) + kleinJ(y);', '+ coachStufenJ(y) + kleinJ(y) + verkehrJ(y);   // Verkehrspaket 24.11.2026')
open(P, 'w', encoding='utf-8').write(s)
print('ok')
