# HeCoAir-Seite (hecoair.org)

Die Energie-Rechner erscheinen zusätzlich auf einer eigenen Seite der HeCoAir GmbH, im Erscheinungsbild der Firma
(wie die Planunterlagen, z. B. Pfarrhaus Niedernhausen). Die Rechner selbst bleiben nur hier im Repo; die HeCoAir-Seite
wird daraus gebaut.

- `ci/` Logo, Favicon, Schrift Barlow (lokal, OFL) und `hecoair.css` mit Farben und Kopf-/Fußzeile
- `impressum.html`, `datenschutz.html` Rechtstexte der GmbH (gelb markierte Stellen noch ergänzen)
- `../werkzeug/hecoair-seite.py` baut die Seite: `python3 werkzeug/hecoair-seite.py` → Ordner `_hecoair-seite/`

Hochladen: Inhalt von `_hecoair-seite/` per FTP oder Plesk-Dateimanager in das Hauptverzeichnis von hecoair.org.
Zugangsdaten gehören nicht ins Repo.

Farben: Dunkelgrün #36452a · Oliv #5c6e40 · Tinte #1f2419 · Papier #f6f7f1 · Linie #d5dbc3 · Gold #f2be4a · Orange #e9853a · Rost #ad5716
