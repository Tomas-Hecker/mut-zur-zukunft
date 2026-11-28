#!/usr/bin/env python3
"""Tomas 28.11.2026: Erstattung beim neuen Elektroauto läuft nach Plan aus, 5.000 € bis zu Käufen 2030,
dann jedes Jahr 1.000 € weniger, ab 2035 nichts mehr. Nur Texte; die Beträge (AutoStufeS, AutoStufeL)
kommen mit dem nächsten Lauf der Mikrosimulation."""
import sys
P = 'steuerrechner/index.html'
s = open(P, encoding='utf-8').read()
if 'ab 2035 nichts mehr' in s:
    print('schon drin'); sys.exit()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a)); s = s.replace(a, b)
rep('["Neuwagen: Mehrwertsteuer auf die ersten 10.000 € eines Elektroautos erstattet, weniger, je mehr Elektroautos verkauft werden",',
    '["Neuwagen: bis 5.000 € zurück für ein Elektroauto, gekauft bis 2030, danach jedes Jahr 1.000 € weniger, ab 2035 nichts mehr",')
rep('Die Erstattung sinkt in Stufen, je mehr der neuen Autos elektrisch sind, und entfällt ab 80 % (AutoStufeS, AutoStufeL).',
    'Die Erstattung läuft nach festem Plan aus: bis 5.000 € für Käufe bis 2030, danach jedes Jahr 1.000 € weniger, ab 2035 nichts mehr (AutoStufeS, AutoStufeL).')
rep('"Die Erstattung beim Kauf eines neuen Elektroautos sinkt in Stufen, je nachdem, wie viele der neuen Autos im Vorjahr rein elektrisch waren: unter 40 % bis 5.000 €, 40 bis unter 50 % bis 3.750 €, 50 bis unter 65 % bis 2.500 €, 65 bis unter 80 % bis 1.250 €, ab 80 % nichts mehr (Mehrwertsteuer auf die ersten 10.000, 7.500, 5.000, 2.500 und 0 € des Preises). Eine neue Stufe gilt ab dem 1. Juli des folgenden Jahres, und die Erstattung steigt nie wieder, auch wenn der Anteil kurz sinkt.',
    '"Die Erstattung beim Kauf eines neuen Elektroautos läuft nach festem Plan aus: bis 5.000 € für Käufe bis 2030, 2031 bis 4.000 €, 2032 bis 3.000 €, 2033 bis 2.000 €, 2034 bis 1.000 €, ab 2035 nichts mehr (Mehrwertsteuer auf die ersten 10.000, 8.000, 6.000, 4.000 und 2.000 € des Preises). Jeder kennt den Plan im Voraus, und er hängt nicht davon ab, wie viele Elektroautos verkauft werden.')
rep('"Ab 80 % Elektroautos unter den neuen Autos im Vorjahr entfällt die Erstattung ganz;', '"Ab 2035 entfällt die Erstattung ganz;')
rep('das Darlehen für das Auto endet ab 80 %;', 'das Darlehen für das Auto endet ab 2035;')
rep('Annahme: Am Start gilt die Stufe 40 bis unter 50 %, drei Viertel der Erstattung, 3,7 statt 4,9 Mrd. € im Jahr.',
    'Annahme bis zum nächsten Lauf der Mikrosimulation: am Start drei Viertel der Erstattung, 3,7 statt 4,9 Mrd. € im Jahr.')
open(P, 'w', encoding='utf-8').write(s); print('ok')
