# Mikrosimulation (Entwurf 0.1)

Rund 49.000 künstliche Haushalte mit Einkommen, Vermögen und Konsum, gerechnet mit dem Rechenkern des Steuerrechners.

- `python3 bevoelkerung.py` erzeugt `bevoelkerung.json` (fester Startwert, immer gleich).
- `node kern_bauen.js` zieht den Rechenkern aus `../steuerrechner/index.html` nach `kern.js`.
- `node lauf.js [annahmen.json] [ergebnis.json]` rechnet alles in rund 2 Sekunden. Annahmen überschreiben die Werte in `STANDARD` (simulation.js),
  z. B. `{"mpcMittelZiel": 1}` (alles Plus ausgegeben) oder `{"kuerzung": [1,0.8,0.5,0,0,0,0,0], "kuerzungLang": 0, "minusAusErbe": 1}`.
- `node zerlegung.js` zeigt, warum Haushalte weniger haben.
- `node seite/bauen.js` baut die bedienbare Seite, `node seite/test-seite.js` prüft sie im Browser.
- Annahmen und Quellen: `Annahmen.md`.
