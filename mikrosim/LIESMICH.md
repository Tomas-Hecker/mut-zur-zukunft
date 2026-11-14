# Mikrosimulation (Entwurf 0.2)

Rund 49.000 künstliche Haushalte mit Einkommen, Vermögen und Konsum, gerechnet mit dem Rechenkern des Steuerrechners.

- `python3 bevoelkerung.py` erzeugt `bevoelkerung.json` (fester Startwert, immer gleich), Löhne geeicht auf die VGR 2025.
- `node eichen.js` eicht danach die Abzüge in der Einkommensteuer auf das Aufkommen 2025 (schreibt die Spalte `abzug`).
- `node eichen_sparen.js` zeigt die Eichung der Sparquoten nach Gruppen auf die EVS (Werte stehen in `STANDARD`).
- `node abgleich.js` schreibt `abgleich.md`: jede Summe des Modells neben der amtlichen Zahl.
- `node kern_bauen.js` zieht den Rechenkern aus `../steuerrechner/index.html` nach `kern.js`.
- `node lauf.js [annahmen.json] [ergebnis.json]` rechnet alles in rund 2 Sekunden. Annahmen überschreiben die Werte in `STANDARD` (simulation.js),
  z. B. `{"mpcMittelZiel": 1}` (alles Plus ausgegeben) oder `{"kuerzung": [1,0.8,0.5,0,0,0,0,0], "kuerzungLang": 0, "minusAusErbe": 1}`.
- `node zerlegung.js` zeigt, warum Haushalte weniger haben.
- `node ausgleich.js` rechnet die Ausgleichsvarianten, `node uebergabe.js` schreibt `uebergabe-buch.json` für das Buch-Rechenmodell.
- `node spanne.js` rechnet die ehrliche Spanne der Haushalte mit weniger (andere Eichungen, ohne und mit Ausgleich) nach `spanne.json`.
- `node steuerlast.js [ohne] [haus]` schreibt `steuerlast.json` für die Grafiken in `steuerlast/` (Standard: Wahl von Version 32 ohne Hausregel im ersten Jahr).
- `node seite/bauen.js` baut die bedienbare Seite, `node seite/test-seite.js` prüft sie im Browser.
- Annahmen und Quellen: `Annahmen.md`.
