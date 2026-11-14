# Mikrosimulation: Annahmen und Quellen (Entwurf 0.1, 14.11.2026)

Das Modell rechnet rund 49.000 künstliche Haushalte. Sie stehen mit Gewichten für die 41,25 Mio. Haushalte in Deutschland.
Jeder Haushalt wird mit dem **Rechenkern des Steuerrechners** gerechnet, also nach denselben Regeln wie die Beispielhaushalte im
Buch (`kern.js` wird automatisch aus `steuerrechner/index.html` gezogen; Facharbeiter +594 €, Familie +1.119 € im Monat wie in Version 31).
Neu sind Vermögen, Erbschaften und Verhalten. „Vollständig“ kann ein Modell das heutige Verhalten nicht abbilden. Deshalb steht hier jede
Annahme mit ihrer Herkunft, und die unsicheren lassen sich auf der Seite einstellen.

Art der Werte: **Statistik** (amtliche Zahl), **Studie** (Fachliteratur), **Eichpunkt** (Schätzung aus dem Projekt), **Annahme** (eigene, einstellbar).

## 1. Bevölkerung (bevoelkerung.py)

| Was | Wert | Art | Quelle |
|---|---|---|---|
| Haushalte | 41,25 Mio. | Eichpunkt | Vermögenstabelle „heute“ (version-31/aufkommen/vermoegen-heute.json); Mikrozensus 2025: 41,1 Mio. |
| Haushaltstypen | allein 17,9 Mio. (davon 65+ 6,3), Paare 20,0 Mio. (davon 65+ 4,9), Alleinerziehende 2,5 Mio. | Statistik, vereinfacht | Mikrozensus 2024/25 |
| Erwachsene Kinder und Verwandte mit eigenem Einkommen | 4,0 Mio. eigene Steuerfälle | Annahme | Rest bis zu den Erwachsenen |
| Erwachsene zusammen | 65,6 Mio. (amtlich 69,6) | Abweichung | Menschen in Heimen und Teile der erwachsenen Kinder fehlen |
| Löhne in Vollzeit | Median 3.950 € im Monat, Streuung 0,40, obere 5 % Pareto ab 100.000 € | Statistik/Annahme | Entgeltstatistik der BA; Rechenmodell Blatt SV-Freibetrag |
| Löhne in Teilzeit | Median 1.650 € im Monat | Statistik | wie oben |
| Gewinne Selbständiger | Median 45.000 €, Streuung 0,95; KV 40 % privat, sonst rund 20 % freiwillig gesetzlich | Annahme | Summe der Gewinne 271 Mrd. € |
| Beamte und Pensionäre | Besoldung Median 4.200 €, Pension Median 3.400 € | Annahme | Summe 170 Mrd. € (Beihilfe 22,6 Mrd. = 13 %) |
| Renten | Rentnerinnen allein Median 1.550 €, Rentner 1.800 €, Paare 1.850 + 1.100 €, dazu Betriebs- und Zusatzrenten bei der Hälfte | Statistik, gerundet | Alterssicherungsbericht 2024; Summe 355 Mrd. € |
| Bürgergeld | Regelbedarf plus Miete und Heizung | Recht | Summe 41 Mrd. € |
| Andere Leistungen in Geld (Arbeitslosen-, Kranken-, Elterngeld, BAföG) | 54 Mrd. € | Annahme | für die Haushalte neutral gerechnet (die Reform müsste sie anpassen) |

**Abgleich:** Lohn- und Einkommensteuer samt Soli nach heutigem Recht 397–402 Mrd. € (Steuerschätzung 2025: Lohnsteuer vor Kindergeld
316,8 + veranlagte 79,4 + Soli 13 ≈ 409). Bestandsschutz der Rentner 50–54 Mrd. € für 7,3–7,6 Mio. Haushalte (Version 31: 78,4 für 8,73 Mio.).

## 2. Vermögen

| Was | Wert | Art | Quelle |
|---|---|---|---|
| Haushalte und Vermögen je Stufe | 8 Stufen von unter 100.000 € bis über 100 Mio. €, zusammen 16,6 Bio. € | Eichpunkt | vermoegen-heute.json (PHF 2023: Median 103.200 €, P90 777.200 €, plus Reichenzuschätzung) |
| Zusammensetzung je Stufe | eigenes Heim, andere Immobilien, Geld und Wertpapiere, Betriebe | Eichpunkt | SVR 2025 |
| Wer welches Vermögen hat | Rang aus Einkommen (0,6), Alter (0,55), Selbständigkeit (0,3) und Zufall | Annahme | geeicht auf PHF: Median 55–74 Jahre rund 140.000 € (Modell: Rentner 138.500 €) |
| Eigentümer | 6 % bis 95 % je Stufe, zusammen 42 % | Statistik | Mikrozensus 2022: 41,9 % |
| Bezahlter Teil des eigenen Hauses | Rentner 90–100 %, Erwerbstätige im Mittel rund 70 % | Annahme | wie Rechenmodell (HausFrei) |
| Mietwert | 3,2 % des Hauswerts, zusammen 214,5 Mrd. € | Statistik | Eurostat, wie Version 31 |
| Ausgezahlte Zinsen und Dividenden | 1,0 % (kleine Vermögen) bis 3,0 % (ab 1 Mio. €) des Geldvermögens | Annahme | Bundesbank: kleine Vermögen liegen auf Konten und in Versicherungen |
| Mieten | 3,5 % netto, davon 35 % steuerpflichtig (Abschreibung, Zinsen) | Annahme | Eichpunkt; Einkommensteuerstatistik |
| Betriebe ab 1 Mio. € Vermögen | 7 % Gewinn, die Hälfte ausgeschüttet, der Rest bleibt in der GmbH (Körperschaftsteuer) | Eichpunkt/Annahme | |

