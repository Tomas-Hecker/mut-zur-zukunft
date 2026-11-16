#!/usr/bin/env python3
"""Steuerrechner vorab auf Version 35, bis Annahmen-Register und Rechenkern V35 vom Buch kommen (Absprache 16.11.2026, 06:08 UTC).
Werte aus broschuere-mut-zur-zukunft/version-35/werte-v35.json und beispiele-rechner-v35-roh.json („nachher“):
Prämie 40 € im Monat, Freibetrag 1.160 € (Grenze 1.572), ExMinPlus 564, Bürgerjob BJPlus 778,8; alter Ausgleich (10 € je Erwachsenem,
Rentner bis 300 €) aus; neu: Zuschlag zur Rente, damit die Rente heutiger Rentner 4 % mehr kauft (rpz), Beamte und Pensionäre in BeamtAusgl.
rpz = AusgRPAn × max(0, AusgRPProz × N − V) im Normfall (derselbe Haushalt lebt nur von seiner Rente, gibt sie ganz aus, ohne Haus, ohne Sparen):
N = Nettorente heute, V = Plus der Reform im Normfall. Staat: 9,73 Mrd. € im ersten Jahr, schmilzt nach AusgRPA ab.
Läuft als letzter Schritt nach gen.py. Ein zweiter Lauf ändert nichts. Entfällt, sobald das Register V35 eingespielt ist."""
p = 'steuerrechner/index.html'
s = open(p, encoding='utf-8').read()
if 'Vorab Version 35' in s:
    raise SystemExit
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)

rep('const A = structuredClone(ANNAHMEN);', '''// Vorab Version 35 (bis Register und Rechenkern V35 vom Buch kommen): Werte aus werte-v35.json
Object.assign(ANNAHMEN, { KVPraem: 480, ExMinPlus: 564, Grenze1: 1572, Grenze2: 1572, BJPlus: 778.8, AusgAn: 0,
  AusgRPAn: 1, AusgRPProz: 0.04, AusgRP0: 9.73, AusgRPA: [0.85236, 0.63417, 0.40538, 0.20743, 0.07488, 0.01571, 0.00154, 0.00012, 0.00001], BeamtAusgl: 10.81 });
Object.assign(ANNAHMEN.SicherheitWerte, { Grenze1: 1572, Grenze2: 1572 });
const A = structuredClone(ANNAHMEN);''')

# Haushalt: Zuschlag zur Rente (rpz) wie der Ausgleich ins Plus und in die Kaufkraft
rep('''  const ausgl = ausgB + ausgR;''', '''  // Version 35: Zuschlag zur Rente für heutige Rentner, damit die Rente im Normfall AusgRPProz mehr kauft als heute
  let rpz = 0;
  if (A.AusgRPAn && h.bs && h.rente > 0 && !h._norm) {
    const nf = haushalt({ ...h, lohn1: 0, std1: 0, lohn2: 0, std2: 0, mini: 0, gewinn: 0, kap: 0, gmbh: 0, aus: 0, verm: 0, transfer: 0, pkv: 0, vorsorge: 0,
      miet: 0, hb: 0, spar: 0, vollj: 0, unterhalt: 0, bjob: 0, bs: 1, rentner: 1, _norm: true, _cap: false });
    const N = nf.verf - nf.kg;
    rpz = Math.max(0, A.AusgRPProz * N - nf.vgl);
  }
  const ausgl = ausgB + ausgR + rpz;''')
rep('''    praemie, pvPriv, ausSum, agRP,''', '''    rpz, praemie, pvPriv, ausSum, agRP,''')
rep('''    if (r.ausgB + r.ausgR > 0.5) t.push(''', '''    if (r.rpz > 0.5) t.push(`Zuschlag zur Rente: Wer beim Start schon Rente bezieht, hat mit seiner Rente bei gleichem Einkauf mindestens ${pct(A.AusgRPProz, 0)} mehr Geld als heute: ${eur(r.rpz)} im Jahr`);
    if (r.ausgB + r.ausgR > 0.5) t.push(''')

# Staat: Zuschlag zur Rente schmilzt ab, solange die heutigen Rentner leben
rep('''function rentnerAnteil(n) {''', '''function rpAnteil(n) { const t = [1, ...A.AusgRPA], j = Math.floor(n / 5); return j >= t.length - 1 ? 0 : t[j] + (t[j + 1] - t[j]) * (n - 5 * j) / 5; }
function rentnerAnteil(n) {''')
rep('''    const rent = A.AusgAn * A.AusgRent0 * rentnerAnteil(i);''',
    '''    const rent = A.AusgAn * A.AusgRent0 * rentnerAnteil(i) + (A.AusgRPAn || 0) * A.AusgRP0 * rpAnteil(i);''')
# Säulenbild: Prozentsatz des Zuschlags zur Rente nennen
rep('sbDaten(h, r, { kst: A.KStS })', 'sbDaten(h, r, { kst: A.KStS, rpzProzent: (A.AusgRPProz || 0) * 100 })')
# Name des Postens im Säulenbild: 4 % mehr Geld bei gleichem Einkauf, nicht 4 % mehr Kaufkraft (Buch, 16.11. 06:22 UTC, bis Tomas entscheidet)
rep('`${SB_NEU.rpz}: Sie kauft ${String(d.rpzProzent).replace(".", ",")}\\u00a0% mehr`', '`${SB_NEU.rpz}: bei gleichem Einkauf mindestens ${String(d.rpzProzent).replace(".", ",")}\\u00a0% mehr Geld`')
# Texte, die die neuen Werte nennen
rep('Bis 13.800 € Ausgaben im Jahr (1.150 € im Monat) je Erwachsenem', 'Bis 13.920 € Ausgaben im Jahr (1.160 € im Monat) je Erwachsenem')
rep('eine steuerfreie Prämie von 600 € im Jahr, 50 € im Monat;', 'eine steuerfreie Prämie von 480 € im Jahr, 40 € im Monat;')
rep('1.066 € zum Leben, 84 € Ausgleich der Mehrwertsteuer und 50 € Prämie.', '1.076 € zum Leben, 84 € Ausgleich der Mehrwertsteuer und 40 € Prämie.')
rep('wer im Bürgerjob arbeitet, bekommt zusätzlich 200 € (1.400 € im Monat);', 'wer im Bürgerjob arbeitet, verdient 21 Stunden in der Woche zum Mindestlohn, 1.265 € im Monat;')
rep('ein Bürgerjob mit Recht auf Arbeit für 1.400 € im Monat (200 € mehr als die Grundsicherung, wer stattdessen lernt, bekommt 1.200 €)',
    'ein Bürgerjob mit Recht auf Arbeit, 21 Stunden in der Woche zum Mindestlohn, 1.265 € im Monat (wer stattdessen lernt, bekommt 1.200 €)')
rep('Im Vorschlag 17 Stunden in der Woche im Bürgerjob, 1.400 € im Monat,', 'Im Vorschlag 21 Stunden in der Woche im Bürgerjob, 1.265 € im Monat,')
open(p, 'w', encoding='utf-8').write(s)
print('Steuerrechner vorab auf Version 35')
