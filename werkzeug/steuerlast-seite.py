"""Baut steuerlast/index.html aus den Grafiken in bilder/steuerlast/ (Schnitt: Projektordner, Skript stl/schnitt.py)."""
import re
R = '/home/user/mut-zur-zukunft/'
u = open(R + 'ueber-mich.html').read()
header = re.search(r'<header class="top">.*?</header>', u, re.S).group(0)
header = header.replace(' aria-current="page"', '')
header = re.sub(r'href="(?!https?:|mailto:|#)([^"]*)"', lambda m: 'href="../' + (m.group(1) if m.group(1) != './' else '') + '"', header)
footer = re.search(r'<footer>.*?</footer>', u, re.S).group(0).replace('href="', 'href="../')

G = [
 ("steuerlast-feld-einkommen-vermoegen", 1688, 1362, "Wer hat mehr Geld, wer weniger",
  "Farbfeld nach Einkommen und Vermögen: Bis rund 310.000 € Vermögen haben fast alle Gruppen mehr Geld als heute, zwischen 310.000 und 490.000 € bleibt es fast gleich, darüber haben die Gruppen weniger.",
  "Jedes Feld ist eine Gruppe von Haushalten. Nach rechts steigt das Einkommen, nach unten das Vermögen. Grün heißt: Die Haushalte haben im Mittel mehr Geld als heute, in Prozent ihres Einkommens. Rot heißt: weniger. Bis rund 310.000 € Vermögen ist fast alles grün, zwischen 310.000 und 490.000 € bleibt es fast gleich, weniger haben vor allem Haushalte mit mehr als 490.000 € Vermögen. Auch in grünen Feldern haben einzelne Haushalte weniger. Schraffierte Felder: zu wenige Haushalte für eine Aussage."),
 ("steuerlast-nach-einkommen", 1688, 982, "Wie viel vom Einkommen an Steuern und Abgaben geht",
  "Punktgrafik nach Einkommenszehnteln: Das unterste Zehntel zahlt 7,3 statt 18,1 % seines Einkommens, das oberste 41,6 statt 40,3 %.",
  "Zehn gleich große Gruppen von je 4,1 Mio. Haushalten, geordnet nach dem Einkommen vor Steuern (Löhne, Gewinne, Renten, Kapitalerträge, Grundsicherung). Die Zahl hinter der Gruppe ist ihr mittleres Einkommen im Monat, die Punkte zeigen den Durchschnitt der Gruppe. Das unterste Zehntel zahlt 7,3 statt 18,1 % seines Einkommens, das oberste 41,6 statt 40,3 %. „Mit weniger“ zählt die Haushalte der Gruppe, die trotzdem weniger haben als heute (bei gleichem Einkauf, ohne Erbe)."),
 ("steuerlast-anteile", 1688, 722, "Wie viel vom Ganzen jede Gruppe trägt",
  "Balken: Das oberste Zehntel trägt 40,2 statt 37,8 % aller Steuern und Abgaben der Haushalte, die untere Hälfte 14,1 statt 15,7 %.",
  "Alle Haushalte zahlen mit der Reform 1.063 Mrd. € im Jahr, heute 1.094 Mrd. €. Das oberste Zehntel trägt mehr vom Ganzen als heute, 40,2 statt 37,8 %. Das oberste Prozent trägt 11,9 statt 12,3 %, wenn das Erbe voll wirkt 12,4 %: Es spart viel und zahlt vor allem über das Erbe."),
 ("steuerlast-nach-vermoegen", 1688, 702, "Wie viel vom Einkommen nach Vermögen geht",
  "Punktgrafik nach Vermögen: Haushalte unter 100.000 € Vermögen zahlen 5,3 Punkte weniger von ihrem Einkommen, Haushalte zwischen 400.000 € und 1 Mio. € mehr.",
  "Gruppen nach Nettovermögen. Mehr zahlen vor allem Haushalte mit eigenem Haus, das noch nicht abbezahlt ist: Auf den Mietwert des unbezahlten Teils fällt Ausgabensteuer an, ebenso auf ausgegebene Zinsen und Mieten. Der beim Start bezahlte Teil des Hauses und Ausgaben aus versteuertem Ersparten bleiben frei."),
 ("wer-bezahlt-einkommen-vermoegen", 1688, 1122, "Welche Einkommen und Vermögen die Reform bezahlen",
  "Balken nach Einkommens- und Vermögensart: Auf Löhne fallen 43,3 Mrd. € weniger, auf Gewinne eigener Firmen 15,7 Mrd. € mehr, auf vererbte Firmen 5,7 Mrd. € mehr.",
  "Wie viel mehr oder weniger Steuern und Abgaben im Jahr auf jede Art von Einkommen und Vermögen fallen als heute, in Milliarden Euro. Auf Löhne fallen 43,3 Mrd. € weniger, auf Gewinne eigener Firmen 15,7 Mrd. € mehr. Beim Erbe zahlen Firmen 5,7 Mrd. € mehr, 13,0 Mrd. €, wenn der Staatsanteil am Erbe voll wirkt: Heute sind vererbte Firmen zu 85 % verschont, mit der Reform zählt alles voll. Zusammen tragen die Haushalte 31 Mrd. € weniger als heute, 23 Mrd. € davon ist der Ausgleich für heutige Rentner (bis 300 € im Monat) und 10 € im Monat je Erwachsenem. Steuern von Firmen, die nicht den Haushalten gehören, sind nicht enthalten."),
 ("vermoegen-sparen", 1688, 962, "Wie Vermögen wächst",
  "Punktgrafik zum Sparen: Haushalte unter 100.000 € Vermögen sparen 7,9 % ihres Vermögens im Jahr statt heute minus 3,3 %.",
  "Um wie viel Prozent das Vermögen der Haushalte im Jahr durch Sparen wächst. Haushalte mit weniger als 100.000 € Vermögen bauen heute im Mittel Vermögen ab (−3,3 % im Jahr), mit der Reform wächst es um 7,9 %. Gespart wird, was vom Einkommen nach Steuern und Abgaben bleibt, wenn der Haushalt so viel einkauft wie heute; was er mehr hat, legt er in dieser Rechnung ganz zurück. Nicht enthalten: Wertsteigerung von Häusern und Aktien, Erbschaften und Schenkungen."),
]
figs = "\n".join(f'''<figure id="{f}">
<a href="../bilder/steuerlast/{f}.webp" title="{t}: Grafik groß öffnen"><img src="../bilder/steuerlast/{f}.webp" width="{w}" height="{h}" loading="lazy" alt="{alt}"></a>
<figcaption>{cap}</figcaption>
</figure>''' for f, w, h, t, alt, cap in G)

