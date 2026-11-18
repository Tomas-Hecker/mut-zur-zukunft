#!/usr/bin/env python3
"""Steuerrechner: Haushalt mit und ohne Reform bis 2070 und auf die Lebenszeit (Entwurf, 18.11.2026).
Ersetzt den Abschnitt „Auf 30 Jahre gerechnet“: Vergleich mit dem Weg ohne Reform, wahlweise mit Demografieschulden
(Anteil des Haushalts an den Kosten des Alterns, drei Viertel über Beiträge, ein Viertel über Steuern), mit Reform
Wachstum, Freibetrag, Energie und Auslaufen der Übergangsregeln je Jahr; Fall ungünstig / wahrscheinlich / günstig,
Alter für die Lebenszeit, Vermögen aus der Sparquote mit und ohne Abgeltungsteuer.
Grundlage wie im Buch: broschuere-mut-zur-zukunft/version-41/vergleich-ohne-reform/grundlage-vergleich-ohne-reform.json,
Jahrespfad rechenmodell-mikrosim/v0.4/paket-a-jahrespfad/verlauf-jahre-paket9A-v41*.json.
Läuft nach annahmen-regler.py. Ein zweiter Lauf ändert nichts."""
import os
p = 'steuerrechner/index.html'
s = open(p, encoding='utf-8').read()
if 'function vglZeigen()' in s:
    raise SystemExit
JS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vergleich-ohne-reform.js'), encoding='utf-8').read()
a = 'setForm(BEISPIELE[DEFAULT_BEISPIEL].v);'
assert s.count(a) == 1
s = s.replace(a, JS.strip('\n') + '\n' + a)
open(p, 'w', encoding='utf-8').write(s)
