#!/usr/bin/env python3
"""Ersetzt die Anhang-Seiten im Online-Buch durch einen Hinweis, solange die Anhänge auf Version 41 neu gerechnet werden
(Entscheidung Tomas 18.11.2026: Verweise auf Anhänge zeigen bis dahin einen Hinweis, keine alten Anhänge online).
Alle bisherigen Anker der Seite (a1, b5, anh-A1, Überschriften …) bleiben als leere Ziele erhalten, damit jeder Link trifft.
Aufruf VOR buch-bauen.py: python3 werkzeug/anhang-platzhalter.py buch   Ein zweiter Lauf ändert nichts."""
import glob, json, os, re, sys
ORD = sys.argv[1]
st = json.load(open(os.path.join(ORD, 'stellen.json'), encoding='utf-8')) if os.path.exists(os.path.join(ORD, 'stellen.json')) else {}
NAMEN = {'a': 'das Steuersystem', 'b': 'die Bausteine', 'c': 'die Simulation', 'd': 'Recht und Verfassung'}
for p in sorted(glob.glob(os.path.join(ORD, 'anhang-*.html'))):
    nm = os.path.basename(p); b = nm[7]
    s = open(p, encoding='utf-8').read()
    if 'anhang-hinweis' in s:
        continue
    ids = [i for i in dict.fromkeys(re.findall(r' id="([^"]+)"', s[s.index('<main'):s.index('</main>')]))]
    ids += [k for k, v in st.items() if v.split('#')[0] == nm and k not in ids]
    titel = re.search(r'<h1>(.*?)</h1>', s).group(1)
    anker = ''.join(f'<span id="{i}"></span>' for i in ids)
    main = (f'<main class="bmain">{anker}<div class="bhero"><div class="bwrap"><div class="bnum">{b.upper()}</div><div><p class="eyebrow">Anhang {b.upper()}</p>'
            f'<h1>{titel}</h1></div></div></div><article class="bwrap anhang-hinweis" style="display:block;padding:2rem clamp(16px,4vw,48px)">'
            '<p style="font-size:1.2rem;font-weight:600">Dieser Anhang wird gerade mit den neuen Zahlen des Buchs neu gerechnet. Bis dahin steht er hier nicht, '
            'damit keine alten Zahlen neben dem neuen Text stehen.</p>'
            '<p>Jede Rechnung lässt sich schon jetzt nachprüfen: Der <a href="../steuerrechner/">Steuerrechner</a> rechnet mit denselben Annahmen wie das Buch, '
            'für deinen Haushalt und für den Staat bis 2070, und zeigt bei jeder Annahme die Quelle. '
            '<a href="./">Zum Inhaltsverzeichnis</a></p></article></main>')
    s = s[:s.index('<main')] + main + s[s.index('</main>') + 7:]
    open(p, 'w', encoding='utf-8').write(s)
    print(nm, len(ids), 'Anker als Hinweis')

# Quellen: bleiben stehen, mit einem Hinweis, bis die neue Liste mit den Anhängen kommt
p = os.path.join(sys.argv[1], 'quellen.html')
if os.path.exists(p):
    s = open(p, encoding='utf-8').read()
    if 'quellen-hinweis' not in s:
        a = '<article class="btext">'
        assert s.count(a) == 1
        s = s.replace(a, a + '<p class="quellen-hinweis" style="font-weight:600">Diese Liste ist vom 15.11. und wird mit den Anhängen gerade auf den neuen Stand gebracht. '
                      'Einige Hinweise auf Anhänge und Bausteine beziehen sich noch auf die alte Fassung.</p>')
        open(p, 'w', encoding='utf-8').write(s)
        print('quellen.html mit Hinweis')