## 3. Konsum und Sparen

| Was | Wert | Art | Quelle |
|---|---|---|---|
| Eichung | Sparquote 10,4 % des verfügbaren Einkommens, oder wahlweise Konsum genau 2.085,7 Mrd. € (2.300,2 − 214,5 Mietwert, wie Version 31) | Statistik | VGR 2025 |
| Sparquote nach Einkommen | rund 7 Punkte mehr je Verdopplung des Einkommens: + 0,10 × ln(Einkommen/30.000), über 100.000 € zusätzlich + 0,08 × ln(Einkommen/100.000) | Studie | EVS 2018: unten Entsparen, oben 20–40 % |
| Kapitalerträge | nach Steuer zur Hälfte ausgegeben (ab 1 Mio. € zu einem Viertel), der Rest wieder angelegt | Studie | Baker, Nagel, Wurgler 2007; Di Maggio, Kermani, Majlesi 2020 |
| Verzehr von Erspartem im Alter | 1 % (65 Jahre) bis 3,5 % (90 Jahre) des Geldvermögens | Annahme | PHF: Ältere entsparen langsam |

**Wichtige Abweichung:** Mit den Einkommen der künstlichen Haushalte und der amtlichen Sparquote ergibt sich ein Konsum von rund
1.910 Mrd. € ohne Mietwert, 8 % weniger als die 2.086 Mrd. €, auf denen Version 31 die Ausgabensteuer rechnet. Entweder fehlen den
künstlichen Haushalten Einkommen (Umfragen erfassen Einkommen aus Vermögen nur teilweise), oder die Grundlage von Version 31 ist zu
hoch. Das ist zu klären, bevor Zahlen ins Buch gehen. Auf der Seite lässt sich beides wählen.

## 4. Verhalten (alle einstellbar)

| Was | Standard | Art | Quelle |
|---|---|---|---|
| Plus sofort ausgegeben | im Mittel 50 % (Version 32), gestaffelt von 75 % (unter 100.000 €) bis 10 % (über 100 Mio. €); Grundsicherung 100 % | Studie/Annahme | Jappelli, Pistaferri 2014 (Mittel 0,48); Fagereng, Holm, Natvik 2021 (rund 0,5 im ersten Jahr, sinkt mit dem Vermögen) |
| Minus sofort am Einkauf gekürzt | unter 100.000 € 100 %, bis 200.000 € 80 %, bis 400.000 € 50 %, darüber 25 % (Version 32) | Annahme | Christelis u. a. 2019: Verluste wirken stärker bei wenig Puffer |
| Minus nach und nach gekürzt | ganz (Dauerzustand) | Annahme | |
| Vom Angelegten vererbt | 5 % bis 85 % nach Vermögen, Rentner + 15 Punkte | Annahme | De Nardi 2004: Vermögende vererben den Großteil |
| Variante „Reiche kürzen nicht“ | Kürzung 0 %, Minus fehlt ganz am Erbe | Annahme | Wunsch Tomas, 14.11. |

Steuer aus einem zusätzlich ausgegebenen Euro: über dem Freibetrag rund 60 Cent (50 Cent Ausgabensteuer und 10 Cent Mehrwertsteuer),
darunter rund 20 Cent Mehrwertsteuer. Vererbtes bringt den Staatsanteil nur, soweit der Nachlass über dem Familienfreibetrag liegt,
und nur zur Hälfte fällig (langfristig, wie Version 31).

## 5. Erbschaften

| Was | Wert | Art | Quelle |
|---|---|---|---|
| Sterblichkeit | 0,95 % mit 65, + 10,5 % je Jahr (Gompertz); Paare erst beim zweiten Tod (0,6 × Rate mit Alter + 6) | Statistik/Annahme | Rechenmodell RTSteig, Sterbetafel 2023/25 |
| Schenkungen | 0,9 % im Jahr vom Vermögen über 500.000 € | Annahme | |
| Erbschaftsteuer heute | Steuerklasse I, 400.000 € je Kind, 7–30 %, Betriebe zu 85 % verschont, Immobilien zu drei Vierteln bewertet; Schenkungen rund 4 % | Recht/Annahme | ErbStG |
| Staatsanteil | 50 % über dem Familienfreibetrag (400.000 €, + 25 % je weiterem Kind), Kinderlose 40.000 € | Vorschlag | Version 31 |

**Abgleich:** Nachlässe und Schenkungen rund 320 Mrd. € (DIW: 300–400), Erbschaftsteuer heute rund 20 Mrd. € (Statistik 14,9; festgesetzt 2025 21,4).

## 6. Was fehlt noch

- Arbeitsangebot: ob Menschen mehr oder weniger arbeiten.
- Preise und Firmen: wer die höhere Mehrwertsteuer am Ende trägt, wohin die Gewinnsteuern der Firmen wirken.
- Jahre bis 2070: Die Mikrosimulation rechnet ein Jahr (Start) und einen Dauerzustand, keine Jahresreihe.
- Gewerbesteuer und der Teil der Gewinnsteuern, der ausländische Eigentümer trifft, sind nicht den Haushalten zugeordnet.
