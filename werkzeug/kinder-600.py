#!/usr/bin/env python3
"""Freibetrag je Kind 600 € im Monat (von Tomas am 18.11.2026 freigegeben): Ausgleich je Kind (KIDM) 31 statt 20 € im Monat,
also 6.828 € Existenzminimum im Jahr plus 12 × 31 €. Gilt wie bisher auch für die Grundsicherung der Kinder.
Läuft nach kern-v41.py und prognose-v41.py. Ein zweiter Lauf ändert nichts."""
p = 'steuerrechner/index.html'
s = open(p, encoding='utf-8').read()
if 'KIDM: 31,' in s:
    raise SystemExit
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('KIDM: 20, GSKinder: 2.0,   // Version 28: je Kind 20 € im Monat mehr frei (Ausgleich der Mehrwertsteuer), 589 € im Monat',
    'KIDM: 31, GSKinder: 2.0,   // Version 41: je Kind 31 € im Monat mehr frei (Ausgleich der Mehrwertsteuer und Aufrundung), 600 € im Monat')
rep('["KIDM","Ausgleich der höheren Mehrwertsteuer je Kind","Vorschlag","20 € im Monat","Die höhere Mehrwertsteuer verteuert auch den Einkauf für Kinder. Grobe eigene Rechnung: Ein Kind kauft vor allem Lebensmittel (frei), Kleidung und Strom (5 %), dazu Spielzeug, Schulsachen und Möbel (50 %); sein Einkauf wird rund 20 € im Monat teurer. Darum steigt der Freibetrag jedes Kindes um 240 € im Jahr und die Grundsicherung für Kinder um 20 € im Monat, im Gesetz an die Mehrwertsteuer gekoppelt wie bei Erwachsenen.',
    '["KIDM","Zuschlag je Kind über dem Existenzminimum","Vorschlag","31 € im Monat","Die höhere Mehrwertsteuer verteuert auch den Einkauf für Kinder. Grobe eigene Rechnung: Ein Kind kauft vor allem Lebensmittel (frei), Kleidung und Strom (5 %), dazu Spielzeug, Schulsachen und Möbel (50 %); sein Einkauf wird rund 20 € im Monat teurer. Der Vorschlag rundet auf: Für jedes Kind bleiben 600 € im Monat frei, 31 € mehr als das Existenzminimum, und die Grundsicherung für Kinder steigt um 31 € im Monat. Das kostet rund 1,8 Mrd. € im Jahr mehr als ein Zuschlag von 20 €.')
rep('Mit 20 € im Monat mehr (KIDM) kostet ihr Ausgleich für die höhere Mehrwertsteuer zusammen rund 0,5 Mrd. € im Jahr.',
    'Mit 31 € im Monat mehr (KIDM) kostet ihr Zuschlag zusammen rund 0,7 Mrd. € im Jahr.')
rep('dazu 20 € im Monat Ausgleich für die Mehrwertsteuer (KIDM), zusammen 589 € im Monat.', 'dazu 31 € im Monat (KIDM), zusammen 600 € im Monat.')
rep('589 € je Kind', '600 € je Kind', 3)
rep('zusammen 589 € im Monat.",[["Statistisches Bundesamt', 'zusammen 600 € im Monat.",[["Statistisches Bundesamt')
assert '589' not in s.replace('589,', ''), [s[i-60:i+20] for i in range(len(s)) if s.startswith('589', i)][:3]
open(p, 'w', encoding='utf-8').write(s)
print('Freibetrag je Kind 600 €')
