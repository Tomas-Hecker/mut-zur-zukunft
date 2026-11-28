"""Rechtsprüfung 28.11.2026 (Abschnitt 10) im Sanierungsrechner:
1. keine doppelte Gutschrift: A = min(gleich, S, Deckel), negatives A ist die Gutschrift
2. Erhaltung: in der Reform 15 % der Raten für Wärmepumpe und Heizkörper nicht umlegbar (§ 559 Abs. 2, § 559e Abs. 2)
3. Ablösen mit dem ursprünglichen Betrag (1/50, 1/40), nicht mit dem Hauswert"""
p = 'steuerrechner/index.html'; s = open(p, encoding='utf-8').read()
if 'ErhReform' in s: raise SystemExit('schon eingespielt')
R = [
 ("DeckelAb: 2027, DeckelJahre: 8,", "DeckelAb: 2027, DeckelJahre: 8, ErhReform: 0.15,"),
 ("abl = v.abl ? ablJ * Math.pow(1 + w, t) : 0;", "abl = v.abl ? ablJ : 0;   // ursprünglicher Betrag, in heutigem Geld gleich"),
 ("const spart = w0R - (km + eT + bkR(bk1)), vOhne = -tT - tH - abl + (c0 - cS) * fG + q * (ue0 - ue1);\n    basis.push({ t, q, tT, tH, eT, w0R, abl, spart, vOhne });",
  "const spart = w0R - (km + eT + bkR(bk1)), vOhne = -tT - tH - abl + (c0 - cS) * fG + q * (ue0 - ue1);\n    const vTeil = vOhne + SAN.ErhReform * (tT + tH);   // Erhaltung: 15 % der Raten hätte der Vermieter auch bei der alten Heizung bezahlt\n    basis.push({ t, q, tT, tH, eT, w0R, abl, spart, vOhne, vTeil });"),
 ("const gut = Math.max(0, -S), gleich = (mw(\"spart\") - mw(\"vOhne\")) / 2;", "const gleich = (mw(\"spart\") - mw(\"vTeil\")) / 2;"),
 ("const U = Math.min(gleich, Math.max(0, S), deckel);", "const A0 = Math.min(gleich, S, deckel), U = Math.max(0, A0), gut = Math.max(0, -A0);"),
 ("(dann darf die Miete um ein Fünfzigstel, bei Fenstern ein Vierzigstel des Betrags im Jahr steigen)", "(jedes Jahr ein Fünfzigstel, bei Fenstern ein Vierzigstel des ursprünglichen Betrags; es zählt bei der Aufteilung mit)"),
  ("(${sPlus(r.S)} im Jahr); ist er negativ, schreibt der Vermieter ihn gut${", "(${sPlus(r.S)} im Jahr); 15 % der Raten zählen als Erhaltung, die bei der alten Heizung ohnehin angefallen wäre; fehlt dem Mieter etwas, schreibt der Vermieter es gut${"),
 ('<span class="hint">was ohnehin fällig war, darf nicht auf die Miete</span>', '<span class="hint">heutiges Recht: was ohnehin fällig war, darf nicht auf die Miete; in der Reform pauschal 15 % der Raten</span>'),
  ("vR: umlR - gut + b.vOhne, abl: b.abl };", "vR: umlR - gut + b.vTeil, abl: b.abl };   // die Erhaltung hätte er bei der alten Heizung auch bezahlt"),
  ("Von der Ersparnis, die danach übrig bleibt, darf der Vermieter 30 Jahre lang die Hälfte aufschlagen, die Warmmiete steigt also nicht, solange der Staat seinen Anteil hält.",
   "Nach dem Umbau auf die Wärmepumpe schlägt der Vermieter einen festen Betrag auf die Miete, so hoch, dass er und der Mieter im Schnitt der ersten 20 Jahre gleich viel gewinnen, höchstens die Ersparnis des Mieters bei der Umstellung; gewinnt er schon ohne Aufschlag mehr, schreibt er ihm die Hälfte des Unterschieds gut. Der Aufschlag steigt höchstens wie die Verbraucherpreise und läuft, solange die zinslosen Kredite laufen, höchstens 50 Jahre."),
]
for a, b in R:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s); print('ok')
