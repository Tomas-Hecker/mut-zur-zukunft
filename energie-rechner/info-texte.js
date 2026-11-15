/* Erklärungen zu den Info-Knöpfen im Energie-Rechner (siehe ../info.js) */
(() => {
  const K10 = ["kapitel-10.html#strom-zu-hause", "Kapitel 10, Strom und Wärme zu Hause"],
    STR = ["kapitel-5.html#strom", "Kapitel 5, Strom aus Sonne und Wind"],
    SIM = ["anhang-b.html#strom-simulation", "Anhang B5, Strom zur richtigen Stunde"],
    MARKT = ["kapitel-5.html#mehr-wettbewerb-strom-teilen-preise-sehen", "Kapitel 5, Strom teilen, Preise sehen"],
    AUTO = ["kapitel-5.html#jedes-auto-ein-speicher", "Kapitel 5, Jedes Auto ein Speicher"],
    WP = ["kapitel-5.html#waermepumpe", "Kapitel 5, Wärmepumpe mit zinslosem Kredit"];
  const e = (t, b) => [t, ...(b || [])];
  Info.felder({
    plz: e("Deine Postleitzahl. Der Rechner lädt dann im Hintergrund das typische Wetter deines Postleitzahlbereichs (die ersten drei Ziffern), Stunde für Stunde ein ganzes Jahr, aus Messungen und Satellitendaten der EU. Gespeichert wird sie nicht."),
    hh: e("Der Strom für Licht, Kochen, Waschen und Geräte im Jahr, ohne Wärmepumpe und Auto. Steht auf der Jahresabrechnung. Typisch: 1 Person 1.500, 3 Personen 3.500 kWh.", K10),
    pvS: e("Leistung der Solarmodule auf der Südseite des Dachs, in Kilowatt Peak. Ein Modul hat heute etwa 0,45 kWp. 10 kWp brauchen rund 50 m² Dach. 0 heißt: keine Module auf dieser Seite.", STR),
    pvO: e("Leistung der Module auf der Ostseite. Ost und West bringen etwas weniger als Süd, dafür mehr Strom morgens und abends, wenn du ihn brauchst."),
    pvW: e("Leistung der Module auf der Westseite. Westmodule liefern bis in den Abend."),
    neig: e("Wie steil das Dach ist, in Grad. 30 bis 35° ist für Süd ideal, flachere Dächer bringen im Sommer mehr, im Winter weniger."),
    pvKost: e("Was die Anlage mit Montage je kWp kostet. Für Einfamilienhäuser 2026 meist 1.200 bis 1.600 €. Seit 2023 ohne Mehrwertsteuer."),
    pvVerl: e("Ein Teil des Stroms geht im Wechselrichter, in den Kabeln, durch Wärme und Schmutz verloren, zusammen typisch 12 bis 15 %."),
    eeg: e("Was du für Strom bekommst, den du ins Netz schickst. Für neue Anlagen bis 10 kWp mit Eigenverbrauch 2026 rund 7,7 Cent. In Stunden mit negativem Börsenpreis gibt es nichts."),
    pvJahre: e("So lange rechnet der Rechner mit der Anlage. Module halten meist 25 bis 30 Jahre."),
    wpAn: e("Ob eine Wärmepumpe mitgerechnet wird. Dann heizt sie bevorzugt mit Solarstrom und in billigen Stunden.", WP),
    wpArt: e("Luft-Wasser-Wärmepumpen holen Wärme aus der Außenluft, Sole-Wasser-Wärmepumpen aus dem Erdreich, das ist teurer, im Winter aber effizienter."),
    waerme: e("Wie viel Wärme das Haus im Jahr braucht. Gasverbrauch in kWh mal 0,9 oder Liter Heizöl mal 9."),
    ww: e("Der Anteil für warmes Wasser. Für 3 bis 4 Personen rund 2.500 kWh."),
    vl: e("Wie heiß das Heizwasser an sehr kalten Tagen sein muss. Fußbodenheizung 35 °C, große Heizkörper 45 °C, alte kleine Heizkörper 55 °C oder mehr. Je niedriger, desto sparsamer die Wärmepumpe."),
    heizgr: e("Ab dieser Außentemperatur wird nicht mehr geheizt. Gut gedämmte Häuser 12 °C, ältere 15 °C."),
    puffer: e("Wie viel Wärme das Haus zwischenspeichern kann, im Pufferspeicher oder im Estrich der Fußbodenheizung. So kann die Wärmepumpe in billigen Stunden vorheizen."),
    evAn: e("Ob ein Elektroauto mitgerechnet wird. Es lädt dann vor allem mit Solarstrom und in billigen Stunden.", AUTO),
    km: e("Wie viele Kilometer das Auto im Jahr fährt."),
    evVerb: e("Strom auf 100 km. Im Winter rund 15 bis 25 % mehr als die Herstellerangabe."),
    evVerl: e("Beim Laden geht ein Teil als Wärme verloren, typisch 10 %."),
    evHaus: e("Wie viel du zu Hause lädst. Der Rest wird unterwegs teurer geladen."),
    evKw: e("Wie schnell die Wallbox lädt. 11 kW sind üblich, damit ist das Auto über Nacht voll."),
    evModus: e("Wann das Auto zu Hause steht und laden kann. Wer tagsüber daheim ist, kann mehr Solarstrom laden."),
    ab: e("Wann das Auto werktags morgens losfährt. Bis dahin soll es geladen sein."),
    an: e("Wann das Auto werktags wieder zu Hause ist."),
    batMod: e("Automatisch sucht der Rechner die Speichergröße, die sich am meisten lohnt. Du kannst auch selbst eine Größe festlegen."),
    batKwh: e("Wie viel Strom der Speicher fasst. Für ein Einfamilienhaus sind 5 bis 10 kWh üblich."),
    batFix: e("Was der Speicher unabhängig von der Größe kostet: Wechselrichter, Einbau, Anschluss."),
    batKwhKost: e("Was jede Kilowattstunde Speicher zusätzlich kostet. 2026 meist 300 bis 500 €."),
    batJahre: e("Wie lange der Speicher hält, meist 12 bis 15 Jahre."),
    batWg: e("Von 100 kWh, die in den Speicher gehen, kommen so viele wieder heraus. Typisch 90 %."),
    fest: e("Der Preis je kWh in einem normalen Stromvertrag mit festem Preis, mit allem."),
    netz: e("Was der Netzbetreiber für den Transport je kWh bekommt, ohne Mehrwertsteuer. Steht auf dem Preisblatt deines Netzbetreibers. Die Vorgabe gilt für die Syna in Idstein."),
    abg: e("Stromsteuer, Konzessionsabgabe und Umlagen je kWh, ohne Mehrwertsteuer. Das Buch schlägt vor, Stromsteuer und Umlagen zu senken.", STR),
    aufs: e("Was ein Anbieter mit dynamischem Tarif zusätzlich zum Börsenpreis verlangt, je kWh."),
    h8: e("Vorschlag aus dem Buch, heute noch kein Recht: In mindestens 8 Stunden am Tag, wenn viel Wind und Sonne im Netz sind, fällt das Netzentgelt weg. Wer dann lädt und heizt, spart.", MARKT),
    zins: e("Der Zins, den du für dein Geld sonst bekommen würdest, etwa auf einem Sparkonto. Damit werden die Kosten von PV und Speicher auf die Jahre verteilt."),
    steig: e("Wie stark der Strompreis jedes Jahr steigt. 2 % entsprechen etwa der Inflation."),
    aOff: e("Was eine kWh an öffentlichen Ladesäulen kostet."),
    aVerb: e("Liter Sprit auf 100 km bei einem vergleichbaren Verbrenner."),
    aSprit: e("Was ein Liter Sprit kostet."),
    gasKwh: e("Was eine kWh Gas heute kostet, zum Vergleich mit der Wärmepumpe."),
    gasNutz: e("Wie viel der Energie im Gas als Wärme ankommt, um 90 %."),
    gasGrund: e("Die feste Gebühr im Jahr für den Gasanschluss."),
    gasWart: e("Wartung und Schornsteinfeger im Jahr."),
  });
  Info.texte("#eing", {
    "Dein Ort": e("Mit deiner Postleitzahl lädt der Rechner ein typisches Wetterjahr für deinen Ort: Sonne, Temperatur und Luftfeuchte für jede Stunde. Ohne Postleitzahl rechnet er mit Idstein im Taunus."),
    "Haushalt": e("Der normale Strom im Haus, ohne Wärmepumpe und Auto."),
    "Photovoltaik": e("Solarmodule auf dem Dach machen aus Sonnenlicht Strom. Was du selbst nutzt, musst du nicht kaufen. Der Rest geht ins Netz.", STR),
    "Wärmepumpe": e("Heizt mit Strom aus der Umwelt. Läuft sie, wenn die Sonne scheint oder der Strom billig ist, sinken die Kosten.", WP),
    "E-Auto und Wallbox": e("Das Elektroauto ist ein großer Stromspeicher auf Rädern. Lädt es mittags mit Solarstrom oder nachts billig, spart es viel.", AUTO),
    "Batteriespeicher": e("Speichert Solarstrom vom Mittag für den Abend. Er lohnt sich nur, wenn die Ersparnis die Kosten in seiner Lebensdauer wieder hereinholt."),
    "Strompreise": e("Woraus sich der Strompreis zusammensetzt. Beim dynamischen Tarif ändert sich der Börsenpreis jede Stunde, Netzentgelt, Steuern und Aufschlag kommen dazu.", MARKT),
    "Wirtschaftlichkeit": e("Womit der Rechner Kosten auf die Jahre verteilt und wie die Preise steigen."),
  });
  const wrap = document.querySelector(".wrap") || document.body;
  Info.texte(wrap, {
    "Ergebnis": e("Der Rechner spielt ein ganzes Jahr Stunde für Stunde durch, für jeden Tarif mit und ohne PV und Speicher, und zeigt die günstigste Kombination. Mit „intelligenter Steuerung“ laden Auto und Wärmepumpe in Sonnen- und Billigstunden.", SIM),
    "Wirtschaftlichste Speichergröße": e("Für jede Speichergröße: Was sie im Jahr spart, gegen das, was sie im Jahr kostet. Der Punkt zeigt, wo der Abstand am größten ist."),
    "Strompreis je Verbraucher": e("Was eine kWh für Haushalt, Wärmepumpe und Wallbox im Schnitt kostet, aus PV und Netz gemischt. Wer flexibel ist, zahlt weniger."),
    "Eine Woche Stunde für Stunde": e("Eine Woche aus dem simulierten Jahr: wann die Sonne Strom liefert, wann der Speicher lädt, wann Auto und Wärmepumpe Strom ziehen und was er an der Börse kostet."),
    "Süd, Ost oder West?": e("Wie viel ein Kilowatt Peak je nach Dachseite im Jahr bringt, mit dem Wetter deines Orts."),
    "Die Formeln aus dem Vortrag": e("Die einfachen Faustformeln aus dem Vortrag „Strom clever managen“, mit deinen Zahlen ausgerechnet."),
    "E-Auto: Kosten je 100 km": e("Was 100 km mit dem Elektroauto kosten, wenn es so lädt wie in der Simulation, im Vergleich zum Verbrenner.", AUTO),
    "Wärmepumpe oder Gas": e("Was Heizen mit der Wärmepumpe im Jahr kostet, mit dem Strompreis aus der Simulation, gegen eine Gasheizung. Kauf, Förderung und CO₂-Preis rechnet der Rechner „Heizung und Dämmung“.", WP),
    "Wetterjahr": e("Das Wetter, mit dem gerechnet wird: ein typisches Jahr aus Messungen und Satellitendaten 2005 bis 2023, Stunde für Stunde."),
  });
  Info.texte("#mx", {
    "Festpreis": e("Ein normaler Stromvertrag: jede kWh kostet gleich viel."),
    "Dynamisch": e("Der Preis folgt jede Stunde der Strombörse. Mittags bei viel Sonne und nachts ist er oft niedrig, abends hoch.", MARKT),
    "+ § 14a": e("Dynamischer Tarif, dazu ein Netzentgelt, das je nach Uhrzeit wechselt. Das gibt es heute für steuerbare Wärmepumpen und Wallboxen (§ 14a, Modul 3)."),
    "Vorschlag: 8 h frei": e("Vorschlag aus dem Buch, kein geltendes Recht: 8 Stunden am Tag ohne Netzentgelt.", MARKT),
    "Ohne PV": e("Alles Strom aus dem Netz."),
    "Mit PV": e("Mit Solaranlage, ohne Speicher."),
    "PV + Speicher": e("Mit Solaranlage und Speicher in der Größe, die sich bei diesem Tarif am meisten lohnt."),
  });
  Info.texte("#tiles", {
    "Stromkosten im Jahr": e("Was du im Jahr für Strom bezahlst, Einspeisevergütung abgezogen, dazu Abschreibung und Zins für PV und Speicher."),
    "Ersparnis zu": e("Wie viel günstiger es ist als ganz ohne PV mit festem Stromtarif."),
    "Strom aus dem Netz": e("Wie viel Strom du trotzdem noch kaufst."),
    "Autarkie": e("Welcher Anteil deines Stroms aus eigener PV und Speicher kommt."),
    "Eigenverbrauch": e("Welcher Anteil des Solarstroms im Haus bleibt, statt ins Netz zu gehen."),
    "Einspeisung": e("Wie viel Solarstrom ins Netz geht und vergütet wird."),
  });
  Info.texte("#vp", {
    "kWh im Jahr": e("Wie viel Strom dieser Verbraucher im Jahr braucht."),
    "aus PV": e("Welcher Anteil davon aus der eigenen Solaranlage kommt."),
    "Kosten": e("Was dieser Strom im Jahr kostet."),
    "je kWh": e("Der Durchschnittspreis je kWh für diesen Verbraucher."),
  });
  Info.texte("#ot", {
    "kWh je kWp": e("Wie viel Strom ein Kilowatt Peak Module auf dieser Seite im Jahr liefert."),
    "im Vergleich zu Süd": e("Wie viel weniger es ist als auf der Südseite."),
    "meiste Leistung": e("Zu welcher Uhrzeit die Module im Juni am meisten liefern. Ost früh, West spät."),
  });
  Info.texte("#atiles", {
    "Strom an der Wallbox": e("Was eine kWh beim Laden zu Hause im Schnitt kostet, mit Solarstrom und billigen Stunden."),
    "E-Auto je 100 km": e("Was 100 km mit dem Elektroauto kosten, mit Laden zu Hause und unterwegs."),
    "Verbrenner je 100 km": e("Was 100 km mit dem Verbrenner kosten."),
    "Im Jahr gespart": e("Was du mit dem Elektroauto im Jahr an Energiekosten sparst. Kauf, Steuer und Werkstatt vergleicht der E-Auto-Rechner."),
  });
  Info.texte("#htiles", {
    "Jahresarbeitszahl": e("Wie viel Wärme die Wärmepumpe im Jahr aus einer kWh Strom macht, mit dem Wetter deines Orts."),
    "Strom für die Wärmepumpe": e("Wie viel Strom die Wärmepumpe im Jahr braucht."),
    "Wärmepumpe im Jahr": e("Was der Strom der Wärmepumpe im Jahr kostet."),
    "Gasheizung im Jahr": e("Was dieselbe Wärme mit Gas im Jahr kostet, mit Grundpreis und Wartung."),
  });
  Info.texte("#wtiles", {
    "Mitteltemperatur": e("Die mittlere Temperatur übers Jahr an deinem Ort."),
    "Sonneneinstrahlung": e("Wie viel Sonnenenergie im Jahr auf einen Quadratmeter waagrechte Fläche fällt."),
    "Luftfeuchte": e("Die mittlere Luftfeuchte. Sie bestimmt, wie oft die Luft-Wärmepumpe abtauen muss."),
    "Ertrag Süd": e("Was ein Kilowatt Peak je Dachseite im Jahr bringt."),
  });
})();
