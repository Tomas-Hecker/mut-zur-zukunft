#!/usr/bin/env python3
"""Staatsseite und Haushalte des Steuerrechners auf Rechenkern Version 41 (wie version-41/modell-v41/modell_2_5_gesamtpaket_kern.py).
Quelle: broschuere-mut-zur-zukunft/version-41/staat-rechner-umbau-v41.md (18.11.2026). Werte in kern-v41-werte.json:
A (neue und geänderte Annahmen), MIKRO (Reihen p9, sf, sfp der Mikrosimulation), STRF (Zeile Energie und Straßenfonds 2028 bis 2072).
Neu: Stufe 4 mit zwei Dritteln (Satz4 = 2), Ausweichen an der obersten Stufe, Ergänzungssteuer der Konzerne, Chancen für alle,
Bildung zählt wie Sparen, Schonfrist für heutige Rentner und Beamte, Energie und Straßenfonds, Anteil am Hauswert als Barwert.
Läuft nach prognose-v36.py. Ein zweiter Lauf ändert nichts."""
import json, os
p = 'steuerrechner/index.html'
s = open(p, encoding='utf-8').read()
if 'Rechenkern Version 41' in s:
    raise SystemExit
W = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kern-v41-werte.json'), encoding='utf-8'))
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)
js = lambda x: json.dumps(x, ensure_ascii=False)

rep('const A = structuredClone(ANNAHMEN);', f'''// Rechenkern Version 41 (Buch Version 41, 17.11.2026): Stufe 4 mit zwei Dritteln, Ausweichen, Ergänzungssteuer, Chancen für alle,
// Bildung zählt wie Sparen, Schonfrist, Energie und Straßenfonds, Wertzuwachs der Häuser 2,5 %, Verhalten aus der Mikrosimulation mit Paket 9
Object.assign(ANNAHMEN, {js(W["A"])});
const A = structuredClone(ANNAHMEN);''')

rep('const mikro = (key, k) => {', f'''Object.assign(MIKRO, {js(W["MIKRO"])});   // Version 38/39: Stufe 4 über 60 % (p9), Schonfrist (sf, davon beim Plus sfp)
const STRF = {js(W["STRF"])};   // Version 40: Energie und Straßenfonds, Mrd. € je Reformjahr 2028 bis 2072 (positiv: fehlt dem Haushalt)
const mikro = (key, k) => {{''')

# Anteil am Hauswert als Barwert (Version 41)
rep('  A.AntL = 2 * A.AntJahre - 2 * ((1 + A.AntWert) ** A.AntJahre - 1) / A.Zins;',
    '  A.AntL = 2 * (1 - ((1 + A.AntWert) / (1 + A.Zins)) ** A.AntJahre) / A.Zins;   // Version 41: Barwert')

# neue Funktionen Jahr für Jahr (wie im Rechenkern)
rep('function kredit(saldoS, saldoL, jahre = 45, s4 = [0, 0]) {', '''// Version 37/38: Chancen für alle und Bildung zählt wie Sparen (Mrd. € im Jahr)
function chancen() { return A.ChAn * (A.ChSchule + A.ChMentor + A.ChAbschluss - A.ChAbschlussSpar + A.ChLesen + A.ChWerkstatt + A.ChHaft - A.ChHaftSpar + A.ChGrESt); }
function bildungSpar() { return A.BSpAn * (A.BSpGeb + A.BSpMehr) * A.BSpSatz; }
// Version 38: Erhöhung der Stufe 4 auf zwei Drittel, Ergänzungssteuer, Ausweichen; Version 39: Schonfrist; Version 40: Energie und Straßenfonds
function s4Zwei(k) { return A.S4Mikro > 0 && k <= A.Stufe4Jahre ? mikro("p9", k) * (A.Satz4 - 1.5) / 0.5 : 0; }
function ergJ(k) { return A.ErgAn * (A.ErgStart + (A.ErgLang - A.ErgStart) * Math.min(1, (k - 1) / A.ErgJahre)); }
function auswJ(k, s4) { return k > A.Stufe4Jahre ? 0 : A.AuswAn * A.AuswStart * (1 + ((s4[0] > 0 ? s4[1] / s4[0] : 1) - 1) * Math.min(1, (k - 1) / A.Jahre)); }
function schonfristJ(k) { return A.SfAn * mikro("sf", k); }
function schonfristPlusJ(k) { return A.SfAn * mikro("sfp", k); }
function strassenfondsJ(k) { return A.SFAn * STRF[Math.min(Math.max(k, 1), STRF.length) - 1]; }
function kredit(saldoS, saldoL, jahre = 45, s4 = [0, 0]) {''')
rep('''    steuer.push(((y - 1 >= A.Jahre) ? saldoL : sb + (saldoL - sb) * (y - 1) / A.Jahre) - u.hf - u.bs - zulageBeamte(y) - neueRegeln(y).sum + (y === 1 ? nj1 : 0)
      + (y <= A.Stufe4Jahre ? s4[0] + (s4[1] - s4[0]) * Math.min(1, (y - 1) / A.Jahre) : 0));''',
    '''    steuer.push(((y - 1 >= A.Jahre) ? saldoL : sb + (saldoL - sb) * (y - 1) / A.Jahre) - u.hf - u.bs - zulageBeamte(y) - neueRegeln(y).sum + (y === 1 ? nj1 : 0)
      - schonfristJ(y)   // Version 39: Schonfrist
      + (y <= A.Stufe4Jahre ? s4[0] + (s4[1] - s4[0]) * Math.min(1, (y - 1) / A.Jahre) : 0) + s4Zwei(y));   // Version 38: dazu die Erhöhung auf zwei Drittel''')
