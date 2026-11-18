/* Erklärungen zu den Info-Knöpfen im E-Auto-Rechner (siehe ../info.js) */
(() => {
  const K10 = ["kapitel-10.html#strom-zu-hause", "Kapitel 10, Strom und Wärme zu Hause"],
    EA = ["kapitel-5.html#elektroauto-mit-zinslosem-darlehen", "Kapitel 5, Elektroauto mit zinslosem Darlehen"],
    SP = ["kapitel-5.html#jedes-auto-ein-speicher", "Kapitel 5, Jedes Auto ein Speicher"],
    CO2 = ["anhang-b.html#heizen-und-verkehr-aufschlag-bis-zum-preispfad", "Anhang B7, Heizen und Verkehr"];
  const e = (t, b) => [t, ...(b || [])];
  Info.felder({
    km: e("Wie viele Kilometer du im Jahr fährst. In Deutschland sind es im Schnitt rund 13.000 km. Je mehr du fährst, desto schneller holt das Elektroauto den höheren Kaufpreis herein, weil jeder Kilometer billiger ist.", K10),
    jahre: e("So lange rechnet der Rechner, vom Kauf bis zum Verschrotten oder Verkauf. Ein Restwert beim Verkauf wird nicht abgezogen, bei beiden Autos nicht. Autos fahren in Deutschland im Schnitt rund 18 Jahre."),
    kaufjahr: e("Im Kaufjahr beginnt die Rechnung. Davon hängt ab, wie lange das Elektroauto keine Kfz-Steuer zahlt, und beim Dienstwagen, welche Grenze für den Listenpreis gilt."),
    iPreis: e("Was der Verbrenner beim Kauf kostet, nach Rabatt. Vergleiche am besten zwei ähnliche Autos, etwa dasselbe Modell als Benziner und als Elektroauto."),
    iVerb: e("Liter Sprit auf 100 km, wie du wirklich fährst. Die Herstellerangabe ist meist etwas zu niedrig. Steht oft im Bordcomputer."),
    iKraft: e("Benzin oder Diesel. Diesel setzt je Liter etwas mehr CO₂ frei (2,65 statt 2,37 kg), deshalb steigt sein Preis mit dem CO₂-Preis etwas stärker.", CO2),
    iSprit: e("Was ein Liter heute an der Tankstelle kostet. Darin steckt schon ein CO₂-Preis. Der Rechner lässt ihn in den nächsten Jahren steigen, so wie der EU-Emissionshandel es erwarten lässt. Alles andere bleibt auf dem Preis von heute.", CO2),
    iSteuer: e("Die Kfz-Steuer im Jahr für den Verbrenner. Sie steht im Steuerbescheid oder lässt sich beim Zoll ausrechnen."),
    iVers: e("Haftpflicht und Kasko im Jahr. Für ein vergleichbares Elektroauto ist sie meist ähnlich hoch."),
    iWart: e("Inspektion, Ölwechsel, Bremsen, Auspuff, Reparaturen im Schnitt eines Jahres. Elektroautos brauchen weniger, weil Ölwechsel, Kupplung und Auspuff wegfallen und die Bremsen kaum abnutzen."),
    ePreis: e("Was das Elektroauto beim Kauf kostet, nach Rabatt. Eine staatliche Kaufprämie gibt es heute nicht. Das Buch schlägt stattdessen ein zinsloses Darlehen vor.", EA),
    eVerb: e("Kilowattstunden Strom auf 100 km laut Hersteller (WLTP). Im Winter braucht das Auto für Heizung und kalte Batterie rund 15 bis 25 % mehr. Wer viel im Winter fährt, trägt hier etwas mehr ein."),
    eVerlust: e("Beim Laden geht ein Teil des Stroms als Wärme verloren, typisch 10 bis 15 %. Bezahlt wird der Strom, der aus der Steckdose kommt, nicht der, der in der Batterie ankommt."),
    eHaus: e("Was eine Kilowattstunde zu Hause kostet, mit allem: Arbeitspreis auf der Stromrechnung. Mit eigener PV-Anlage oder dynamischem Tarif wird es billiger, das rechnet der Energie-Rechner genau.", K10),
    eOff: e("Was eine Kilowattstunde an öffentlichen Ladesäulen kostet. Schnellladen an der Autobahn ist teurer, Laden beim Supermarkt oft billiger."),
    eAnteil: e("Wie viel du zu Hause oder bei der Arbeit lädst. Der Rest wird unterwegs geladen. Je mehr zu Hause, desto billiger wird jeder Kilometer."),
    eVers: e("Haftpflicht und Kasko im Jahr für das Elektroauto."),
    eWart: e("Inspektion und Reparaturen im Schnitt eines Jahres. Meist deutlich weniger als beim Verbrenner."),
    eSteuerNach: e("Reine Elektroautos, die bis Ende 2030 zugelassen werden, zahlen bis zu zehn Jahre keine Kfz-Steuer, längstens bis Ende 2035. Danach zahlen sie nach Gewicht, halbiert, meist 30 bis 100 € im Jahr."),
    eWallbox: e("Eine eigene Ladestation zu Hause, mit Einbau. Wer schon eine hat oder an der normalen Steckdose lädt, trägt 0 ein."),
    thg: e("Halter von Elektroautos dürfen ihre CO₂-Einsparung jedes Jahr verkaufen, über einen Anbieter im Internet. Das bringt 2026 meist 300 bis 380 € im Jahr. Wie hoch die Prämie später ist, weiß niemand, deshalb kannst du hier einstellen, bis wann sie zählt."),
    thgBis: e("Bis zu diesem Jahr rechnet der Rechner mit der THG-Prämie, danach ohne. Vorsichtig ist ein Jahr nicht zu weit in der Zukunft."),
    methode: e("Wie der Weg zur Arbeit beim Dienstwagen versteuert wird: pauschal mit 0,03 % des Listenpreises je Kilometer und Monat oder genau je Fahrt mit 0,002 %. Je Fahrt lohnt sich, wenn du selten ins Büro fährst."),
    entf: e("Die einfache Strecke von der Wohnung zur Arbeit in Kilometern."),
    fahrten: e("Wie oft im Jahr du zur Arbeit fährst. Zählt nur bei der Abrechnung je Fahrt, höchstens 180 Fahrten."),
    satz: e("Von jedem zusätzlichen Euro geldwerten Vorteil gehen Steuer und Sozialabgaben ab. Bei mittlerem Einkommen sind das zusammen etwa 40 bis 50 %. Über der Beitragsgrenze fallen nur noch Steuern an."),
    agLaden: e("Lädst du beim Arbeitgeber oder erstattet er dir den Strom für zu Hause, ist das steuerfrei. Dann zahlst du für den Strom des Dienstwagens nichts selbst."),
    dJahre: e("Wie viele Jahre du den Dienstwagen fährst. Danach geht er meist zurück."),
  });
  Info.texte("#tiles", {
    "Verbrenner gesamt": e("Alles, was der Verbrenner über die ganze Nutzungsdauer kostet: Kauf, Sprit, Steuer, Versicherung und Werkstatt, zusammengezählt. Darunter steht, was das je 100 km sind."),
    "Elektroauto gesamt": e("Alles, was das Elektroauto über die ganze Nutzungsdauer kostet: Kauf, Wallbox, Strom, Steuer, Versicherung und Werkstatt, abzüglich THG-Prämie. Darunter steht, was das je 100 km sind."),
    "Energie je 100 km": e("Was Sprit und Strom für 100 km kosten, heute. Beim Strom ist der Mix aus Laden zu Hause und unterwegs eingerechnet, mit Ladeverlusten.", K10),
    "Kfz-Steuer E-Auto": e("Bis zu diesem Jahr zahlt das Elektroauto keine Kfz-Steuer, danach den Betrag, den du eingetragen hast."),
  });
  Info.texte("#cumT", { "": e("Die Linien zählen alle Kosten seit dem Kauf zusammen. Am Anfang liegt das Elektroauto höher, weil es teurer ist. Weil jeder Kilometer billiger ist, holt es auf. Wo sich die Linien kreuzen, hat es sich bezahlt gemacht.") });
  Info.texte("#t100", {
    "Anschaffung": e("Der Kaufpreis, verteilt auf alle Kilometer. Beim Elektroauto mit Wallbox."),
    "Sprit oder Strom": e("Was du für Sprit oder Strom bezahlst, zu den Preisen von heute."),
    "Versicherung": e("Haftpflicht und Kasko, verteilt auf alle Kilometer."),
    "Wartung und Reparaturen": e("Werkstatt, verteilt auf alle Kilometer."),
    "Kfz-Steuer": e("Kfz-Steuer, verteilt auf alle Kilometer. Das Elektroauto zahlt in den ersten Jahren nichts."),
    "Steigender CO₂-Preis im Sprit": e("Was der Sprit mehr kostet, weil der CO₂-Preis in den nächsten Jahren steigt. Das Buch schlägt vor, dieses Geld als Klimageld an alle zurückzugeben.", CO2),
    "THG-Prämie": e("Die Prämie für die eingesparte CO₂-Menge, die Halter von Elektroautos jedes Jahr bekommen. Sie senkt die Kosten, deshalb steht sie mit Minus da."),
    "Zusammen": e("Alle Kosten je 100 km zusammen. Der Unterschied zwischen den beiden Spalten ist, was das Elektroauto je 100 km spart oder mehr kostet."),
  });
  Info.texte("#t_dw", {
    "Bemessungsgrundlage": e("Der Bruttolistenpreis, von dem der geldwerte Vorteil berechnet wird. Bei reinen Elektroautos zählt nur ein Viertel (bis 100.000 €) oder die Hälfte davon."),
    "Private Nutzung": e("Für jeden Monat wird 1 % der Bemessungsgrundlage zum Lohn gezählt, als ob du so viel mehr verdienen würdest. Darauf zahlst du Steuer und Abgaben."),
    "Arbeitsweg": e("Für den Weg zur Arbeit kommt noch etwas dazu: 0,03 % je Kilometer und Monat oder 0,002 % je Fahrt."),
    "Geldwerter Vorteil": e("Private Nutzung und Arbeitsweg zusammen. So viel wird im Monat zu deinem Lohn gezählt."),
    "Eigener Ladestrom": e("Was du für den Strom selbst bezahlst, wenn der Arbeitgeber ihn nicht übernimmt."),
    "Steuer und Abgaben": e("Lohnsteuer und Sozialabgaben auf den geldwerten Vorteil, mit dem Satz, den du oben eingetragen hast."),
    "Über": e("Was dich der Dienstwagen über die ganze Dauer der Überlassung kostet."),
    "Deine Belastung im Monat": e("Steuer und Abgaben auf den geldwerten Vorteil plus eigener Strom. So viel kostet dich der Dienstwagen jeden Monat."),
  });
})();
