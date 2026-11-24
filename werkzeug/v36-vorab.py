#!/usr/bin/env python3
"""Steuerrechner vorab auf Paket 6 (Buch Version 36), bis Rechenkern und Register vom Buch kommen.
Quelle: broschuere-mut-zur-zukunft/version-35/rechner-v36-stufe4.md und beispiele-rechner-v36-roh.json (16.11.2026):
Freibetrag 1.200 € im Monat (Grenze1 = Grenze2 = 2.052), Stufe 4 dauerhaft (Stufe4Jahre 99, Satz4 1,5 = 60 % vom Geld, das ins
Private fließt, über 5.000 € Ausgaben im Monat je Erwachsenem). Die Stufe 4 steckt im Haushalt in tarif() und xtInv().
In der Gesamtrechnung bleibt sie ein eigener Posten (stufe4()), Aufkommen und Bausteine rechnen mit tarifG (ohne Stufe 4, Raster FBGesamt), sonst zählte sie doppelt.
Läuft nach v35-vorab.py. Ein zweiter Lauf ändert nichts."""
p = 'steuerrechner/index.html'
s = open(p, encoding='utf-8').read()
if 'Vorab Paket 6' in s:
    raise SystemExit
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)

rep('const A = structuredClone(ANNAHMEN);', '''// Vorab Paket 6 (Buch Version 36): Freibetrag 1.200 € im Monat, Stufe 4 dauerhaft mit 60 % über 5.000 € im Monat
Object.assign(ANNAHMEN, { Grenze1: 2052, Grenze2: 2052, Stufe4Jahre: 99, Satz4: 1.5 });
Object.assign(ANNAHMEN.SicherheitWerte, { Grenze1: 2052, Grenze2: 2052 });
const A = structuredClone(ANNAHMEN);''')

# Tarif: Stufe 4 im Haushalt, wenn sie dauerhaft gilt (wie ctax im Rechenkern); tarifG für Aufkommen und Bausteine des Staates
rep('''function tarif(x) { // Ausgabensteuer je Erwachsenem auf Ausgaben x über dem Existenzminimum
  x = Math.max(0, x);
  return A.Satz1 * Math.min(x, A.Grenze1) + A.Satz2 * Math.max(0, Math.min(x, A.Grenze2) - A.Grenze1) + A.Satz3 * Math.max(0, x - Math.max(A.Grenze1, A.Grenze2));
}''', '''function tarif(x) { // Ausgabensteuer je Erwachsenem auf Ausgaben x über dem Existenzminimum
  x = Math.max(0, x);
  return A.Satz1 * Math.min(x, A.Grenze1) + A.Satz2 * Math.max(0, Math.min(x, A.Grenze2) - A.Grenze1) + A.Satz3 * Math.max(0, x - Math.max(A.Grenze1, A.Grenze2))
    + (A.Stufe4Jahre >= 99 ? (A.Satz4 - A.Satz3) * Math.max(0, x - A.Grenze3) : 0);   // Paket 6: Stufe 4 dauerhaft (wie ctax im Rechenkern)
}
// Version 36 (wie ctax_g im Rechenkern): Tarif der Hochrechnung und der Bausteine, ohne Stufe 4 und auf dem Raster mit FBGesamt;
// was der Freibetrag darüber kostet und die Stufe 4 stehen als eigene Posten in der Gesamtrechnung
function tarifG(x) {
  x = Math.max(0, x);
  const g1 = A.Grenze1G ?? A.Grenze1, g2 = A.Grenze2G ?? A.Grenze2;
  return A.Satz1 * Math.min(x, g1) + A.Satz2 * Math.max(0, Math.min(x, g2) - g1) + A.Satz3 * Math.max(0, x - Math.max(g1, g2));
}''')
rep('''  if (C <= f2) return F0 + E * G1 + (C - f1) / (1 + A.Satz2);
  return F0 + E * G2 + (C - f2) / (1 + A.Satz3);''', '''  if (C <= f2) return F0 + E * G1 + (C - f1) / (1 + A.Satz2);
  if (A.Stufe4Jahre >= 99 && A.Grenze3 > G2) {   // Paket 6: vierte Stufe (wie xt_inv im Rechenkern)
    const G3 = A.Grenze3, f3 = f2 + (1 + A.Satz3) * E * (G3 - G2);
    if (C > f3) return F0 + E * G3 + (C - f3) / (1 + A.Satz4);
  }
  return F0 + E * G2 + (C - f2) / (1 + A.Satz3);''')
