"""Baut steuerlast/index.html aus den Grafiken in bilder/steuerlast/ (Schnitt: Projektordner, Skript stl/schnitt.py)."""
import re
R = '/home/user/mut-zur-zukunft/'
import json
M = '/mnt/project-files/rechenmodell-mikrosim/v0.3/'
J = json.load(open(M + 'steuerlast.json'))
UB = json.load(open(M + 'uebergabe-v36.json'))   # Paket 6 (uebergabe-v35.json ist der Stand ohne Paket)
def k(x, n=1):
    t = f"{abs(x):,.{n}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if x < 0 else "") + t
def sk(x, n=1): return ("+" if x > 0 else "") + k(x, n)
Z = J['zehntel']; ein = {a['art'] if 'art' in a else a['name']: a for a in J['arten']['einkommen']}
def diff(name, lang=False, liste='einkommen'):
    a = next(a for a in J['arten'][liste] if a['name'] == name)
    return a['reform_lang_mrd' if lang else 'reform_mrd'] - a['heute_mrd']
E, MS = J['erwachsene'], J['menschen']
SG = UB['spanne_gewaehlt']
assert SG['punktwert']['von_100'] == E['von_100']['mehr'], ('Spanne passt nicht zu steuerlast.json', SG['punktwert'], E['von_100'])
N = dict(
 emehr=str(E['von_100']['mehr']), eweniger=str(E['weniger_zusammen']), mmehr=str(MS['von_100']['mehr']), erw=k(E['erwachsene_mio'], 1), mensch=k(MS['menschen_mio'], 1),
 sw1=k(SG['gewaehlt']['erwachsene_weniger_mio_von_bis'][0]), sw2=k(SG['gewaehlt']['erwachsene_weniger_mio_von_bis'][1]), swr=k(SG['rand']['erwachsene_weniger_mio_hoechstens']), satzb=SG['satz_buch'],
 weniger=k(E['mit_weniger_mio']), wmittel=k(E['weniger_im_mittel_monat'], 0),
 z1h=k(Z[0]['quote_heute']), z1r=k(Z[0]['quote_reform']), z10h=k(Z[9]['quote_heute']), z10r=k(Z[9]['quote_reform']),
 uh=k(sum(z['anteil_heute'] for z in Z[:5])), ur=k(sum(z['anteil_reform'] for z in Z[:5])),
 oh=k(Z[9]['anteil_heute']), orr=k(Z[9]['anteil_reform']),
 gh=k(J['gesamt']['heute_mrd'], 0), gr=k(J['gesamt']['reform_mrd'], 0),
 p1h=k(J['oberstes_prozent']['anteil_heute']), p1r=k(J['oberstes_prozent']['anteil_reform']), p1l=k(J['oberstes_prozent']['anteil_reform_lang']),
 lohn=k(abs(diff('Löhne und Gehälter'))), lohnw='mehr' if diff('Löhne und Gehälter') > 0 else 'weniger', gew=k(diff('Gewinne eigener Firmen')),
 firm=k(diff('Firmen', liste='erbe')), firml=k(diff('Firmen', True, 'erbe')),
 summe=k(abs(J['gesamt']['heute_mrd'] - J['gesamt']['reform_mrd']), 0), summew='weniger' if J['gesamt']['heute_mrd'] > J['gesamt']['reform_mrd'] else 'mehr', ausgl=k(J["ausgleich_mrd"], 1),
 wh=k(J['aufbau'][0]['wachstum_heute']), wr=k(J['aufbau'][0]['wachstum_reform']),
 sh=k(J['aufbau'][0]['sparen_heute_monat'], 0), sr=k(J['aufbau'][0]['sparen_reform_monat'], 0),
 qh=k(J['aufbau'][0]['sparquote_heute']), qr=k(J['aufbau'][0]['sparquote_reform']),
 sq=k(J['aufbau'][0]['sparquote_reform']), vm=k(J['aufbau'][0]['vermoegen_mittel'], 0), vp=k(J['vermoegen'][0]['quote_heute'] - J['vermoegen'][0]['quote_reform']),
)
print(J['stand'], N)
u = open(R + 'ueber-mich.html').read()
header = re.search(r'<header class="top">.*?</header>', u, re.S).group(0)
header = header.replace(' aria-current="page"', '')
header = re.sub(r'href="(?!https?:|mailto:|#)([^"]*)"', lambda m: 'href="../' + (m.group(1) if m.group(1) != './' else '') + '"', header)
footer = re.search(r'<footer>.*?</footer>', u, re.S).group(0).replace('href="', 'href="../')

