#!/usr/bin/env python3
"""Korrekturen aus der Rechnerprüfung vom 15.11.2026 (von Tomas freigegeben). Einmal ausführen."""
def rep(p, a, b, n=1):
    s = open(p, encoding='utf-8').read(); c = s.count(a); assert c == n, (p, a[:70], c)
    open(p, 'w', encoding='utf-8').write(s.replace(a, b))

H = 'heizungsrechner/index.html'
assert 'StromCO2P' not in open(H, encoding='utf-8').read(), 'schon gelaufen'
# Biogas-Stufen: stimmen mit § 43 GModG überein (10 % 2029, 15 % 2030, 30 % 2035, 60 % 2040); nur amtliche Quelle ergänzt
rep(H, '30 % ab 2035, 60 % ab 2040. <a href="https://reduco.ai/blog/heizungsgesetz-2026-aenderungen" target="_blank" rel="noopener">Überblick</a>',
       '30 % ab 2035, 60 % ab 2040 (§ 43 GModG). <a href="https://www.gmodg.bund.de/GModG/DE/Home/startseite/GModG_News/GModG_News-node.html" target="_blank" rel="noopener">Bundesregierung</a>, <a href="https://reduco.ai/blog/heizungsgesetz-2026-aenderungen" target="_blank" rel="noopener">Überblick</a>')
# CO₂-Faktor Erdgas auf den Brennwert bezogen, so wie Gas abgerechnet wird
rep(H, 'const EF = { gas: 0.201, oel: 0.266 };           // kg CO₂ je kWh',
       'const EF = { gas: 0.181, oel: 0.266 };           // kg CO₂ je kWh; Gas je kWh Brennwert (0,201 je kWh Heizwert ÷ 1,11), wie abgerechnet')
rep(H, '<li><b>CO₂-Preis:</b>', '<li><b>CO₂ je kWh:</b> Erdgas 0,181 kg je kWh Brennwert (so wird Gas abgerechnet; 0,201 kg je kWh Heizwert), Heizöl 0,266 kg je kWh (Umweltbundesamt).</li>\n        <li><b>CO₂-Preis:</b>')
# Reform: Strom 5 % Mehrwertsteuer und Stromsteuer auf das europäische Mindestmaß (0,1 statt 2,05 Cent netto), wie im Buch
rep(H, 'const RF = { strom: 1.05 / 1.19,', 'const RF = { stromSt: 0.0205 - 0.001, strom: 1.05 / 1.19,')
rep(H, 'wpStrom: v.wpStrom * RF.strom,', 'wpStrom: (v.wpStrom / 1.19 - RF.stromSt) * 1.05,')
rep(H, '// Vorschlag aus dem Buch: Strom 5 %,', '// Vorschlag aus dem Buch: Strom 5 % und Stromsteuer auf dem europäischen Mindestmaß,')
# CO₂ des Stroms: sinkender Pfad statt 20 Jahre Strommix 2024
rep(H, '  WpKw: 1500, StromCO2: 0.363, Lebensdauer: 40 };',
       '''  WpKw: 1500, StromCO2: 0.363, Lebensdauer: 40 };
// CO₂ je kWh Strom: 2024 laut Umweltbundesamt, danach sinkend mit dem Ausbau von Wind und Sonne (eigene Annahme nach den Ausbauzielen)
const StromCO2P = [[2024, 0.363], [2030, 0.25], [2040, 0.10], [2045, 0.05]];
const stromCO2 = j => { const p = StromCO2P; if (j <= p[0][0]) return p[0][1]; for (let i = 1; i < p.length; i++) if (j <= p[i][0]) { const [a, pa] = p[i - 1], [b, pb] = p[i]; return pa + (pb - pa) * (j - a) / (b - a); } return p.at(-1)[1]; };
const stromCO2Mittel = v => { let s = 0; for (let n = 0; n < v.dauer; n++) s += stromCO2(v.jahr + n); return s / Math.max(1, v.dauer); };''')
rep(H, 'const co2 = { wp0: s0 * D.StromCO2 / 1000, wp1: s1 * D.StromCO2 / 1000,',
       'const sc = stromCO2Mittel(V), co2 = { wp0: s0 * sc / 1000, wp1: s1 * sc / 1000,')