# Gesamtrechnung: Aufkommen und Bausteine ohne Stufe 4, sie kommt als eigener Posten dazu
rep('  for (const z of Z) s += tarif(Math.exp(mu + A.Sigma * z) - exm);', '  for (const z of Z) s += tarifG(Math.exp(mu + A.Sigma * z) - exm);')
rep('(A.RentN * (tarif(rx) - tarif(Math.max(0, rx - A.RentVerd)))', '(A.RentN * (tarifG(rx) - tarifG(Math.max(0, rx - A.RentVerd)))')
rep('(A.RMiniN * (tarif(xm) - tarif(Math.max(0, xm - 12 * A.RMiniV))) + A.RMidiN * (tarif(xd) - tarif(Math.max(0, xd - miniFrei(12 * A.RMidiV)))))',
    '(A.RMiniN * (tarifG(xm) - tarifG(Math.max(0, xm - 12 * A.RMiniV))) + A.RMidiN * (tarifG(xd) - tarifG(Math.max(0, xd - miniFrei(12 * A.RMidiV)))))')
rep('(tarif(xh) - tarif(Math.max(0, xh - rentMehr(A.RMehrW, A.RMehrH))))', '(tarifG(xh) - tarifG(Math.max(0, xh - rentMehr(A.RMehrW, A.RMehrH))))')
rep('const K = g.e * (tarif(g.ue / g.e) - tarif(Math.max(0, g.ue - J) / g.e));', 'const K = g.e * (tarifG(g.ue / g.e) - tarifG(Math.max(0, g.ue - J) / g.e));')
# Haushalt: der getrennte Hinweis auf die befristete Stufe 4 entfällt, sie steckt dauerhaft im Ergebnis
rep('const s4 = A.Stufe4Jahre > 0 ? h.erw', 'const s4 = A.Stufe4Jahre > 0 && A.Stufe4Jahre < 99 ? h.erw')
rep('function stufe4(mitMiete) { // Mehreinnahmen der befristeten Stufe 4, Mrd. €', 'function stufe4(mitMiete) { // Mehreinnahmen der Stufe 4, Mrd. € (Paket 6: dauerhaft)')

# Texte
rep('Bis 13.920 € Ausgaben im Jahr (1.160 € im Monat) je Erwachsenem', 'Bis 14.400 € Ausgaben im Jahr (1.200 € im Monat) je Erwachsenem')
rep('''<p>Bis zu Ausgaben von 1.150 € im Monat je Erwachsenem (und 589 € je Kind) bleibt alles frei. Darüber gibt es nur einen Satz: Von 100 €, die ins Private fließen, gehen 50 € an die Steuer, für 50 € wird eingekauft. Das ist ein Aufschlag von 100 % auf die Ausgaben.''',
    '''<p>Bis zu Ausgaben von 1.200 € im Monat je Erwachsenem (und 589 € je Kind) bleibt alles frei. Darüber gilt ein Satz: Von 100 €, die ins Private fließen, gehen 50 € an die Steuer, für 50 € wird eingekauft. Das ist ein Aufschlag von 100 % auf die Ausgaben. Nur für den Teil der Ausgaben über 5.000 € im Monat je Erwachsenem gehen von 100 € 60 € an die Steuer.''')
rep('also wie im Preis, sind das 50 %, nie mehr.', 'also wie im Preis, sind das 50 %, auf den Teil über 5.000 € im Monat 60 %, nie mehr.')
rep('gehört zu 50 % der Gemeinschaft. Frei bleiben 400.000 € je Nachlass für Kinder und Enkel,',
    'gehört zu 50 % der Gemeinschaft. Frei bleiben 400.000 € je Nachlass für Kinder und Enkel; übrige Erben haben 20.000 € frei, darüber gehören 60 % der Gemeinschaft;')
open(p, 'w', encoding='utf-8').write(s)
print('Steuerrechner vorab auf Paket 6')
