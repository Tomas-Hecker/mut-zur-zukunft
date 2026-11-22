#!/usr/bin/env python3
"""Regel von Tomas (22.11.2026): Prozente ohne Nachkommastellen, ganz gerundet, außer bei festen Gesetzes- und Regelwerten
(Sätze, Schuldenbremse, Werte im Register). Dazu der Bürgerjob mit 18 Stunden zum Mindestlohn von 16,84 € (1.314 € im Monat).
Läuft nach eu-start-v41.py. Ein zweiter Lauf ändert nichts."""
p = 'steuerrechner/index.html'
s = open(p, encoding='utf-8').read()
if 'Prozente ganz (22.11.2026)' in s:
    raise SystemExit
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)
rep('const pct = (x, d = 1) => fmt(x * 100, d) + " %";', 'const pct = (x, d = 0) => fmt(x * 100, d) + " %";   // Prozente ganz (22.11.2026): ohne Nachkommastellen, feste Regelwerte geben d an')
rep('(s0 >= 0 ? `${pct(s0 / A.BIP, 2)} des BIP; Überschuss vom ersten Jahr an.` : `${pct(s0 / A.BIP, 2)} des BIP; negativ heißt Lücke.`)',
    '(s0 >= 0 ? `${pct(s0 / A.BIP)} des BIP; Überschuss vom ersten Jahr an.` : `${pct(s0 / A.BIP)} des BIP; negativ heißt Lücke.`)')
rep('`${pct(-s0 / A.BIP, 2)} des BIP; passt in die Schuldenbremse', '`${pct(-s0 / A.BIP)} des BIP; passt in die Schuldenbremse')
rep('`${pct(sL4 / A.BIP, 1)} des BIP, nach', '`${pct(sL4 / A.BIP)} des BIP, nach')
rep('(17 Stunden in der Woche, 1.400 € im Monat, gibt alles aus)', '(18 Stunden in der Woche zum Mindestlohn, 1.314 € im Monat, gibt alles aus)')
rep('pct(r.anteil, 1)', 'pct(r.anteil)', 3)   # Anteil des Staates am Haus
open(p, 'w', encoding='utf-8').write(s)
print('Prozente ganz eingebaut')
