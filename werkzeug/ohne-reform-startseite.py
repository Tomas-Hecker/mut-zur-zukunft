#!/usr/bin/env python3
"""Setzt auf der Startseite das Farbfeld „Mit Reform gegen ohne Reform“ (alle Menschen samt Kindern, mit Energie) mit Jahreswahl ein.
Quelle: broschuere-mut-zur-zukunft/version-41/steuerlast/homepage-ohne-reform/ (Bilder *-energie.png und homepage-feld-ohne-reform.json).
Aufruf: python3 werkzeug/ohne-reform-startseite.py [Quellordner]. Ein zweiter Lauf ändert nichts."""
import json, os, re, sys
from PIL import Image
Q = sys.argv[1] if len(sys.argv) > 1 else '/mnt/project-files/broschuere-mut-zur-zukunft/version-41/steuerlast/homepage-ohne-reform/'
J = json.load(open(Q + 'homepage-feld-ohne-reform.json', encoding='utf-8'))
JAHRE = [(2038, 'nach 10 Jahren'), (2048, 'nach 20 Jahren'), (2058, 'nach 30 Jahren'), (2068, 'nach 40 Jahren'), (2070, '2070')]
STANDARD = 2048
os.makedirs('bilder/ohne-reform', exist_ok=True)
k = lambda x: f"{x:+.1f}".replace('.', ',').replace('-', '−')
alt = {}
for j, _ in JAHRE:
    im = Image.open(f'{Q}homepage-feld-ohne-reform-{j}-energie.png').convert('RGB')
    im.save(f'bilder/ohne-reform/mit-gegen-ohne-reform-{j}.webp', quality=88, method=6)
    m = J[f'energie_{j}']['prozent_des_einkommens']
    alt[j] = (f'Farbfeld nach Einkommen und Vermögen, {j}: Alle Menschen haben mit der Reform im Mittel {k(m[-1][-1])} % ihres Einkommens '
              f'gegen den Weg ohne Reform. Mehr haben vor allem die unteren und mittleren Einkommen, weniger vor allem Menschen in Haushalten '
              f'mit mehr als 300.000 € Vermögen und im obersten Zehntel der Einkommen.')
W, H = im.size
knoepfe = ''.join(f'<button type="button" data-j="{j}" aria-pressed="{"true" if j == STANDARD else "false"}">{t}</button>' for j, t in JAHRE)
fig = (f'<figure class="steuerlast" id="ohne-reform"><div class="or-wahl" role="group" aria-label="Jahr wählen">{knoepfe}</div>'
       f'<img id="or-bild" src="bilder/ohne-reform/mit-gegen-ohne-reform-{STANDARD}.webp" width="{W}" height="{H}" loading="lazy" alt="{alt[STANDARD]}">'
       '<figcaption>Wer mit der Reform mehr Geld hat als ohne sie, im selben Jahr, für alle Menschen samt Kindern nach Einkommen (nach rechts) '
       'und Vermögen ihres Haushalts (nach unten), im mittleren Fall, mit dem wahrscheinlichen Umstieg auf E-Auto, Wärmepumpe und Solarstrom. '
       'Ohne Reform steigen die Kosten des Alterns über Beiträge und Steuern. Weniger haben vor allem Menschen in Haushalten mit mehr als 300.000 € Vermögen '
       'und im obersten Zehntel der Einkommen. <a href="steuerlast/">Gegen heute gerechnet: Wer die Reform bezahlt</a></figcaption></figure>')
js = ('<script>(()=>{const A=' + json.dumps({str(j): alt[j] for j, _ in JAHRE}, ensure_ascii=False) + ',b=document.getElementById("or-bild");'
      'document.querySelectorAll("#ohne-reform .or-wahl button").forEach(k=>k.addEventListener("click",()=>{'
      'document.querySelectorAll("#ohne-reform .or-wahl button").forEach(x=>x.setAttribute("aria-pressed",x===k));'
      'b.src=`bilder/ohne-reform/mit-gegen-ohne-reform-${k.dataset.j}.webp`;b.alt=A[k.dataset.j];}))})();</script>')
css = ('<style id="or-stil">.or-wahl{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}.or-wahl button{font:inherit;font-size:.92rem;padding:6px 12px;'
       'border:1px solid var(--line);border-radius:999px;background:var(--surface,#fff);color:inherit;cursor:pointer}'
       '.or-wahl button[aria-pressed="true"]{background:var(--brand,#12372A);color:#fff;border-color:transparent}</style>')
p = 'index.html'; s = open(p, encoding='utf-8').read()
s = re.sub(r'\n*<style id="or-stil">.*?</style>', '', s, flags=re.S)
s = re.sub(r'\n*<script>\(\(\)=>\{const A=.*?</script>', '', s, flags=re.S)
s, n = re.subn(r'<figure class="steuerlast"[^>]*>.*?</figure>', lambda m: fig, s, count=1, flags=re.S); assert n == 1
s = s.replace('</head>', css + '\n</head>', 1)
s = s.replace('</body>', js + '\n</body>', 1)
open(p, 'w', encoding='utf-8').write(s)
print('Farbfeld ohne Reform eingesetzt')
