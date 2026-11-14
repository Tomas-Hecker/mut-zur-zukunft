# Mikrosimulation: Annahmen und Quellen (Entwurf 0.2, 14.11.2026, geeicht an VGR 2025, Kassenstatistik 2025 und EVS)

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
| Minijobs als Nebenjob | 3,3 Mio. Beschäftigte (im Modell 2,5 Mio. Haushalte) | Statistik | Minijob-Zentrale, Quartalsbericht 2025 |
| **Eichung der Löhne** | alle Löhne und Besoldungen × 1,11, so dass die Summe 2.036,3 Mrd. € ergibt | Statistik | VGR 2025, Bruttolöhne und -gehälter (Destatis, Fachserie 18 Reihe 1.4, Tabelle 2.1.8). Der Faktor deckt Sonderzahlungen, den Lohnstand 2025 und Löhne, die Umfragen untererfassen |
| **Abzüge in der Einkommensteuer** | 6,8 % des Erwerbseinkommens (zusammen 154 Mrd. €) | Eichung | Der Rechenkern kennt nur die Werbungskostenpauschale und die Sozialbeiträge. Werbungskosten darüber, Kirchensteuer, Spenden, Riester und Rürup, außergewöhnliche Belastungen und steuerfreie Lohnteile (Zuschläge, Entgeltumwandlung) stehen in diesem einen Anteil. Er ist so gewählt, dass die Lohn- und Einkommensteuer samt Soli 405 Mrd. € ergibt (Kassenstatistik 2025: Lohnsteuer 262,7 + Kindergeld 54,6 + veranlagte Einkommensteuer 78,2 + Soli rund 9,5). Ohne diese Abzüge wären es 458 Mrd. € |
| Gewinne Selbständiger | Median 45.000 €, Streuung 0,95; KV 40 % privat, sonst rund 20 % freiwillig gesetzlich | Annahme | Summe der Gewinne 271 Mrd. € |
| Beamte und Pensionäre | Besoldung Median 4.200 €, Pension Median 3.400 € | Annahme | Summe 170 Mrd. € (Beihilfe 22,6 Mrd. = 13 %) |
| Renten | Rentnerinnen allein Median 1.550 €, Rentner 1.800 €, Paare 1.850 + 1.100 €, dazu Betriebs- und Zusatzrenten bei der Hälfte | Statistik, gerundet | Alterssicherungsbericht 2024; Summe 355 Mrd. € |
| Bürgergeld | Regelbedarf plus Miete und Heizung, abzüglich Kindergeld (wird angerechnet, § 11 SGB II) | Recht | Summe 38,7 Mrd. € samt Grundsicherung im Alter. Bis 14.11. war das Kindergeld doppelt gezählt (3,4 Mrd. € zu viel); Familien in der Grundsicherung lagen dadurch über dem Freibetrag und zahlten scheinbar Ausgabensteuer |
| Andere Leistungen in Geld (Arbeitslosen-, Kranken-, Elterngeld, BAföG) | 54 Mrd. € | Annahme | für die Haushalte neutral gerechnet (die Reform müsste sie anpassen). Wer nur davon lebt, für den zahlt der Träger mit der Reform die Prämie der Krankenkasse, wie heute die Beiträge (§ 251, § 224 SGB V); Schalter `praemieLeistung` |
| Krankenkasse ohne Arbeit, Rente oder Leistungen | Wer vom Ersparten lebt, zahlt heute freiwillig mindestens den Mindestbeitrag: 20 % von 14.000 € im Jahr (rund 230 € im Monat), sonst 20 % der Einnahmen bis zur Bemessungsgrenze; ein Beitrag je Haushalt (Partner mitversichert); 0,57 Mio. Haushalte, 1,6 Mrd. € | Recht/Annahme | § 240 SGB V. Erwachsene Kinder unter 25 ohne Einkommen sind bei den Eltern mitversichert und zahlen mit der Reform die Prämie selbst (außer in Bildung oder Bürgerjob, die das Modell nicht abbildet). Bis 14.11. fehlte der heutige Beitrag |

**Abgleich:** Alle Summen mit Soll, Ist und Abweichung stehen in [abgleich.md](abgleich.md) (erzeugt mit `node abgleich.js`).

## 2. Vermögen

