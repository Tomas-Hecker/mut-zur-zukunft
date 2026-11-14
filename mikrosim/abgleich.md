# Soll/Ist-Abgleich der Mikrosimulation

Stand 2026-11-14. Erzeugt mit `node abgleich.js`. „Soll“ ist die amtliche Zahl, „Ist“ die Summe der künstlichen Haushalte.

| Bereich | Größe | Soll | Ist | Abweichung | Quelle | Bemerkung |
|---|---|---|---|---|---|---|
| Bevölkerung | Haushalte (Mio.) | 41,1 | 41,3 | 0,4 % | Mikrozensus 2025 | geeicht |
| Bevölkerung | Erwachsene (Mio.) | 69,6 | 65,6 | -5,8 % | Bevölkerungsstatistik 2025, 18 Jahre und älter | fehlt: Heime, Teil der erwachsenen Kinder |
| Bevölkerung | Kinder unter 18 (Mio.) | 14,3 | 14,1 | -1,6 % | Bevölkerungsstatistik 2025 |  |
| Bevölkerung | Haushalte im Eigentum (Anteil %) | 41,9 | 41,9 | 0,1 % | Mikrozensus 2022 | geeicht |
| Einkommen | Bruttolöhne und -gehälter (Mrd. €) | 2.036,3 | 2.036,3 | -0,0 % | VGR 2025, Destatis Fachserie 18 Reihe 1.4 (Stand 02.06.2026), Tab. 2.1.8 | geeicht (Faktor 1,11 auf die Löhne der Umfrage) |
| Einkommen | Renten der Rentenversicherung und Betriebsrenten (Mrd. €) | – | 355,2 | – | Alterssicherungsbericht; VGR enthält sie in 836,7 Mrd. € Sozialleistungen | kein direkter Vergleich |
| Einkommen | Gewinne der Selbständigen und Ausschüttungen (Mrd. €) | 539,9 | 388,7 | -28,0 % | VGR 2025, Destatis Fachserie 18 Reihe 1.4 (Stand 02.06.2026), Konto II.1.2: Selbständigeneinkommen 175,6 + Ausschüttungen und Entnahmen 364,3 | Modell niedriger: Entnahmen aus Personengesellschaften nur teilweise erfasst |
| Einkommen | Verfügbares Einkommen (Mrd. €) | 2.583,7 | 2.302,8 | -10,9 % | VGR 2025, Destatis Fachserie 18 Reihe 1.4 (Stand 02.06.2026), Konto II.2 | Modell ohne Organisationen ohne Erwerbszweck (rund 67), ohne unterstellte Zinsen (FISIM, rund 51) und Versicherungserträge (rund 38): vergleichbar rund 2.428 |
| Steuern | Lohn- und Einkommensteuer samt Soli (Mrd. €) | 405,0 | 405,0 | 0,0 % | Kassenstatistik 2025: Lohnsteuer 262,7 + Kindergeld 54,6 + veranlagte 78,2 + Soli rund 9,5 | geeicht über Abzüge von 6,8 % des Erwerbseinkommens |
| Steuern | Mehrwertsteuer der Haushalte (Mrd. €) | – | 208,8 | – | Umsatzsteuer gesamt 310,2 (auch Staat, Vereine, Wohnungsbau) | Anteil der Haushalte plausibel |
| Konsum | Konsum ohne Mietwert (Mrd. €) | 2.085,7 | 2.087,6 | 0,1 % | VGR 2025, Destatis Fachserie 18 Reihe 1.4 (Stand 02.06.2026): Haushalte 2.305,4 − Mietwert 214,5 (Version 31: 2.300,2 − 214,5) | geeicht |
| Vermögen | Restschuld auf das eigene Heim (Bio. €) | 1,2 | 1,2 | 3,3 % | Bundesbank: Wohnungsbaukredite an private Haushalte rund 1,58 Bio. € (2025), davon rund drei Viertel für das eigene Heim (Schätzung) | geeicht; davor 3,8 Bio. € (Fehler, zu hoch) |
| Vermögen | Mietwert, der nach der Reform besteuert wird (Anteil %) | – | 19,3 | – | Regel „Eigenes Haus frei“: nur der beim Start noch nicht bezahlte Teil |  |
| Konsum | Mietwert selbst genutzter Wohnungen (Mrd. €) | 214,5 | 214,5 | 0,0 % | Eurostat, wie Version 31 | geeicht |
| Vermögen | Nettovermögen der Haushalte (Bio. €) | 16,6 | 16,8 | 1,4 % | Eichpunkt: PHF 2023 plus Zuschätzung der Reichsten | geeicht |
| Erbschaft | Erbschaftsteuer heute (Mrd. €) | 21,4 | 19,9 | -7,2 % | festgesetzte Erbschaft- und Schenkungsteuer 2025 | Modell etwas niedriger |
| Erbschaft | Nachlässe und Schenkungen (Mrd. €) | 300–400 | 318,4 | – | DIW-Schätzung | im Bereich |

## Sparen nach Gruppen (EVS 2018, Fachserie 15 Heft 4, Tabelle 1.2)

Anteil der Konsumausgaben am Haushaltsnettoeinkommen, mit Mietwert auf beiden Seiten, Haushalte unter 18.000 € netto im Monat. Die EVS erfasst weniger Konsum als die VGR; verglichen wird deshalb der Abstand zu den Arbeitnehmerhaushalten.

| Gruppe | EVS | Abstand zu Arbeitnehmern (EVS) | Modell | Abstand (Modell) |
|---|---|---|---|---|
| Arbeitnehmer | 71,0 % | 0,0 Punkte | 94,4 % | 0,0 Punkte |
| Ruhestand | 83,3 % | 12,4 Punkte | 106,1 % | 11,7 Punkte |
| Selbständige | 62,4 % | -8,5 Punkte | 85,7 % | -8,7 Punkte |