rep('  const ag = ausgleichPfad(ny, miet), vh = verhalten(steuer, ag);',
    '''  const ag = ausgleichPfad(ny, miet);
  // Version 39: Schonfrist, der Teil bei Haushalten mit Plus zählt dort, der Rest senkt das Minus der übrigen
  const vh = verhalten(steuer, ag.map((a, i) => { const d = schonfristJ(i + 1) - schonfristPlusJ(i + 1); return { ...a, plus: a.plus - d, minus: a.minus + d }; }));''')
rep('    const B = gleich[y - 1] + vh[y - 1];',
    '    const B = gleich[y - 1] + vh[y - 1] + ergJ(y) - auswJ(y, s4) - strassenfondsJ(y);   // Version 38: Ergänzungssteuer und Ausweichen, Version 40: Energie und Straßenfonds')

# Gesamtrechnung: zwei neue Ausgaben
rep('    ["Altvermögenskonto: versteuertes Erspartes bleibt frei, mit Obergrenze (läuft aus)", nr1.avk, 0],',
    '''    ["Chancen für alle: Schulessen, Mentor, Abschluss, Lesen und Schreiben, Werkstatt, Haft als Neustart, erstes Zuhause ohne Grunderwerbsteuer", chancen(), chancen()],
    ["Bildung zählt wie Sparen: keine Ausgabensteuer auf Kurs- und Prüfungsgebühren für Abschlüsse und geprüfte Kurse", bildungSpar(), bildungSpar()],
    ["Altvermögenskonto: versteuertes Erspartes bleibt frei, mit Obergrenze (läuft aus)", nr1.avk, 0],''')

# Tabelle: Stufe 4, Ausweichen und Ergänzungssteuer unter dem Saldo (wie Blatt Gesamtrechnung, Zeilen 92 bis 97; langfristig 2072)
rep('''  h += `<tr class="sum"><td>Saldo bei gleichem Einkauf, ohne Ausgleich</td><td class="${g.saldoS >= 0 ? "pos" : "neg"}">${mrd(g.saldoS)}</td><td class="${g.saldoL >= 0 ? "pos" : "neg"}">${mrd(g.saldoL)}</td></tr>`;''',
    '''  h += `<tr class="sum"><td>Saldo bei gleichem Einkauf, ohne Ausgleich</td><td class="${g.saldoS >= 0 ? "pos" : "neg"}">${mrd(g.saldoS)}</td><td class="${g.saldoL >= 0 ? "pos" : "neg"}">${mrd(g.saldoL)}</td></tr>`;
  if (A.Stufe4Jahre > 0) {
    const sS = saldoMitStufe4(g, false), sL = saldoMitStufe4(g, true);
    h += row(`Stufe 4 mit 60 % auf den Teil der Ausgaben über ${eur(A.Stufe4Monat)} im Monat je Erwachsenem`, g.s4[0], g.s4[1]);
    if (A.Satz4 !== 1.5) h += row(`Stufe 4: was ${A.Satz4 === 2 ? "zwei Drittel" : pct(A.Satz4 / (1 + A.Satz4), 0)} statt 60 % mehr bringen`, s4Zwei(1), s4Zwei(45));
    if (A.AuswAn) h += row("Ausweichen an der obersten Stufe", -auswJ(1, g.s4), -auswJ(45, g.s4));
    if (A.ErgAn) h += row("Ergänzungssteuer der Konzerne", ergJ(1), ergJ(45));
    h += `<tr class="sum"><td>Saldo mit Stufe 4, Ausweichen und Ergänzungssteuer</td><td class="${sS >= 0 ? "pos" : "neg"}">${mrd(sS)}</td><td class="${sL >= 0 ? "pos" : "neg"}">${mrd(sL)}</td></tr>`;
  }''')
rep('function kredit(saldoS, saldoL, jahre = 45, s4 = [0, 0]) {', '''// Saldo bei gleichem Einkauf ohne Ausgleich, mit Stufe 4, Ausweichen und Ergänzungssteuer (Blatt Gesamtrechnung, Zeile 97; langfristig 2072)
function saldoMitStufe4(g, lang) { const k = lang ? 45 : 1, on = A.Stufe4Jahre > 0; return (lang ? g.saldoL : g.saldoS) + (on ? g.s4[lang ? 1 : 0] + s4Zwei(k) - auswJ(k, g.s4) : 0) + ergJ(k); }
function kredit(saldoS, saldoL, jahre = 45, s4 = [0, 0]) {''')
# Kacheln: dieselbe Größe wie Zeile 97
rep('const ohneA = `Bei gleichem Einkauf und ohne Ausgleich wären es ${mrd(g.saldoS + (A.Stufe4Jahre >= 99 ? g.s4[0] : 0))} Mrd. €.`;',
    'const ohneA = `Bei gleichem Einkauf und ohne Ausgleich wären es ${mrd(saldoMitStufe4(g, false))} Mrd. €.`;')
rep('  const sL4 = g.saldoL + (A.Stufe4Jahre >= 99 ? g.s4[1] : 0);', '  const sL4 = saldoMitStufe4(g, true);')

# Texte: zwei Drittel statt 60 %
rep('Nur für den Teil der Ausgaben über 5.000 € im Monat je Erwachsenem gehen von 100 € 60 € an die Steuer.',
    'Nur für den Teil der Ausgaben über 5.000 € im Monat je Erwachsenem gehen von 100 € zwei Drittel an die Steuer.')
rep('auf den Teil über 5.000 € im Monat 60 %, nie mehr.', 'auf den Teil über 5.000 € im Monat zwei Drittel, nie mehr.')
open(p, 'w', encoding='utf-8').write(s)
print('Staatsseite auf Rechenkern Version 41')