| Was | Wert | Art | Quelle |
|---|---|---|---|
| Haushalte und Vermögen je Stufe | 8 Stufen von unter 100.000 € bis über 100 Mio. €, zusammen 16,6 Bio. € | Eichpunkt | vermoegen-heute.json (PHF 2023: Median 103.200 €, P90 777.200 €, plus Reichenzuschätzung) |
| Zusammensetzung je Stufe | eigenes Heim, andere Immobilien, Geld und Wertpapiere, Betriebe | Eichpunkt | SVR 2025 |
| Wer welches Vermögen hat | Rang aus Einkommen (0,6), Alter (0,55), Selbständigkeit (0,3) und Zufall | Annahme | geeicht auf PHF: Median 55–74 Jahre rund 140.000 € (Modell: Rentner 138.500 €) |
| Eigentümer | 6 % bis 95 % je Stufe, zusammen 42 % | Statistik | Mikrozensus 2022: 41,9 % |
| Bezahlter Teil des eigenen Hauses | Rentner 96 %, Erwerbstätige 75 %; 68 % der erwerbstätigen und 19 % der Rentner-Eigentümer zahlen noch ab | Statistik/Schätzung | Restschuld geeicht auf 1,15 Bio. € (Bundesbank: Wohnungsbaukredite an private Haushalte rund 1,58 Bio. €, davon rund drei Viertel für das eigene Heim). Bis 14.11. lag sie fälschlich bei 3,8 Bio. € |
| Mietwert | 3,2 % des Hauswerts, zusammen 214,5 Mrd. € | Statistik | Eurostat, wie Version 31 |
| Ausgezahlte Zinsen und Dividenden | 1,0 % (kleine Vermögen) bis 3,0 % (ab 1 Mio. €) des Geldvermögens | Annahme | Bundesbank: kleine Vermögen liegen auf Konten und in Versicherungen |
| Mieten | 3,5 % netto, davon 35 % steuerpflichtig (Abschreibung, Zinsen) | Annahme | Eichpunkt; Einkommensteuerstatistik |
| Betriebe ab 1 Mio. € Vermögen | 7 % Gewinn, die Hälfte ausgeschüttet, der Rest bleibt in der GmbH (Körperschaftsteuer) | Eichpunkt/Annahme | |

## 3. Konsum und Sparen

| Was | Wert | Art | Quelle |
|---|---|---|---|
| Eichung (Standard) | Konsum genau 2.085,7 Mrd. € ohne Mietwert (VGR 2025: Konsum der Haushalte 2.305,4, Version 31: 2.300,2, jeweils − 214,5 Mietwert); wahlweise Sparquote 10,4 % | Statistik | VGR 2025 |
| Sparen nach Gruppen | Rentnerhaushalte sparen 10 Punkte weniger, Selbständige 6 Punkte mehr als Arbeitnehmer bei gleichem Einkommen | Statistik | EVS 2018 (Fachserie 15 Heft 4, Tabelle 1.2): Konsum je Nettoeinkommen Arbeitnehmer 71,0 %, Ruhestand 83,3 %, Selbständige 62,4 %. Geeicht wird der Abstand zu den Arbeitnehmern (`node eichen_sparen.js`); das Verhältnis statt des Abstands verlangte von Rentnern mehr Konsum, als Einkommen und Erspartes hergeben |
| Sparquote nach Einkommen | rund 7 Punkte mehr je Verdopplung des Einkommens: + 0,10 × ln(Einkommen/30.000), über 100.000 € zusätzlich + 0,08 × ln(Einkommen/100.000) | Studie | EVS 2018: unten Entsparen, oben 20–40 % |
| Kapitalerträge | nach Steuer zur Hälfte ausgegeben (ab 1 Mio. € zu einem Viertel), der Rest wieder angelegt | Studie | Baker, Nagel, Wurgler 2007; Di Maggio, Kermani, Majlesi 2020 |
| Verzehr von Erspartem im Alter | 1 % (65 Jahre) bis 3,5 % (90 Jahre) des Geldvermögens | Annahme | PHF: Ältere entsparen langsam |

**Geklärte Abweichung (Stand 14.11.):** Vor der Eichung ergab die amtliche Sparquote nur 1.910 Mrd. € Konsum. Der Grund waren
fehlende Löhne (1.825 statt 2.036 Mrd. €). Seit der Eichung liegen beide Wege nah beieinander: Mit der Sparquote ergibt sich 2.068 Mrd. €
Konsum, 1 % unter der amtlichen Summe. Offen bleibt: Gewinne und Entnahmen aus Firmen liegen im Modell bei 389 Mrd. €, in der VGR bei
540 Mrd. € (Selbständigeneinkommen 175,6 + Ausschüttungen und Entnahmen 364,3). Rechnet man sie hinzu, ändert sich die Zahl der
Haushalte mit weniger um weniger als 1,5 Mio.

