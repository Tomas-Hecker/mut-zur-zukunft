#!/usr/bin/env python3
"""Tomas 27.11.2026: Umzugshilfe 5.000 € statt Startprämie plus 1 Mrd. € für Verfahren und Familie (14:31 UTC),
Mentoren-Netz beim Berufscoach, ein Coach je 900 statt 750 Menschen, Netz 0,2 Mrd. € (14:55 UTC),
dazu mehr Fachkräfte durch Einwanderung wie die Kette (rechenmodell-mikrosim/alterung-2026-11-27/einwanderung-kette.md):
Wachstum mittel +0,946 %, zuversichtlich +1,893 % über 20 Jahre, Primärsaldo +0,0405 / +0,0811 % des BIP,
Freibetrag verteilt auf 0,95 / 1,9 % mehr Erwachsene. Läuft nach ergaenzungen-v41.py; zweiter Lauf ändert nichts."""
import sys
P = 'steuerrechner/index.html'
s = open(P, encoding='utf-8').read()
if 'MentNetz' in s:
    print('schon drin'); sys.exit()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a)); s = s.replace(a, b)
rep('Object.assign(ANNAHMEN, { Satz4: 0.75 / 0.25, ArbPausch: 0.19 });',
    'Object.assign(ANNAHMEN, { Satz4: 0.75 / 0.25, ArbPausch: 0.19 });\n'
    '// Tomas 27.11.2026: Umzugshilfe 5.000 € statt Startprämie, Verfahren und Familie 1 Mrd. €, Mentoren-Netz (ein Coach je 900 statt 750), Einwanderung wie die Kette\n'
    'Object.assign(ANNAHMEN, { StartGrund: 5000, StartSatz: 0, VerfFam: 1.0, CoachN: 70000 * 750 / 900, MentNetz: 0.2 });')
z = 'Object.assign(ANNAHMEN.Prognose.zuversichtlich, { wachs: 0.191075, ki: 0, chancen: 1.8518518518518519, sockel: 0.01, auto: 0.01 });'
rep(z, z + '\n// Tomas 27.11.2026: mehr Fachkräfte durch Einwanderung wie die Kette (EINW_G, EINW_PB, Freibetrag auf mehr Erwachsene)\n'
    'Object.assign(ANNAHMEN.Prognose.mittel, { wachs: 0.0685 + 0.00946, pbx: ANNAHMEN.Prognose.mittel.pbx + 0.000405, einwAnt: 0.0095 });\n'
    'Object.assign(ANNAHMEN.Prognose.zuversichtlich, { wachs: 0.191075 + 0.01893, pbx: ANNAHMEN.Prognose.zuversichtlich.pbx + 0.000811, einwAnt: 0.019 });')
rep('    ["Startprämie für Fachkräfte aus dem Ausland", start, start],',
    '    ["Umzugshilfe für Fachkräfte aus dem Ausland, " + eur(A.StartGrund) + " je Fachkraft", start, start],\n'
    '    ["Schnelle Verfahren und Hilfe für die Familie: Visum und Anerkennung aus einer Hand, Kitaplatz, Arbeitssuche für den Partner", A.VerfFam, A.VerfFam],')
rep('    ["Berufscoach für alle, mit KI-Lernguthaben von " + eur(A.KILernEur) + " im Monat", coach, coach],',
    '    ["Berufscoach für alle, mit KI-Lernguthaben von " + eur(A.KILernEur) + " im Monat", coach, coach],\n'
    '    ["Mentoren-Netz bei den Kammern: ein Mentor aus deinem Beruf, freiwillig", A.MentNetz, A.MentNetz],')
rep('    out.push({ jahr: y, v: d, mw: need * A.BIP / njp + (regel && y >= Q.FixAb ? fixPkt : 0), pb, aus, netto, brutto });',
    '    out.push({ jahr: y, v: d, mw: need * A.BIP / njp + (regel && y >= Q.FixAb ? fixPkt : 0), pb, aus, netto, brutto: brutto / (1 + (c.einwAnt || 0) * Math.min(1, Math.max(0, (y - 2027) / 20))) });   // Freibetrag verteilt auf mehr Erwachsene')
