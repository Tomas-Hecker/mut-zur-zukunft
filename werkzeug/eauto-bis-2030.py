#!/usr/bin/env python3
"""Tomas 24.11.2026, 13:55: Die Erstattung der Mehrwertsteuer beim neuen Elektroauto gilt nur für Käufe bis Ende 2030.
E-Auto-Rechner und Steuerrechner (Texte); zweiter Lauf ändert nichts."""
import sys
def patch(p, R, marke):
    s = open(p, encoding='utf-8').read()
    if marke in s: print(p, 'schon drin'); return
    for a, b in R:
        assert s.count(a) == 1, (p, a[:60], s.count(a)); s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s); print(p, 'ok')
patch('eauto-rechner/index.html', [
 ('// MwSt auf die ersten 10.000 € eines neuen E-Autos zurück (bis 5.000 €),', '// MwSt auf die ersten 10.000 € eines neuen E-Autos zurück (bis 5.000 €, nur für Käufe bis Ende 2030),'),
 ('ePreis: Math.max(0, v.ePreis * f - 5000),', 'ePreis: Math.max(0, v.ePreis * f - (v.kaufjahr <= 2030 ? 5000 : 0)),'),
 ('Mehrwertsteuer auf die ersten 10.000 € des E-Autos zurück, Strom', 'Mehrwertsteuer auf die ersten 10.000 € des E-Autos zurück (für Käufe bis Ende 2030), Strom'),
], 'nur für Käufe bis Ende 2030')
patch('steuerrechner/index.html', [
 ('["Neuwagen: Mehrwertsteuer auf die ersten 10.000 € eines Elektroautos erstattet, weniger, je mehr Elektroautos verkauft werden",',
  '["Neuwagen: Mehrwertsteuer auf die ersten 10.000 € eines Elektroautos erstattet, für Käufe bis Ende 2030, weniger, je mehr Elektroautos verkauft werden",'),
 ('Neuwagen: Wer privat ein Elektroauto neu kauft, bekommt die Mehrwertsteuer auf die ersten 10.000 € zurück, also bis zu 5.000 €; für Verbrenner gibt es nichts.',
  'Neuwagen: Wer privat ein Elektroauto bis Ende 2030 neu kauft, bekommt die Mehrwertsteuer auf die ersten 10.000 € zurück, also bis zu 5.000 €; für Verbrenner gibt es nichts, für Käufe ab 2031 auch für Elektroautos nicht mehr.'),
], 'für Käufe bis Ende 2030, weniger')
