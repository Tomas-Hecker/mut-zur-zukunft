#!/usr/bin/env python3
"""Tomas 24.11.2026, 16:37 UTC: Fahrten zur Arbeit zählen nicht als Ausgaben (19 ct je gefahrenem km, wie 38 ct je km einfacher Strecke,
für jedes Verkehrsmittel), dafür oberste Stufe 75 % über 5.000 € statt 66 %.
Läuft nach verkehr-v41.py und verkehr-texte-v41.py; zweiter Lauf ändert nichts."""
import json, re, sys
P = 'steuerrechner/index.html'
s = open(P, encoding='utf-8').read()
if 'ArbPausch' in s:
    print('schon drin'); sys.exit()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a)); s = s.replace(a, b)
# Sätze und Pfad der Kette
rep('Object.assign(ANNAHMEN, { Satz4: 0.66 / 0.34, Satz4Saldo: 2.0, VkPaket: 1 });',
    'Object.assign(ANNAHMEN, { Satz4: 0.66 / 0.34, Satz4Saldo: 2.0, VkPaket: 1 });\n'
    '// Tomas 24.11.2026, 16:37: Fahrten zur Arbeit werden von den Ausgaben abgezogen (ArbPausch € je gefahrenem km), oberste Stufe 75 %\n'
    'Object.assign(ANNAHMEN, { Satz4: 0.75 / 0.25, ArbPausch: 0.19 });')
pf = json.load(open('/mnt/project-files/rechenmodell-mikrosim/arbeitsweg-75-2026-11-24/kette-ertragspfad-arbeitsweg-75.json'))
pf = {k: round(v, 3) for k, v in pf.items() if int(k) <= 2071}
s, n = re.subn(r'const VK_PFAD = \{[^}]*\};', 'const VK_PFAD = ' + json.dumps(pf, separators=(',', ':')) + ';', s); assert n == 1
rep('// die 66 % (netto mit weniger Ausweichen rund 3,5 Mrd. €) stecken zusammen mit Aufschlag (ohne Lkw über 3,5 t) und Gutschrift für den Arbeitsweg im Pfad VK_PFAD',
    '// seit 24.11.2026, 16:37: die 75 % und der Abzug der Fahrten zur Arbeit (19 ct je km) stecken zusammen mit Aufschlag (ohne Lkw über 3,5 t) und Gutschrift für den Arbeitsweg im Pfad VK_PFAD (kette-ertragspfad-arbeitsweg-75.json)')
# Haushalt: Abzug der Fahrten zur Arbeit; heute die Entfernungspauschale (38 ct je km einfacher Strecke ab dem ersten km)
rep('  const frei = existenz + mehr + rentFrei + njFrei;', '  const frei = existenz + mehr + rentFrei + njFrei + A.ArbPausch * (h.arbkm || 0);   // Fahrten zur Arbeit zählen nicht als Ausgaben')
rep('    if (bpe > 0) wk += A.WKP;\n  }', '    if (bpe > 0) wk += A.WKP;\n  }\n  if (personen[0].bpe > 0 && h.arbkm > 0) wk += Math.max(0, A.ArbPausch * h.arbkm - A.WKP);   // heute: Entfernungspauschale statt Pauschbetrag')
rep('const ra = haushalt({ ...h, lohn1: 0, lohn2: 0, mini: 0, gewinn: 0, kap', 'const ra = haushalt({ ...h, arbkm: 0, lohn1: 0, lohn2: 0, mini: 0, gewinn: 0, kap')
rep('    const nf = haushalt({ ...h, lohn1: 0, std1: 0,', '    const nf = haushalt({ ...h, arbkm: 0, lohn1: 0, std1: 0,')
rep('"vollj", "unterhalt"];', '"vollj", "unterhalt", "arbkm"];')
rep('const LEER = { fl: 0, ', 'const LEER = { arbkm: 0, fl: 0, ')
rep('const needMore = ["mini", ', 'const needMore = ["arbkm", "mini", ')
rep('<div class="field"><label for="gewinn">Gewinn als Selbständige(r)</label>',
    '<div class="field"><label for="arbkm">Fahrten zur Arbeit, km im Jahr</label><input id="arbkm" type="number" min="0" step="500"><span class="hint">hin und zurück, mit jedem Verkehrsmittel; zählen mit 19 ct je km nicht als Ausgaben (heute: Entfernungspauschale)</span></div>\n'
    '            <div class="field"><label for="gewinn">Gewinn als Selbständige(r)</label>')
