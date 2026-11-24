"""Kleine Rechner auf „du“ (Entscheidung Tomas, 14.11.2026). Wiederholbar: übersprungen, wenn schon ersetzt."""
R = '/home/user/mut-zur-zukunft/'
E = {
 'balkon-rechner': [
  ('Sonne auf dem Balkon, Ihr Stromverbrauch zu jeder Tageszeit und, wenn Sie wollen,', 'Sonne auf dem Balkon, dein Stromverbrauch zu jeder Tageszeit und, wenn du willst,'),
  ('wie viel Strom Sie selbst nutzen, wie viel Sie sparen', 'wie viel Strom du selbst nutzt, wie viel du sparst'),
  ('Rechnen Sie im Zweifel mit etwas weniger Ersparnis.', 'Rechne im Zweifel mit etwas weniger Ersparnis.'),
  ('`Ihr Balkonkraftwerk liefert', '`Dein Balkonkraftwerk liefert'),
  ('Davon nutzen Sie <b>', 'Davon nutzt du <b>'),
  ('höchstens 800 W einspeisen, Ihr Wechselrichter hat', 'höchstens 800 W einspeisen, dein Wechselrichter hat'),
  ('${pct(deck)} Ihres Verbrauchs', '${pct(deck)} deines Verbrauchs'),
  ('auf Ihren Jahresverbrauch skaliert', 'auf deinen Jahresverbrauch skaliert'),
  ('Anmelden müssen Sie das Gerät nur', 'Anmelden musst du das Gerät nur'),
  ('aus Brandschutzgründen. Fragen Sie vorher.', 'aus Brandschutzgründen. Frag vorher.'),
 ],
 'eauto-rechner': [
  ('<h2>Dienstwagen: Ihre Steuer auf den geldwerten Vorteil</h2>', '<h2>Dienstwagen: deine Steuer auf den geldwerten Vorteil</h2>'),
  ('km sparen Sie <b>${eur(diff)}</b>.`;', 'km sparst du <b>${eur(diff)}</b>.`;', 2),
  ('row("Ihre Belastung im Monat"', 'row("Deine Belastung im Monat"'),
  ('Mit dem Elektroauto haben Sie über', 'Mit dem Elektroauto hast du über'),
  ('Beim Elektroauto zahlen Sie den Strom selbst;', 'Beim Elektroauto zahlst du den Strom selbst;'),
 ],
 'energie-rechner': [
  ('Tippen Sie auf ein Feld.', 'Tipp auf ein Feld.'),
  ('<h2>Die Formeln aus dem Vortrag, mit Ihren Zahlen</h2>', '<h2>Die Formeln aus dem Vortrag, mit deinen Zahlen</h2>'),
  ('Tragen Sie eine PV-Leistung ein, dann rechnet der Rechner die Formeln mit Ihren Zahlen.', 'Trag eine PV-Leistung ein, dann rechnet der Rechner die Formeln mit deinen Zahlen.'),
 ],
 'heizungsrechner': [
  ('<h3>Ihr Haus</h3>', '<h3>Dein Haus</h3>'),
 ],
}
for d, reps in E.items():
    p = R + d + '/index.html'; s = open(p).read()
    for r in reps:
        a, b = r[0], r[1]; n = r[2] if len(r) > 2 else 1
        c = s.count(a)
        if c == 0 and b in s: continue
        assert c == n, (d, a, c); s = s.replace(a, b)
    open(p, 'w').write(s)
print('du-form ok')