rep(H, 'row("CO₂ im ersten Jahr",', 'row("CO₂ im Jahr (Strom im Mittel der Laufzeit)",')
rep(H, 'CO₂ des Stroms: Strommix 2024 mit 363 g je kWh (Umweltbundesamt, Schätzung vom 9.4.2025); er sinkt mit jedem Jahr mehr Wind und Sonne.',
       'CO₂ des Stroms: Strommix 2024 mit 363 g je kWh (Umweltbundesamt, Schätzung vom 9.4.2025), danach sinkend auf 250 g 2030 und 100 g 2040 (eigene Annahme nach den Ausbauzielen für Wind und Sonne); gerechnet ist das Mittel über ${fmt(V.dauer)} Jahre, ${fmt(sc * 1000)} g je kWh.')
# Heizgradstunden nach Ort: wärmere Orte brauchen bei gleicher Hülle weniger Wärme
rep(H, '  BH.teMittel = BH0.teMittel + (i.th - b.th);', '  BH.teMittel = BH0.teMittel + (i.th - b.th); D.HGT = HGT0 * (20 - i.th) / (20 - b.th);')
rep(H, 'const BH0 = { ...BH }, JAZ0 = V.wpJaz;', 'const BH0 = { ...BH }, JAZ0 = V.wpJaz, HGT0 = D.HGT;')

E = 'eauto-rechner/index.html'
# CO₂-Preis im Sprit steigt mit dem Emissionshandel; THG-Prämie für das E-Auto
rep(E, 'agLaden: "nein", erstatt: 0, dJahre: 4,', 'agLaden: "nein", erstatt: 0, dJahre: 4, iKraft: "benzin", thg: 300, thgBis: 2030,')
rep(E, 'F("iSprit", "Spritpreis", "€/l", 0.01),', 'F("iKraft", "Kraftstoff", "", 0, "", [["benzin", "Benzin"], ["diesel", "Diesel"]]), F("iSprit", "Spritpreis heute", "€/l", 0.01, "der CO₂-Preis darin steigt mit dem Emissionshandel"),')
rep(E, 'F("eWallbox", "Wallbox (einmalig)", "€", 100, "0, wenn schon vorhanden")]',
       'F("eWallbox", "Wallbox (einmalig)", "€", 100, "0, wenn schon vorhanden"), F("thg", "THG-Prämie", "€/Jahr", 10, "2026 meist 300 bis 380 €; wie lange sie so hoch bleibt, ist offen"), F("thgBis", "THG-Prämie bis einschließlich", "", 1, "Jahr; danach ohne Prämie gerechnet")]')
rep(E, '// Rechenkern (privat: Gesamtkosten des Halters)\nfunction rechne(v) {',
       '''// CO₂-Preis je Tonne: 2026 und 2027 nach BEHG, danach EU-Emissionshandel (gleiche Annahme wie im Heizungsrechner)
const CO2P = [[2026, 60], [2027, 65], [2028, 60], [2030, 70], [2035, 100], [2040, 150]];
const co2Preis = j => { const p = CO2P; if (j <= p[0][0]) return p[0][1]; for (let i = 1; i < p.length; i++) if (j <= p[i][0]) { const [a, pa] = p[i - 1], [b, pb] = p[i]; return pa + (pb - pa) * (j - a) / (b - a); } return p.at(-1)[1]; };
const KG_L = { benzin: 2.37, diesel: 2.65 };   // kg CO₂ je Liter
// Rechenkern (privat: Gesamtkosten des Halters)
function rechne(v) {''')
rep(E, '''    i += v.iSteuer + v.iVers + v.iWart + v.km * iEnergie;
    e += eSt + v.eVers + v.eWart + v.km * eEnergie;
    jahre.push({ j: n, i, e, eSt });''',
'''    const spritCO2 = v.iVerb / 100 * KG_L[v.iKraft || "benzin"] / 1000 * (co2Preis(kj) - co2Preis(v.kaufjahr)) * 1.19;   // €/km mehr als heute
    const thg = kj <= v.thgBis ? v.thg : 0;
    i += v.iSteuer + v.iVers + v.iWart + v.km * (iEnergie + spritCO2);
    e += eSt + v.eVers + v.eWart + v.km * eEnergie - thg;
    jahre.push({ j: n, i, e, eSt, sC: v.km * spritCO2, thg });''')
