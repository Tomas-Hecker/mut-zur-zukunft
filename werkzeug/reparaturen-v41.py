#!/usr/bin/env python3
"""Buch 28.11.2026 12:50 UTC: Dienste vor Ort mit 5 % nur für Reparaturen an Kleidung, Schuhen, Haushaltsgeräten
und Fahrrädern; Auto, Handy und Computer 50 % (Anhang III Nr. 10, 19, 25 MwSt-Richtlinie). Nur Text."""
P = 'steuerrechner/index.html'
s = open(P, encoding='utf-8').read()
a = 'Dienste vor Ort mit 5 % statt 50 % Mehrwertsteuer: Friseur, Reparaturen, Renovierung, Reinigung, Haushaltshilfe und Betreuung zu Hause.'
b = ('Dienste vor Ort mit 5 % statt 50 % Mehrwertsteuer: Friseur, Reparaturen an Kleidung, Schuhen, Haushaltsgeräten und Fahrrädern, '
     'Renovierung, Reinigung, Haushaltshilfe und Betreuung zu Hause. Reparaturen an Auto, Handy und Computer tragen 50 %, '
     'weil die EU sie nicht ermäßigen lässt (Anhang III Nr. 10, 19 und 25 der Mehrwertsteuer-Richtlinie).')
if b not in s:
    assert s.count(a) == 1; s = s.replace(a, b)
open(P, 'w', encoding='utf-8').write(s); print('ok')
