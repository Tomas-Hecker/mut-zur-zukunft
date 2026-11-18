/* Erklärungen zu den Info-Knöpfen im Balkon-Rechner (siehe ../info.js) */
(() => {
  const K10 = ["kapitel-10.html#strom-zu-hause", "Kapitel 10, Strom und Wärme zu Hause"],
    STR = ["kapitel-5.html#strom", "Kapitel 5, Strom aus Sonne und Wind"],
    MARKT = ["kapitel-5.html#mehr-wettbewerb-strom-teilen-preise-sehen", "Kapitel 5, Strom teilen, Preise sehen"];
  const e = (t, b) => [t, ...(b || [])];
  Info.felder({
    plz: e("Deine Postleitzahl. Der Rechner lädt dann im Hintergrund das typische Wetter deines Postleitzahlbereichs (die ersten drei Ziffern), Stunde für Stunde ein ganzes Jahr, aus Messungen und Satellitendaten der EU. Gespeichert wird sie nicht."),
    hh: e("Wie viel Strom dein Haushalt im Jahr braucht. Steht auf der Jahresabrechnung. Je mehr du tagsüber verbrauchst, desto mehr vom Balkonstrom nutzt du selbst.", K10),
    wp: e("Die Spitzenleistung der Module in Watt Peak. Zwei übliche Module haben zusammen rund 800 Wp. Erlaubt sind bis 2.000 Wp, am Schukostecker bis 960 Wp."),
    wr: e("Der Wechselrichter macht aus dem Gleichstrom der Module Strom für die Steckdose. Er darf höchstens 800 W ins Haus geben. Liefern die Module mehr, wird der Rest abgeschnitten."),
    azi: e("In welche Himmelsrichtung die Module zeigen. Süd bringt am meisten, Ost und West etwas weniger, dafür morgens oder abends."),
    neig: e("Wie steil die Module stehen. Senkrecht am Geländer bringt im Sommer weniger, im Winter aber fast so viel wie schräg. 35° ist übers Jahr am besten."),
    schatten: e("Wie viel Strom durch Bäume, Nachbarhäuser oder den Balkon darüber verloren geht, in Prozent übers Jahr."),
    verl: e("Verluste in Wechselrichter, Kabeln und durch Schmutz, typisch 10 %."),
    pvKost: e("Was das Set kostet: zwei Module, Wechselrichter und Kabel. 2026 oft 200 bis 500 €, mit Halterung."),
    montage: e("Falls jemand die Anlage für dich anbringt. Selbst montieren ist erlaubt."),
    pvJahre: e("So lange rechnet der Rechner mit der Anlage. 25 Jahre sind vorsichtig, oft halten die Module länger. Beim Umzug nimmst du sie mit."),
    deg: e("Module werden mit den Jahren etwas schwächer, typisch 0,25 bis 0,5 % im Jahr."),
    wrKost: e("Der Wechselrichter hält meist nicht so lange wie die Module. Das kostet ein neuer."),
    wrJahre: e("Nach so vielen Jahren wird der Wechselrichter ersetzt."),
    batKwh: e("Ein kleiner Speicher hebt Mittagsstrom für den Abend auf. 0 heißt: ohne Speicher. Unten in der Tabelle siehst du, ob sich ein Speicher lohnt."),
    batFix: e("Was das Speichergerät ohne Akku kostet."),
    batKwhKost: e("Was jede Kilowattstunde Akku zusätzlich kostet."),
    batWg: e("Von 100 kWh, die hineingehen, kommen so viele wieder heraus, typisch 90 %."),
    batStand: e("Der Speicher braucht selbst etwas Strom, auch wenn er nichts tut, in Watt. Das geht von der Ersparnis ab."),
    batJahre: e("Wie lange der Akku hält, meist 10 bis 15 Jahre."),
    steuer: e("Mit einem Sensor am Stromzähler gibt der Speicher genau so viel ab, wie gerade gebraucht wird. Ohne Sensor gibt er eine feste Leistung ab, dann geht manches ungenutzt ins Netz."),
    grund: e("Wie viel Watt der Speicher ohne Sensor gleichmäßig abgibt. Etwa so viel, wie Kühlschrank, Router und Geräte im Bereitschaftsbetrieb immer brauchen."),
    tarif: e("Fester Preis: jede kWh kostet gleich viel. Dynamisch: der Preis folgt der Strombörse, Stunde für Stunde.", MARKT),
    fest: e("Was eine kWh in deinem Stromvertrag kostet, mit allem."),
    netz: e("Beim dynamischen Tarif: was der Netzbetreiber je kWh bekommt, ohne Mehrwertsteuer."),
    abg: e("Beim dynamischen Tarif: Stromsteuer, Konzessionsabgabe und Umlagen je kWh, ohne Mehrwertsteuer.", STR),
    aufs: e("Was der Anbieter beim dynamischen Tarif zusätzlich zum Börsenpreis verlangt."),
    einsp: e("Für Strom vom Balkon, der ins Netz geht, gibt es normalerweise nichts. Wer die Anlage anmeldet und einen passenden Zähler hat, kann eine kleine Vergütung bekommen."),
    zins: e("Der Zins, den dein Geld sonst auf dem Sparkonto bringen würde. Damit wird gerechnet, ob sich die Anlage mehr lohnt als Sparen."),
    steig: e("Wie stark der Strompreis jedes Jahr steigt. 2 % entsprechen etwa der Inflation."),
    foerd: e("Manche Städte und Gemeinden geben einen Zuschuss. Frag bei deiner Stadt nach."),
  });
  Info.texte("#eing", {
    "Dein Ort": e("Mit deiner Postleitzahl rechnet der Rechner mit Sonne und Temperatur deines Orts, Stunde für Stunde. Ohne Postleitzahl mit Idstein im Taunus."),
    "Haushalt": e("Dein Stromverbrauch. Der Rechner verteilt ihn über den Tag so, wie Haushalte typischerweise Strom brauchen."),
    "Balkonkraftwerk": e("Ein, zwei Solarmodule am Balkon oder auf der Terrasse, die über die Steckdose Strom ins Haus geben. Was gerade läuft, nutzt den Strom zuerst.", STR),
    "Speicher": e("Ein Akku, der Strom vom Mittag für den Abend aufhebt."),
    "Strompreis": e("Was du heute für Strom bezahlst. Jede selbst genutzte kWh spart genau diesen Preis."),
    "Wirtschaftlichkeit": e("Womit der Rechner prüft, ob sich die Anlage lohnt."),
  });
  const wrap = document.querySelector(".wrap") || document.body;
  Info.texte(wrap, {
    "Ergebnis": e("Der Rechner spielt ein ganzes Jahr Stunde für Stunde durch: Wie viel die Module liefern, wie viel du davon gleich verbrauchst und was du damit sparst.", K10),
    "Mit oder ohne Speicher": e("Die Anlage mit verschiedenen Speichergrößen verglichen. Meist lohnt sich ein Speicher am Balkon nicht, weil er teurer ist als der Strom, den er zusätzlich nutzbar macht."),
    "Strom vom Balkon, Monat für Monat": e("Wie viel die Anlage in jedem Monat liefert, wie viel du davon nutzt und wie viel ins Netz geht."),
    "Ein Sommertag und ein Wintertag": e("Stunde für Stunde: wann die Module Strom liefern und wann du ihn brauchst."),
    "Welche Ausrichtung bringt wie viel": e("Wie viel die Module im Jahr bringen, je nach Himmelsrichtung und Neigung, mit dem Wetter deines Orts."),
  });
  Info.texte("#tiles", {
    "Ertrag am Modul": e("So viel Strom liefern die Module im Jahr. Darunter: je kWp, damit du mit anderen Anlagen vergleichen kannst."),
    "Selbst genutzt": e("So viel Balkonstrom verbrauchst du sofort im Haus. Nur diese kWh sparen Geld. Darunter: welcher Anteil deines Verbrauchs das ist."),
    "Ins Netz": e("Strom, den du gerade nicht brauchst, geht ins Netz, meist ohne Vergütung."),
    "Ersparnis im 1. Jahr": e("Selbst genutzter Strom mal Strompreis: so viel weniger zahlst du im ersten Jahr."),
    "Kosten": e("Was die Anlage kostet, mit Montage und Speicher, abzüglich Zuschuss."),
    "Gewinn über": e("Was nach allen Kosten über die ganze Lebensdauer übrig bleibt, mit steigendem Strompreis. Darunter der heutige Wert, wenn du stattdessen zum eingetragenen Zins sparen würdest."),
  });
  Info.texte("#vgl", {
    "Speicher": e("Die Größe des Akkus."),
    "Selbst genutzt": e("Wie viel Balkonstrom du mit dieser Speichergröße selbst nutzt."),
    "Ersparnis 1. Jahr": e("Was du im ersten Jahr sparst."),
    "Kosten": e("Was Anlage und Speicher zusammen kosten."),
    "Bezahlt nach": e("Nach so vielen Jahren hat die Ersparnis die Kosten wieder hereingeholt."),
    "Rendite": e("Wie viel Prozent im Jahr das eingesetzte Geld bringt, wie ein Zins. Zum Vergleich: ein Sparkonto bringt 2 bis 3 %."),
    "Speicher allein bezahlt": e("Ob sich der Speicher für sich genommen bezahlt macht, bevor er kaputt ist."),
  });
  Info.texte("#ot", { "Ausrichtung": e("Ertrag im Jahr je Himmelsrichtung (Zeilen) und Neigung (Spalten). 90° heißt senkrecht, etwa am Balkongeländer.") });
})();