# Texte
for a, b, n in [
 ('Fachkräfte aus dem Ausland bekommen eine Startprämie von 15.000 € plus 20 % des Gehalts über 30.000 €.',
  'Fachkräfte aus dem Ausland bekommen 5.000 € für den Umzug; wichtiger ist, dass alles schnell geht: Visum und Anerkennung aus einer Hand, ein Kitaplatz und Hilfe bei der Arbeitssuche für den Partner.', 1),
 ('"StartAn","Startprämie für Fachkräfte aus dem Ausland (1 = an)","Vorschlag","1","Schalter: Jede neue Fachkraft aus dem Ausland bekommt eine Startprämie, als Ausgleich für die Bildung, die ihr Herkunftsland bezahlt hat, gegen die Zusage, mindestens fünf Jahre zu bleiben. Kosten: 0,2 Mio. × (15.000 € + 20 % × 23.000 €) = 3,9 Mrd. €.',
  '"StartAn","Umzugshilfe für Fachkräfte aus dem Ausland (1 = an)","Vorschlag","1","Schalter: Jede neue Fachkraft aus dem Ausland bekommt 5.000 € für den Umzug (Tomas, 27.11.2026, statt der früheren Startprämie). Kosten: 0,2 Mio. × 5.000 € = 1,0 Mrd. €. Dazu 1 Mrd. € im Jahr für schnelle Verfahren und die Familie (VerfFam). Wer wieder geht, geht meist wegen der Familie oder der Bürokratie.', 1),
 ('"StartN","Fachkräfte mit Startprämie pro Jahr"', '"StartN","Fachkräfte mit Umzugshilfe pro Jahr"', 1),
 ('"StartGrund","Startprämie: Grundbetrag","Vorschlag","15.000 €","Grundbetrag 15.000 €, so viel, wie Umzug, Kaution, die Einrichtung der ersten Wohnung und ein Sprachkurs etwa kosten.',
  '"StartGrund","Umzugshilfe je Fachkraft","Vorschlag","5.000 €","5.000 € für den Umzug (bis 27.11.2026 Startprämie von 15.000 € plus 20 % des Gehalts über 30.000 €).', 1),
 ('"StartSatz","Startprämie: Anteil am Jahresgehalt über der Schwelle","Vorschlag","20 %","Dazu 20 % des Jahresgehalts über der Schwelle.',
  '"StartSatz","Anteil am Jahresgehalt über der Schwelle","Vorschlag","0 %","Seit der Umzugshilfe (27.11.2026) kein Anteil am Gehalt mehr, vorher 20 %.', 1),
 ('"StartAb","Startprämie: Schwelle"', '"StartAb","Schwelle für den früheren Anteil am Gehalt"', 1),
 ('"CoachN","Berufscoaches mit KI-Unterstützung","Annahme","70.000 Personen","Mit KI-Unterstützung begleitet ein Coach rund 750 Menschen im Erwerbsalter; dafür braucht es rund 70.000 Coaches.',
  '"CoachN","Berufscoaches mit KI-Unterstützung","Annahme","58.300 Personen","Mit KI-Unterstützung und einem freiwilligen Mentoren-Netz bei den Kammern begleitet ein Coach rund 900 Menschen im Erwerbsalter; dafür braucht es rund 58.300 Coaches (2028 rund 19.400, 2029 rund 38.900). Das Netz kostet rund 0,2 Mrd. € im Jahr (MentNetz), zusammen spart das rund 0,8 Mrd. € für die Tilgung.', 1),
 ('im zuversichtlichen Fall 2056 und im mittleren Fall 2095', 'im zuversichtlichen Fall 2055 und im mittleren Fall 2092', 1),
 ('im zuversichtlichen Fall ab 2033, im mittleren Fall ab 2038.', 'im zuversichtlichen Fall ab 2032, im mittleren Fall ab 2037.', 1),
 ('ab 2030 um rund 8,6 Punkte', 'ab 2030 um rund 8,4 Punkte', 1),
 ('im vorsichtigen Fall aus Anhang C9 ab 2030 rund 8,6 Punkte', 'im vorsichtigen Fall aus Anhang C9 ab 2030 rund 8,4 Punkte', 1),
 ('fehlen im ersten Jahr rund 56 Mrd.', 'fehlen im ersten Jahr rund 54 Mrd.', 4),
 ('im zweiten rund 64 Mrd.', 'im zweiten rund 61 Mrd.', 3),
 ('im dritten rund 50 Mrd.', 'im dritten rund 48 Mrd.', 2),
 ('2070 rund 36 Mrd.', '2070 rund 39 Mrd.', 1),
 ('2070 von rund 36 Mrd.', '2070 von rund 39 Mrd.', 1),
]:
    rep(a, b, n)
open(P, 'w', encoding='utf-8').write(s); print('ok')