G = [
 ("steuerlast-feld-einkommen-vermoegen", 1688, 1362, "Wer hat mehr Geld, wer weniger",
  "Farbfeld nach Einkommen und Vermögen: Mehr Geld haben vor allem die unteren Einkommen mit wenig Vermögen, bei mittleren Einkommen ändert sich im Mittel wenig, weniger haben vor allem Haushalte mit mehr als 310.000 € Vermögen und das oberste Zehntel der Einkommen.",
  "Jedes Feld ist eine Gruppe von Erwachsenen, geordnet nach Einkommen und Vermögen ihres Haushalts. Nach rechts steigt das Einkommen, nach unten das Vermögen. Grün heißt: Die Erwachsenen der Gruppe haben im Mittel mehr Geld als heute, in Prozent ihres Einkommens. Rot heißt: weniger. Mehr Geld haben vor allem die unteren drei Zehntel der Einkommen mit wenig Vermögen. Bei mittleren Einkommen haben rund 6 von 10 mehr, im Mittel ändert sich wenig. Weniger haben vor allem Erwachsene in Haushalten mit mehr als 310.000 € Vermögen und im obersten Zehntel der Einkommen. In jedem Feld haben einzelne mehr und andere weniger. Schraffierte Felder: zu wenige Fälle für eine Aussage."),
 ("steuerlast-nach-einkommen", 1688, 982, "Wie viel vom Einkommen an Steuern und Abgaben geht",
  "Punktgrafik nach Einkommenszehnteln: Das unterste Zehntel zahlt «z1r» statt «z1h» % seines Einkommens, das oberste «z10r» statt «z10h» %.",
  "Zehn gleich große Gruppen von je 4,1 Mio. Haushalten, geordnet nach dem Einkommen vor Steuern (Löhne, Gewinne, Renten, Kapitalerträge, Grundsicherung). Die Zahl hinter der Gruppe ist ihr mittleres Einkommen im Monat, die Punkte zeigen den Durchschnitt der Gruppe. Das unterste Zehntel zahlt «z1r» statt «z1h» % seines Einkommens, das oberste «z10r» statt «z10h» %. „Mit weniger“ zählt die Erwachsenen der Gruppe, die trotzdem weniger haben als heute (bei gleichem Einkauf, ohne Erbe)."),
 ("steuerlast-anteile", 1688, 722, "Wie viel vom Ganzen jede Gruppe trägt",
  "Balken: Das oberste Zehntel trägt «orr» statt «oh» % aller Steuern und Abgaben der Haushalte, die untere Hälfte «ur» statt «uh» %.",
  "Alle Haushalte zahlen mit der Reform «gr» Mrd. € im Jahr, heute «gh» Mrd. €. Das oberste Zehntel trägt mehr vom Ganzen als heute, «orr» statt «oh» %. Das oberste Prozent trägt im ersten Jahr «p1r» statt «p1h» %. Es spart viel und zahlt vor allem über das Erbe; wenn das Erbe voll wirkt, trägt es «p1l» %."),
 ("steuerlast-nach-vermoegen", 1688, 702, "Wie viel vom Einkommen nach Vermögen geht",
  "Punktgrafik nach Vermögen: Haushalte unter 100.000 € Vermögen zahlen «vp» Punkte weniger von ihrem Einkommen, Haushalte mit mehr Vermögen mehr, am meisten zwischen 400.000 € und 1 Mio. €.",
  "Gruppen nach Nettovermögen. Mehr zahlen vor allem Haushalte, die viel ausgeben, ohne dafür zu arbeiten: Wer Zinsen, Dividenden oder Mieten ausgibt, zahlt darauf wie auf Lohn. Ausgaben aus versteuertem Ersparten bleiben frei. Wer im eigenen Haus wohnt, zahlt nur für den Teil, der beim Start noch nicht bezahlt ist, auf den Mietwert wie auf eine Miete; Tilgung und Zinsen für den Kredit bleiben steuerfrei. Wer sein Haus noch abzahlt, hat zum Start mindestens so oft mehr Geld wie Mieter. Mit bezahltem Haus hat mehr als die Hälfte weniger. Das liegt nicht am Haus, das bleibt frei, sondern daran, wer dort wohnt: Von denen mit weniger sind mehr als 8 von 10 im Ruhestand oder haben ein Vermögen ab 400.000 €. Bei gleichem Vermögen und gleicher Lage steht man mit bezahltem Haus gleich gut oder besser da als zur Miete."),
 ("wer-bezahlt-einkommen-vermoegen", 1688, 1122, "Welche Einkommen und Vermögen die Reform bezahlen",
  "Balken nach Einkommens- und Vermögensart: Auf Löhne fallen «lohn» Mrd. € «lohnw», auf Gewinne eigener Firmen «gew» Mrd. € mehr, auf vererbte Firmen «firm» Mrd. € mehr.",
  "Wie viel mehr oder weniger Steuern und Abgaben im Jahr auf jede Art von Einkommen und Vermögen fallen als heute, in Milliarden Euro. Auf Löhne fallen «lohn» Mrd. € «lohnw», auf Gewinne eigener Firmen «gew» Mrd. € mehr. Beim Erbe zahlen Firmen «firm» Mrd. € mehr, «firml» Mrd. €, wenn der Staatsanteil am Erbe voll wirkt: Heute sind vererbte Firmen zu 85 % verschont, mit der Reform zählt alles voll. Zusammen tragen die Haushalte «summe» Mrd. € «summew» als heute. Darin sind «ausgl» Mrd. € Zuschlag für heutige Rentner: Ihre Rente kauft 4 % mehr. Steuern von Firmen, die nicht den Haushalten gehören, sind nicht enthalten."),
 ("vermoegen-sparen", 1688, 1057, "Wie Vermögen wächst",
  "Punktgrafik zum Sparen nach Vermögen: Haushalte unter 100.000 € Vermögen sparen mit der Reform «sr» € im Monat, heute «sh» €.",
  "Um wie viel Prozent das Vermögen der Haushalte im Jahr durch Sparen wächst. Haushalte mit weniger als 100.000 € Vermögen sparen heute im Mittel «sh» € im Monat, mit der Reform «sr» €, also «sq» % statt «qh» % ihres Einkommens. Sie besitzen im Mittel «vm» €. Gespart wird, was vom Einkommen nach Steuern und Abgaben bleibt, wenn der Haushalt so viel einkauft wie heute; was er mehr hat, legt er in dieser Rechnung ganz zurück. Nicht enthalten: Wertsteigerung von Häusern und Aktien, Erbschaften und Schenkungen."),
]
from PIL import Image
G = [(f, *Image.open(R + 'bilder/steuerlast/' + f + '.webp').size, t, alt, cap) for f, w, h, t, alt, cap in G]
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
<meta name="description" content="Wer mit dem einheitlichen Steuersystem aus „Wir können uns die Zukunft leisten“ mehr Geld hat und wer weniger, nach Einkommen und Vermögen, gerechnet für alle «erw» Mio. Erwachsenen.">
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
<p>Jedes Einkommen nach denselben Regeln: Wer hat mehr Geld als heute, wer weniger? Gerechnet für alle «erw» Mio. Erwachsenen in 41 Mio. Haushalten, nach Einkommen und Vermögen, im ersten Jahr der Reform und bei gleichem Einkauf wie heute.</p>
</div></section>
<div class="wrap sl">
<div class="facts">
<div><b>«emehr» von 100</b><span>Erwachsenen haben mehr Geld als heute, wenn sie so viel einkaufen wie heute. Mit den Kindern gezählt «mmehr» von 100 Menschen.</span></div>
<div><b>«z1h» → «z1r» %</b><span>vom Einkommen zahlt das ärmste Zehntel an Steuern und Abgaben, heute und mit der Reform.</span></div>
<div><b>«oh» → «orr» %</b><span>aller Steuern und Abgaben der Haushalte trägt das reichste Zehntel, heute und mit der Reform.</span></div>
</div>
{figs}
<div class="methode">
<h2>Wie gerechnet wurde</h2>
<p>Rund 46.000 künstliche Haushalte stehen für alle 41 Mio. Haushalte in Deutschland, mit «erw» Mio. Erwachsenen und «mensch» Mio. Menschen. Sie sind auf amtliche Zahlen geeicht: Löhne und Konsum aus der Volkswirtschaftlichen Gesamtrechnung 2025, Lohn- und Einkommensteuer aus den Steuereinnahmen 2025, Vermögen aus der Vermögensbefragung der Bundesbank 2023 mit einer Zuschätzung der Reichsten, Sparen aus der Einkommens- und Verbrauchsstichprobe.</p>
<p>Heute: Lohn- und Einkommensteuer mit Soli, Sozialbeiträge, Abgeltungsteuer, Körperschaftsteuer auf eigene Firmen, Mehrwertsteuer, Erbschaft- und Schenkungsteuer. Mit der Reform: Ausgabensteuer über dem Freibetrag, höhere Mehrwertsteuer auf denselben Einkauf, die verbleibenden Beiträge und der Staatsanteil am Erbe, abzüglich der Auszahlungen an die Haushalte. Das Erbe zählt als erwartete Steuer im Jahr. Wie jede Schätzung hängt das Ergebnis an Annahmen: Gezählt werden Erwachsene über 18: Jeder zählt mit dem Plus seines Haushalts geteilt durch die Erwachsenen darin, erwachsene Kinder bei den Eltern zählen für sich, Kinder unter 18 mit ihrem Haushalt. Im gezeigten Fall haben «emehr» von 100 Erwachsenen mehr Geld. «satzb» Weniger haben im gezeigten Fall «weniger» Mio. Erwachsene, im Mittel «wmittel» € im Monat; mit anderen vertretbaren Annahmen «sw1» bis «sw2» Mio., am Rand höchstens «swr» Mio. Die Grafiken ordnen nach Einkommen und Vermögen des Haushalts und zählen die erwachsenen Kinder bei den Eltern nicht mit. Jeden einzelnen Haushalt rechnet der <a href="../steuerrechner/">Steuerrechner</a> nach, die ganze Rechnung steht im <a href="../buch/">Buch</a>.</p>
</div>
</div>
</main>
{footer}
<script src="../satz.js" defer></script>
</body>
</html>
'''
html = re.sub(r'«(\w+)»', lambda m: N[m.group(1)], html)
assert '«' not in html
open(R + 'steuerlast/index.html', 'w').write(html)
print('ok', len(html))