**Ehrliche Spanne der Haushalte mit weniger** (`node spanne.js`, alle Zeilen in `spanne.json`): Gerechnet wird mit beiden Ankern der Eichung
(Konsum oder Sparquote) und mit mehr Gewinnen und Kapitalerträgen bei den Haushalten (Ausschüttungen × 2, Ausschüttungen × 1,5 und Gewinne × 1,2,
Kapitalerträge × 1,5), weil offen ist, wo die fehlenden rund 150 Mrd. € liegen.

| | Standard | Spanne |
|---|---|---|
| ohne Ausgleich | 17,7 Mio. (43 %) | 16,2 bis 19,8 Mio. |
| mit dem Ausgleich von Version 32 (Rentner bis 300 €, 10 € je Erwachsenem) | 11,2 Mio. (27 %) | 9,9 bis 13,3 Mio. |

Vor der Korrektur von Kindergeld und Krankenkasse (14.11., 13 Uhr) waren es 18,3 und 11,9 Mio.

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

## 4a. Ausgleich (Version 32, Tomas 14.11.2026)

| Was | Wert | Art | Quelle |
|---|---|---|---|
| Ausgleich für heutige Rentner | Wer heute Rente oder Pension bezieht und mit der Reform weniger hätte, bekommt das Minus bis 300 € im Monat ersetzt; läuft mit den heutigen Rentnern aus | Vorschlag | Version 32; `ausgleichRentnerMonat` in `simulation.js`, auf der Seite einstellbar |
| Für jeden Erwachsenen | 10 € im Monat | Vorschlag | Version 32; `pauschaleErwMonat` |
| Kosten im ersten Jahr | 22,7 Mrd. € | Rechnung | `node steuerlast.js` (Feld `ausgleich_mrd`); das Buch rechnet die 10 € mit 69,6 Mio. Erwachsenen (8,35 Mrd. €), das Modell kennt 65,6 Mio. |

In `simulation.js` stehen beide Werte auf 0, damit die Grundrechnung die Reform ohne Ausgleich zeigt. Die Seite und `steuerlast.js` setzen sie
auf Version 32. Ergebnis: 72,8 % der Haushalte haben mehr, 11,2 Mio. weniger (im Mittel 554 € im Monat).

## 4b. Wer heute wie viel zahlt und wie es mit der Reform wäre (steuerlast.js)

- **Last heute:** Einkommensteuer mit Soli, Sozialbeiträge der Haushalte, Steuer auf Kapitalerträge, Mehrwertsteuer und Erbschaftsteuer.
- **Last mit der Reform:** Ausgabensteuer und Mehrwertsteuer, neue Sozialbeiträge, Staatsanteil am Erbe; abgezogen werden Auszahlungen,
  Bestandsschutz und Ausgleich. Probe: Last heute minus Last mit Reform ergibt für jeden Haushalt genau sein Plus (Abweichung 0,00 €).
- **Erstes Jahr:** Staatsanteil am Erbe zu 25 % fällig, langfristig 50 %. Die Hausregel gilt nur für Häuser, die nach dem Start gekauft werden,
  wirkt im ersten Jahr also nicht (`node steuerlast.js haus` rechnet sie zum Vergleich trotzdem ein).
- **Farbfeld:** Einkommenszehntel mal Vermögenszehntel; Farbe = Plus oder Minus in % des Einkommens, mit Erbe. Felder mit weniger als
  30 künstlichen Haushalten sind schraffiert.
- **Welche Einkommen zahlen:** Die Last ohne Erbe wird jedem Haushalt nach den Anteilen seiner Einkommensarten (Lohn, Rente, Firmengewinn,
  Zinsen, Mieten, Sozialleistungen) zugeordnet. Die Erbschaftsteuer nach der Zusammensetzung des Nachlasses: heute Haus und vermietete
  Immobilien zu drei Vierteln bewertet und Betriebe zu 15 %, mit der Reform voll.
- **Sparen:** verfügbares Einkommen minus Konsum minus Unterhalt; mit der Reform zusätzlich das Plus. Wachstum = Sparen in % des Vermögens.

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