rep('<summary>Weitere Angaben: Selbständige, Unternehmen, Rente, Vermögen</summary>', '<summary>Weitere Angaben: Arbeitsweg, Selbständige, Unternehmen, Rente, Vermögen</summary>')
# Energie und Auto: Arbeitsweg aus dem Feld oben
i = s.index('<div class="field"><label for="e_arb">'); j = s.index('</div>', i) + 6
s = s[:i] + '<p class="note field wide" style="margin:0">Die Fahrten zur Arbeit stehen oben unter „Weitere Angaben“. Auf dem Weg zur Arbeit wird das Fahren nie teurer als heute.</p>' + s[j:]
rep('arb: Math.min(n("e_arb"), n("e_km")), ', 'arb: Math.min(n("arbkm"), n("e_km")), ')
# Texte
for a, b in [
 ('Nur für den Teil der Ausgaben über 5.000 € im Monat je Erwachsenem gehen von 100 € 66 € an die Steuer.', 'Nur für den Teil der Ausgaben über 5.000 € im Monat je Erwachsenem gehen von 100 € 75 € an die Steuer. Fahrten zur Arbeit zählen nicht als Ausgaben: 19 ct je gefahrenem km werden abgezogen, wie heute die Entfernungspauschale.'),
 ('auf den Teil über 5.000 € im Monat 66 %, nie mehr.', 'auf den Teil über 5.000 € im Monat 75 %, nie mehr.'),
 ('"66 % (194 % Aufschlag)","Aufschlag von rund 194 % auf die Ausgaben über dem Beginn von Stufe 4: Von 100 €, die dafür ins Private fließen, gehen 66 € an die Steuer, für 34 € wird eingekauft.',
  '"75 % (300 % Aufschlag)","Aufschlag von 300 % auf die Ausgaben über dem Beginn von Stufe 4: Von 100 €, die dafür ins Private fließen, gehen 75 € an die Steuer, für 25 € wird eingekauft.'),
 ('seit dem Verkehrspaket vom 24.11.2026 66 %, bezahlt vom Aufschlag auf die Kilometerabgabe (Lkw über 3,5 t zahlen ihn nicht). Der Staatshaushalt rechnet wie das Rechenmodell weiter mit zwei Dritteln und zieht die 66 % mit dem geringeren Ausweichen netto im Pfad des Verkehrspakets ab, rund 3,5 Mrd. € im Jahr.',
  'seit dem 24.11.2026 75 %, damit die Fahrten zur Arbeit nicht als Ausgaben zählen (19 ct je gefahrenem km): 2028 bringen 75 statt 66 % rund 38,6 Mrd. €, der Abzug kostet rund 33,4 Mrd. €, netto bleiben rund 5,2 Mrd. € für die Tilgung. Der Staatshaushalt rechnet wie das Rechenmodell weiter mit zwei Dritteln und nimmt Stufe, Abzug und Verkehrspaket als Pfad dazu.'),
 ('im mittleren Fall 2099 schuldenfrei. Im vorsichtigen Fall steigt der Normalsatz der Mehrwertsteuer ab 2030 um gut 8,9 Punkte', 'im mittleren Fall 2093 schuldenfrei. Im vorsichtigen Fall steigt der Normalsatz der Mehrwertsteuer ab 2030 um gut 8,3 Punkte'),
 ('im vorsichtigen Fall aus Anhang C9 ab 2030 gut 8,9 Punkte', 'im vorsichtigen Fall aus Anhang C9 ab 2030 gut 8,3 Punkte'),
 ('im zuversichtlichen Fall ab 2033, im mittleren Fall ab 2038.', 'im zuversichtlichen Fall ab 2033, im mittleren Fall ab 2037.'),
 ('gelten 66 % (Stufe 4, bis zum Verkehrspaket zwei Drittel).', 'gelten 75 % (Stufe 4, bis 24.11.2026 zwei Drittel); Fahrten zur Arbeit zählen nicht als Ausgaben.'),
 ('66 % statt der Hälfte an die Steuer (Satz4)', '75 % statt der Hälfte an die Steuer (Satz4)'),
 ('im Monat 66 % Ausgabensteuer und auf die übrigen 34 % die Mehrwertsteuer von 50 %, zusammen rund 77 %', 'im Monat 75 % Ausgabensteuer und auf die übrigen 25 % die Mehrwertsteuer von 50 %, zusammen rund 83 %'),
  ('im zuversichtlichen Fall 2056 und im mittleren Fall 2093', 'im zuversichtlichen Fall 2055 und im mittleren Fall 2093'),
 ('schuldenfrei wird der Staat dann 2091 (Anhang C9)', 'schuldenfrei wird der Staat dann 2090 (Anhang C9)'),
]:
    rep(a, b)
open(P, 'w', encoding='utf-8').write(s); print('ok')
