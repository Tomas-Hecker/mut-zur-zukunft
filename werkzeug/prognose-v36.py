#!/usr/bin/env python3
"""Schuldenprognose des Steuerrechners auf Buch Version 36 (Paket 6), wie schulden/kern19.py und zp19.py mit V36=J.
Quelle: broschuere-mut-zur-zukunft/version-35/staat-schulden-umbau-v36.md (16.11.2026):
Wachstum im mittleren Fall 5,775 %, Kitas und Forschung (KIFO), Zins mit Zukunftsplan ab 2028 von 3,24 % in 7 Jahren auf 3 %,
Ausgabenregel mit Deckel 3 statt 2 % des BIP, keine eigenen Verwaltungseinsparungen, 16,8 Mrd. € je Punkt (netto 14,8).
Läuft nach kern-v36.py. Ein zweiter Lauf ändert nichts."""
p = 'steuerrechner/index.html'
s = open(p, encoding='utf-8').read()
if 'Prognose Version 36' in s:
    raise SystemExit
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)

rep('const A = structuredClone(ANNAHMEN);', '''// Prognose Version 36 (wie schulden/kern19.py mit V36=J): Wachstum mittel 8,9 x 0,75 - 0,9 = 5,775 %, Kitas und Forschung je Fall,
// Ausgabenregel mit Deckel 3 % des BIP, 16,8 Mrd. € je Punkt
Object.assign(ANNAHMEN.Prognose.mittel, { wachs: (8.9 * 0.75 - 0.9) / 100 });
Object.assign(ANNAHMEN.Prognose.vorsichtig, { kita: 0.001, forsch: 0.004 });
Object.assign(ANNAHMEN.Prognose.mittel, { kita: 0.002, forsch: 0.007 });
Object.assign(ANNAHMEN.Prognose.zuversichtlich, { kita: 0.003, forsch: 0.015 });
Object.assign(ANNAHMEN.Prognose.Plan, { AusgMax: 0.03, NJP: 16.8, Verw: 0, ZinsR: 0.03, ZinsStart: 0.0324, ZinsJahre: 7 });
ANNAHMEN.Prognose.KIFO = { kita: 5, kitaJahre: 5, forsch: 10, forschJahre: 10, proto: 1, anerk: 0.5, staat: 0.4, kitaVon: 2028, kitaBis: 2048, forschVon: 2033, forschBis: 2058 };
const A = structuredClone(ANNAHMEN);''')

rep('function prognose(sz, fall, saldoPfad, fixPkt = 0) {', '''// Kitas und Forschung des Staates im Zukunftsplan (kern19.py: kifo_kosten, kifo_gr, kifo_pb)
function kifoKosten(y) {
  const F = A.Prognose.KIFO, s = A.Prognose.ReformStart;
  if (y < s) return 0;
  const k = y - s + 1;
  return F.kita * Math.min(1, k / F.kitaJahre) + F.forsch * Math.min(1, k / F.forschJahre) + F.proto + F.anerk;
}
function kifoGr(c, y) {
  const F = A.Prognose.KIFO;
  return (y >= F.kitaVon && y < F.kitaBis ? (c.kita || 0) / (F.kitaBis - F.kitaVon) : 0) + (y >= F.forschVon && y < F.forschBis ? (c.forsch || 0) / (F.forschBis - F.forschVon) : 0);
}
function kifoPb(c, y) {
  const F = A.Prognose.KIFO;
  return F.staat * ((c.kita || 0) * ramp(y, F.kitaVon, F.kitaBis) + (c.forsch || 0) * ramp(y, F.forschVon, F.forschBis)) - kifoKosten(y) / A.BIP;
}
function prognose(sz, fall, saldoPfad, fixPkt = 0) {''')
rep('    g = g + (interp(y, P.ZinsNeu) - g) / P.TBLaufzeit;',
    '''    // Version 35: mit Zukunftsplan Zins auf neue Schulden ab 2028 von 3,24 % in 7 Jahren auf 3 %
    const zNeu = plan && Q.ZinsR != null && y >= P.ReformStart ? Q.ZinsStart + (Q.ZinsR - Q.ZinsStart) * Math.min(1, (y - P.ReformStart) / Q.ZinsJahre) : interp(y, P.ZinsNeu);
    g = g + (zNeu - g) / P.TBLaufzeit;''')
rep('    if (plan && y >= 2028 && y < 2048) gr += c.binnen / 20;\n',
    '    if (plan && y >= 2028 && y < 2048) gr += c.binnen / 20;\n    if (plan) gr += kifoGr(c, y);   // Kitas und Forschung\n')
rep('+ 10.7 / A.BIP * ramp(y, 2028, 2043) +', '+ (Q.Verw ?? 10.7) / A.BIP * ramp(y, 2028, 2043) +')
rep('      pb += Q.AusgBasis - b + Q.Subv * ramp(y, 2028, 2031) + c.ern * ramp(y, 2030, 2050);\n',
    '      pb += Q.AusgBasis - b + Q.Subv * ramp(y, 2028, 2031) + c.ern * ramp(y, 2030, 2050);\n      pb += kifoPb(c, y);   // Kitas und Forschung: Erträge minus Kosten\n')
# Text unter der Grafik: Kitas und Forschung gehören zum Plan; zur Schuldenbremse nur, was stimmt (schuldenbremse-uebergang-v36.txt)
rep('Gesundheit, eine schlankere Verwaltung, Bildung, weniger Finanzhilfen,', 'Gesundheit, eine schlankere Verwaltung, Bildung, Kitas und Forschung, weniger Finanzhilfen,')
rep('; die Defizite der ersten Jahre erlauben Schuldenbremse und Verteidigungsausnahme.', '. Für den Kredit der ersten Jahre braucht es eine eigene Übergangsregel im Grundgesetz.')
open(p, 'w', encoding='utf-8').write(s)
print('Schuldenprognose auf Version 36')