html = f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Wer die Reform bezahlt · Mut zur Zukunft</title>
<meta name="description" content="Wer mit dem einheitlichen Steuersystem aus „Wir können uns die Zukunft leisten“ mehr Geld hat und wer weniger, nach Einkommen und Vermögen, gerechnet für 41 Mio. Haushalte.">
<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../style.css">
<style>
.sl-hero{{background:var(--brand);color:var(--brand-fg);padding:44px 0 48px}}
.sl-hero h1{{font-size:clamp(2rem,5vw,3rem);margin-bottom:.3em}}
.sl-hero .eyebrow{{color:var(--accent-fill)}}
.sl-hero p{{color:#d6e3da;font-size:1.12rem;max-width:64ch;margin:0}}
.sl{{max-width:900px;padding-top:36px;padding-bottom:56px}}
.sl .facts{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:0 0 12px}}
.sl .facts div{{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:16px}}
.sl .facts b{{display:block;font-family:var(--font-display);font-size:1.6rem;color:#1f5a43;line-height:1.1;margin-bottom:4px}}
.sl .facts span{{color:var(--muted);font-size:.95rem;line-height:1.4;display:block}}
.sl figure{{margin:36px 0 0}}
.sl figure h2{{font-size:clamp(1.3rem,3vw,1.7rem);margin-bottom:.6em}}
.sl figure img{{display:block;width:100%;height:auto;background:#fff;border:1px solid var(--line);border-radius:14px}}
.sl figcaption{{color:var(--muted);font-size:.95rem;margin-top:10px;max-width:72ch}}
.sl .methode{{background:var(--sunk);border-left:4px solid var(--accent-fill);border-radius:var(--r);padding:18px 20px;margin-top:44px}}
.sl .methode h2{{font-size:1.2rem;margin-bottom:.4em}}
.sl .methode p{{margin:0 0 .6em;max-width:72ch}}
@media (max-width:760px){{.sl .facts{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
{header}
<main>
<section class="sl-hero"><div class="wrap">
<p class="eyebrow">Ein einheitliches Steuersystem</p>
<h1>Wer die Reform bezahlt</h1>
<p>Jedes Einkommen nach denselben Regeln: Wer hat mehr Geld als heute, wer weniger? Gerechnet für alle 41 Mio. Haushalte, nach Einkommen und nach Vermögen, im ersten Jahr der Reform und bei gleichem Einkauf wie heute.</p>
</div></section>
<div class="wrap sl">
<div class="facts">
<div><b>73 %</b><span>der Haushalte haben mehr Geld als heute, wenn sie so viel einkaufen wie heute.</span></div>
<div><b>18,1 → 7,3 %</b><span>vom Einkommen zahlt das ärmste Zehntel an Steuern und Abgaben, heute und mit der Reform.</span></div>
<div><b>37,8 → 40,2 %</b><span>aller Steuern und Abgaben der Haushalte trägt das reichste Zehntel, heute und mit der Reform.</span></div>
</div>
{figs}
<div class="methode">
<h2>Wie gerechnet wurde</h2>
<p>Rund 49.000 künstliche Haushalte stehen für alle 41 Mio. Haushalte in Deutschland. Sie sind auf amtliche Zahlen geeicht: Löhne und Konsum aus der Volkswirtschaftlichen Gesamtrechnung 2025, Lohn- und Einkommensteuer aus den Steuereinnahmen 2025, Vermögen aus der Vermögensbefragung der Bundesbank 2023 mit einer Zuschätzung der Reichsten, Sparen aus der Einkommens- und Verbrauchsstichprobe.</p>
<p>Heute: Lohn- und Einkommensteuer mit Soli, Sozialbeiträge, Abgeltungsteuer, Körperschaftsteuer auf eigene Firmen, Mehrwertsteuer, Erbschaft- und Schenkungsteuer. Mit der Reform: Ausgabensteuer über dem Freibetrag, höhere Mehrwertsteuer auf denselben Einkauf, die verbleibenden Beiträge und der Staatsanteil am Erbe, abzüglich der Auszahlungen an die Haushalte. Das Erbe zählt als erwartete Steuer im Jahr. Wie jede Schätzung hängt das Ergebnis an Annahmen: Im gezeigten Fall haben 11,2 Mio. Haushalte weniger als heute, mit anderen vertretbaren Eichungen sind es 9,9 bis 13,3 Mio. Jeden einzelnen Haushalt rechnet der <a href="../steuerrechner/">Steuerrechner</a> nach, die ganze Rechnung steht im <a href="../buch/">Buch</a>.</p>
</div>
</div>
</main>
{footer}
<script src="../satz.js" defer></script>
</body>
</html>
'''
open(R + 'steuerlast/index.html', 'w').write(html)
print('ok', len(html))