rep(E, '''  const eStSum = jahre.slice(1).reduce((a, r) => a + r.eSt, 0);''',
'''  const eStSum = jahre.slice(1).reduce((a, r) => a + r.eSt, 0), sCSum = jahre.slice(1).reduce((a, r) => a + r.sC, 0), thgSum = jahre.slice(1).reduce((a, r) => a + r.thg, 0);''')
rep(E, '''    "Kfz-Steuer": [v.jahre * v.iSteuer, eStSum],
  };''', '''    "Kfz-Steuer": [v.jahre * v.iSteuer, eStSum],
    "Steigender CO₂-Preis im Sprit": [sCSum, 0],
    "THG-Prämie": [0, -thgSum],
  };''')
rep(E, '<li>Verbrauch nach Herstellerangabe (WLTP)', '''<li><b>CO₂-Preis im Sprit:</b> Der Spritpreis von heute enthält den CO₂-Preis von heute. Danach rechnet der Rechner mit dem EU-Emissionshandel für Verkehr und Gebäude: rund 60 € je Tonne 2028, 70 € 2030, 100 € 2035, 150 € 2040 (eigene Annahme, Bandbreite groß). Ein Liter Benzin setzt 2,37 kg CO₂ frei, Diesel 2,65 kg. Sonst bleiben alle Preise wie heute.</li>
        <li><b>THG-Prämie:</b> Halter von Elektroautos können ihre CO₂-Einsparung jedes Jahr über einen Anbieter verkaufen. 2026 zahlen viele Anbieter 300 bis 380 €; die Quote steigt 2027 von 12 auf 17,5 %. <a href="https://www.auto-motor-und-sport.de/verkehr/thg-praemie-2027-wann-beantragen-wie-viel-euro-gibt-es/" target="_blank" rel="noopener">auto motor und sport</a></li>
        <li>Verbrauch nach Herstellerangabe (WLTP)''')

N = 'energie-rechner/index.html'
rep(N, 'F("netz", "Netzentgelt", "€/kWh", 0.001, "netto; Syna 2026: 8,67 Cent")', 'F("netz", "Netzentgelt", "€/kWh", 0.001, "netto, steht auf dem Preisblatt deines Netzbetreibers; Vorgabe: Syna 2026 (Idstein), 8,67 Cent")')
rep(N, 'Der Haushaltsstrom zahlt das normale Netzentgelt.</li>', 'Der Haushaltsstrom zahlt das normale Netzentgelt. Trägst du dein eigenes Netzentgelt ein, rechnet der Rechner die Stufen im selben Verhältnis um; Zeitfenster und Stufen anderer Netzbetreiber weichen ab, sie stehen auf deren Preisblatt.</li>')
rep(N, '<li>Keine Energieberatung. Für die genaue Auslegung', '<li><b>Speicher:</b> Der Speicher lädt hier nur aus der eigenen PV, nie billig aus dem Netz. Mit dynamischem Tarif kann ein Speicher, der auch in billigen Netzstunden lädt, etwas mehr sparen; der Rechner unterschätzt seinen Nutzen dort eher.</li>\n        <li>Keine Energieberatung. Für die genaue Auslegung')
rep(N, 'const m = [31, 29, 31, 30,', 'const m = [31, 28, 31, 30,')

B = 'balkon-rechner/index.html'
rep(B, 'const MT = [31, 29, 31, 30,', 'const MT = [31, 28, 31, 30,')
rep(B, 'pvKost: 400, montage: 0, pvJahre: 30,', 'pvKost: 400, montage: 0, pvJahre: 25,')
rep(B, '"rund 30 Jahre; beim Umzug kommt die Anlage mit"', '"25 Jahre vorsichtig gerechnet, oft halten die Module länger; beim Umzug kommt die Anlage mit"')
print('ok')
