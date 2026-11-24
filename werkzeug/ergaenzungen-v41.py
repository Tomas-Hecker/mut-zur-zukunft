#!/usr/bin/env python3
"""Tomas 24.11.2026 abends: Ergänzungen der Rechtsprüfung (Kinder an beiden Grenzen, Günstigerprüfung D2, Ticket, Arbeitgeber,
Zweitwohnung, große Käufe), Grenze der 75 % als Einkauf ohne Steuer (samt Steuer 8.800 €).
Läuft nach arbeitsweg-75.py; zweiter Lauf ändert nichts."""
import json, re, sys
P = 'steuerrechner/index.html'
s = open(P, encoding='utf-8').read()
if 'arbeitsweg-75-ergaenzungen' in s:
    print('schon drin'); sys.exit()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a)); s = s.replace(a, b)
pf = json.load(open('/mnt/project-files/rechenmodell-mikrosim/arbeitsweg-75-2026-11-24/kette-ertragspfad-arbeitsweg-75-ergaenzungen.json'))
pf = {k: round(v, 3) for k, v in pf.items() if int(k) <= 2071}
s, n = re.subn(r'const VK_PFAD = \{[^}]*\};', 'const VK_PFAD = ' + json.dumps(pf, separators=(',', ':')) + ';', s); assert n == 1
rep('im Pfad VK_PFAD (kette-ertragspfad-arbeitsweg-75.json)', 'im Pfad VK_PFAD (seit dem Abend des 24.11.2026 mit den Ergänzungen der Rechtsprüfung: kette-ertragspfad-arbeitsweg-75-ergaenzungen.json)')
# Texte (Kette: Kredit 299,7 Mrd. € bis 2036, getilgt 2048, schuldenfrei 2095/2056/2090, Freibetrag ab 2038, vorsichtig 8,65 Punkte)
for a, b, n in [
 ('im zuversichtlichen Fall ab 2033, im mittleren Fall ab 2037.', 'im zuversichtlichen Fall ab 2033, im mittleren Fall ab 2038.', 1),
 ('im zuversichtlichen Fall 2055 und im mittleren Fall 2093', 'im zuversichtlichen Fall 2056 und im mittleren Fall 2095', 1),
 ('ab 2030 um gut 8,3 Punkte', 'ab 2030 um rund 8,7 Punkte', 1),
 ('im vorsichtigen Fall aus Anhang C9 ab 2030 gut 8,3 Punkte', 'im vorsichtigen Fall aus Anhang C9 ab 2030 rund 8,7 Punkte', 1),
 ('fehlen im ersten Jahr rund 54 Mrd.', 'fehlen im ersten Jahr rund 57 Mrd.', 4),
 ('im zweiten rund 62 Mrd.', 'im zweiten rund 65 Mrd.', 3),
 ('im dritten rund 55 Mrd.', 'im dritten rund 52 Mrd.', 2),
 ('2070 rund 37 Mrd.', '2070 rund 35 Mrd.', 1),
 ('2070 von rund 37 Mrd.', '2070 von rund 35 Mrd.', 1),
 ('Nur für den Teil der Ausgaben über 5.000 € im Monat je Erwachsenem gehen von 100 € 75 € an die Steuer.',
  'Nur für den Teil der Ausgaben über 5.000 € im Monat je Erwachsenem (Einkauf ohne Steuer, samt Steuer 8.800 €, je Kind 600 € mehr) gehen von 100 € 75 € an die Steuer.', 1),
]:
    rep(a, b, n)
open(P, 'w', encoding='utf-8').write(s); print('ok')
