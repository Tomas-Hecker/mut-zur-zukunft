#!/usr/bin/env python3
"""Tomas 28.11.2026 (über den Wärmepumpen-Thread und die Rechtsprüfung vom 28.11.): Sanierung im Mietshaus.
1. Ablösen nach Lebensdauer: Dämmung 50 Jahre, Fenster 40.
2. Einbau der Wärmepumpe, Heizkörper und Rohre im Mietshaus: zinsloser Kredit über 50 Jahre statt Anteil am Hauswert.
   Umgelegt wird die Tilgung der zinslosen Kredite, höchstens die Ersparnis des Mieters bei den Heizkosten; von der übrigen
   Ersparnis darf der Vermieter 30 Jahre lang die Hälfte aufschlagen; was zur gleichen Warmmiete fehlt, schreibt er gut.
3. Vergleich einmal bei der Umstellung, ausgehend von dem, was der Mieter nach dem Heizkostendeckel zahlt
   (Wärme × mittlerer Strompreis / 3, Teil darüber trägt der Vermieter 2028 zu einem Achtel, ab 2035 ganz),
   Grundpreis, Wartung, Zähler und Schornsteinfeger auf beiden Seiten.
4. Wärmepumpe: 30 Jahre, die ersten 3 ohne Tilgung, wie im Rechenmodell."""
import sys
P = 'steuerrechner/index.html'
s = open(P, encoding='utf-8').read()
if 'LaufH:' in s:
    print('schon drin'); sys.exit()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a)); s = s.replace(a, b)

# Konstanten
rep('MwStStrom: 0.05, MwStGas: 0.50, MwStDienst: 0.05, LaufT: 20, TilgFrei: 3, LaufB: 40, WpEinbau: 0.4,',
    'MwStStrom: 0.05, MwStGas: 0.50, MwStDienst: 0.05, LaufT: 33, TilgFrei: 3, LaufB: 50, LaufF: 40, LaufH: 50, HalbJ: 30, WpEinbau: 0.4,\n'
    '  // Betriebskosten im Jahr mit Mehrwertsteuer, je Haus und je Wohnung, eigene Schätzung: Gas oder Öl mit Grundpreis, Wartung und Schornsteinfeger; Wärmepumpe mit Zähler und Wartung\n'
    '  BkFossil: 300, BkFossilW: 45, BkWp: 200, BkWpW: 20, DeckelAb: 2027, DeckelJahre: 8,')
rep('const SAN_F = ["einb", "g",', 'const SAN_F = ["jahr", "pm", "einb", "g",')
rep('const SAN_STD = { lang: 20, kuehl: 0,', 'const SAN_STD = { jahr: 2028, pm: 28, lang: 33, kuehl: 0,')

# Rechnung
a0 = s.index('  // heute: § 559 (8 %), § 559e (10 % mit Förderung)')
a1 = s.index('function sanLese() {')
neu = r'''  // heute: § 559 (8 %), § 559e (10 % mit Förderung), Heizung höchstens 0,50 € je m², alles höchstens 3 € (2 €) je m²
  const satzT = ZT > 0 ? SAN.UmlageHz : SAN.Umlage;
  const uT = Math.min(satzT * Math.max(0, hz * (1 - erh) - ZT), deckelHz);
  const uB = SAN.Umlage * Math.max(0, hue * (1 - erh) - ZB);
  const uH = Math.min(uT + uB, deckel);
  // Energie
  const wp = v.mWp && tech > 0;
  const kwhStrom = wp ? fl * v.nach / Math.max(1, v.jaz) : 0, kwhGas = wp ? 0 : fl * v.nach / SAN.Kessel;
  const fS = (1 + SAN.MwStStrom) / (1 + m), fG = (1 + SAN.MwStGas) / (1 + m);
  const e0 = fl * v.vor * v.pg / 100, e0R = e0 * fG;
  // CO₂-Kostenaufteilung (CO2KostAufG): Anteil des Vermieters nach kg CO₂ je m², heute mit 19 %, in der Reform mit 50 % Mehrwertsteuer
  const ef = SAN.EF[v.trg] || SAN.EF.gas;
  const co2V = kwh => { const kg = kwh * ef / fl, q = SAN.CO2Stufen.find(([g]) => kg < g)[1]; return q * kwh * ef / 1000 * SAN.CO2Preis * (1 + m); };
  const c0 = co2V(fl * v.vor), cS = co2V(kwhGas);
  const bk0 = SAN.BkFossil + SAN.BkFossilW * n, bk1 = wp ? SAN.BkWp + SAN.BkWpW * n : bk0, bkR = x => x / (1 + m) * (1 + SAN.MwStDienst);
  const eH = kwhStrom * v.ps / 100 + kwhGas * v.pg / 100;
  const eR = kwhStrom * v.ps / 100 * fS + kwhGas * v.pg / 100 * fG;
  // Reform: Deckel für die Heizkosten. Der Mieter zahlt für die Wärme höchstens Wärme × mittlerer Strompreis / 3 (hier der Wärmepumpentarif mit 5 %);
  // pm: mittlerer Strompreis aller Haushalte, amtlich festgestellt; den Teil darüber trägt bei der bestehenden Heizung der Vermieter, 2028 ein Achtel, ab 2035 ganz
  const jahr = clamp(Math.round(v.jahr || 2028), 2028, 2070), qJ = j => v.ausn ? 0 : clamp((j - SAN.DeckelAb) / SAN.DeckelJahre, 0, 1);   // Ausnahme: Denkmal, Anschlusszwang, Wärmenetzgebiet, Eigentümergemeinschaft
  const pm = (v.pm || 28) / 100, cap0 = fl * v.vor * SAN.Kessel * pm / 3, cap1 = fl * v.nach * pm / 3;
  const mE0 = e0R - c0 * fG, ue0 = Math.max(0, mE0 - cap0), mE1 = eR - cS * fG, ue1 = wp ? 0 : Math.max(0, mE1 - cap1);
  // Vergleich einmal bei der Umstellung: was der Mieter vorher nach dem Deckel zahlt und was danach, jeweils mit Grundpreis, Wartung und Zählern
  const q0 = qJ(jahr), vorM = mE0 - q0 * ue0 + bkR(bk0), nachM = mE1 - q0 * ue1 + bkR(bk1), S = vorM - nachM;
  // Reform: Wärmepumpe zinslos über 30 Jahre, die ersten 3 ohne Tilgung; Einbau, Heizkörper und Rohre im Mietshaus zinslos über 50 Jahre;
  // Fenster und Dämmung als Anteil am Hauswert, abgelöst nach der Lebensdauer (Fenster 40, Dämmung 50 Jahre)
  const mix = mat + (1 - mat) * (1 + SAN.MwStDienst);
  const eb = clamp(v.einb / 100, 0, 1), Tn = tech * (1 - eb) / (1 + m), Hn = (tech * eb + hk) / (1 + m), Fn = 0;
  const BnF = fen / (1 + m) * mix, BnB = bau / (1 + m) * mix, Bn = BnF + BnB;
  const LT = [33, 43].includes(v.lang) ? v.lang : SAN.LaufT, tilgT = Tn / (LT - SAN.TilgFrei), tilgH = Hn / SAN.LaufH, tilgF = 0;
  const ablJ = BnF / SAN.LaufF + BnB / SAN.LaufB, uBr = v.abl ? ablJ * (1 - erh) : 0;
  const anteil = v.wert > 0 ? Bn / v.wert : 0;
  // Bank heute: Annuität über 20 Jahre
  const K = Math.max(0, hz + hue - ZT - ZB), i = v.zins / 100;
  const ann = K > 0 ? (i > 0 ? K * i / (1 - Math.pow(1 + i, -J)) : K / J) : 0;
  // Aufteilung (Tomas 28.11.2026): Mieter und Vermieter gewinnen gleich viel. Der Vermieter schlägt einen festen Betrag im Jahr auf,
  // so dass im Schnitt der 20 Jahre beide gleich viel gegenüber dem Haus gewinnen, das mit der Reform bei der alten Heizung bleibt;
  // höchstens die Ersparnis des Mieters bei der Umstellung, die Warmmiete steigt also nie; was dazu fehlt, schreibt er gut
  const basis = []; let zinsR = 0, restT = Tn, restH = Hn;
  for (let t = 1; t <= J; t++) {
    const q = qJ(jahr + t - 1), tT = t > SAN.TilgFrei && restT > 1e-6 ? tilgT : 0, tH = restH > 1e-6 ? tilgH : 0;
    zinsR += (restT + restH) * A.ZinsStart; restT -= tT; restH -= tH;
    const eT = mE1 - q * ue1, w0R = km + mE0 - q * ue0 + bkR(bk0), abl = v.abl ? ablJ * Math.pow(1 + w, t) : 0;
    const spart = w0R - (km + eT + bkR(bk1)), vOhne = -tT - tH - abl + (c0 - cS) * fG + q * (ue0 - ue1);
    basis.push({ t, q, tT, tH, eT, w0R, abl, spart, vOhne });
  }
  const mw = k => basis.reduce((a, b) => a + b[k], 0) / J;
  const gut = Math.max(0, -S), gleich = (mw("spart") - mw("vOhne")) / 2;
  // negativ: der Vermieter gewinnt schon ohne Aufschlag mehr (Deckel, CO₂-Anteil), dann schreibt er dem Mieter den Unterschied gut
  const U = Math.min(gleich, Math.max(0, S), deckel);
  const rows = basis.map(b => {
    const umlR = U;
    return { t: b.t, w0: km + e0 - c0 + bk0, w0R: b.w0R, wH: km + uH + eH - cS + bk1, wR: km + umlR + b.eT + bkR(bk1) - gut, umlR, gut, eT: b.eT, tilg: b.tT + b.tH,
      vH: uH - ann + c0 - cS, vR: umlR - gut + b.vOhne, abl: b.abl };
  });
  const sum = k => rows.reduce((a, r) => a + r[k], 0);
  const mwstH = (hz + hue) * m / (1 + m), mwstR = (fen + bau) / (1 + m) * (1 - mat) * SAN.MwStDienst;
  return { LT, c0, cS, fG, w0R: sum("w0R") / J, n, fl, km, tech, hk, fen, bau, ZT, ZB, uT, uB, uH, satzT, deckel, e0, e0R, eH, eR, kwhStrom, kwhGas, Tn, Hn, Fn, Bn, BnF, BnB, tilgT, tilgH, tilgF, uBr, anteil, K, ann, zinsR, rows, sum, wp,
    jahr, S, U, gleich, q0, ue0, mE0, bk0, bk1, bkR,
    mwstH, mwstR, mwstStromH: kwhStrom * v.ps / 100 * m / (1 + m), mwstStromR: kwhStrom * v.ps / 100 * fS * SAN.MwStStrom / (1 + SAN.MwStStrom),
    staatH: mwstH - ZT - ZB, staatR: mwstR - zinsR, anteilJ: Bn * Math.pow(1 + w, J), ablSum: sum("abl") };
}

'''
s = s[:a0] + neu + s[a1:]
# Lesen und Setzen
rep('v.lang = +$("s_lang").value || 20;', 'v.lang = +$("s_lang").value || SAN.LaufT; v.ausn = $("s_ausn").checked ? 1 : 0;')
rep('["einb", "g", "n", "fl", "miete", "wert", "pg", "ps", "zt", "zb", "mat", "erh", "zins", "wst"].forEach(k => $("s_" + k).value = v[k]);',
    '["jahr", "pm", "einb", "g", "n", "fl", "miete", "wert", "pg", "ps", "zt", "zb", "mat", "erh", "zins", "wst"].forEach(k => $("s_" + k).value = v[k]);')
rep('$("s_lang").value = String(v.lang || 20);', '$("s_lang").value = String(v.lang || SAN.LaufT); $("s_ausn").checked = !!v.ausn;')
rep('v: { bj: 1918, g: 2, n: 4, fl: 400, miete: 8, wert: 1000000, trg: "gas", pg: 12, einb: 0,', 'v: { bj: 1918, g: 2, n: 4, fl: 400, miete: 8, wert: 1000000, trg: "gas", pg: 12, einb: 0, ausn: 1,')

# Eingaben
rep('<span class="hint">zinsloser Kredit, Laufzeit unten; der Einbau, rund 40 %, zählt zum Anteil am Hauswert</span>',
    '<span class="hint">zinsloser Kredit über 30 Jahre, die ersten 3 ohne Tilgung; der Einbau, rund 40 %, zinslos über 50 Jahre</span>')
rep('<label for="s_hk">Größere Heizkörper und Rohre</label><input id="s_hk" type="number" min="0" step="1000"><span class="hint">Bauteil, Anteil am Hauswert</span>',
    '<label for="s_hk">Größere Heizkörper und Rohre</label><input id="s_hk" type="number" min="0" step="1000"><span class="hint">im Mietshaus zinsloser Kredit über 50 Jahre</span>')
rep('<label for="s_fen">Neue Fenster</label><input id="s_fen" type="number" min="0" step="1000"><span class="hint">Bauteil, Anteil am Hauswert</span>',
    '<label for="s_fen">Neue Fenster</label><input id="s_fen" type="number" min="0" step="1000"><span class="hint">Bauteil, Anteil am Hauswert, abgelöst über 40 Jahre</span>')
rep('<label for="s_bau">Dämmung</label><input id="s_bau" type="number" min="0" step="1000"><span class="hint">Bauteil, Anteil am Hauswert</span>',
    '<label for="s_bau">Dämmung</label><input id="s_bau" type="number" min="0" step="1000"><span class="hint">Bauteil, Anteil am Hauswert, abgelöst über 50 Jahre</span>')
rep('<span class="hint">zählt in der Reform zu den Bauteilen</span>', '<span class="hint">im Mietshaus mit Heizkörpern und Rohren zinslos über 50 Jahre</span>')
rep('<summary>Weitere Angaben: Zuschuss, Zinsen, Erhaltung, Ablösen</summary>\n          <div class="fields">',
    '<summary>Weitere Angaben: Jahr, Zuschuss, Zinsen, Erhaltung, Ablösen</summary>\n          <div class="fields">\n'
    '          <div class="field"><label for="s_jahr">Jahr der Umstellung</label><input id="s_jahr" type="number" min="2028" max="2070" step="1"><span class="hint">Deckel für die Heizkosten: über dem Deckel trägt der Vermieter 2028 ein Achtel, ab 2035 alles</span></div>\n'
    '          <div class="field"><label for="s_pm">Mittlerer Strompreis aller Haushalte, Cent je kWh</label><input id="s_pm" type="number" min="0" step="0.5"><span class="hint">für den Deckel: Wärme mal diesem Preis, geteilt durch 3; kommt jedes Jahr aus der amtlichen Statistik</span></div>\n'
    '          <label class="check field wide"><input id="s_ausn" type="checkbox"> Ausnahme vom Deckel: Der Vermieter kann rechtlich oder tatsächlich nicht wechseln, etwa im Denkmal, bei Anschlusszwang für Fernwärme oder wenn die Eigentümergemeinschaft entscheidet</label>')
a0 = s.index('<select id="s_lang">'); a1 = s.index('</select>', a0)
s = s[:a0] + '<select id="s_lang"><option value="33">30 Jahre, die ersten 3 ohne Tilgung</option><option value="43">40 Jahre, die ersten 3 ohne Tilgung: Auslegung auf 40 Jahre nachgewiesen, 2 Jahre überwacht</option>' + s[a1:]
rep('<input id="s_abl" type="checkbox"> Vermieter löst den Anteil am Hauswert über 40 Jahre ab (dann darf die Miete um ein Vierzigstel des Betrags im Jahr steigen)',
    '<input id="s_abl" type="checkbox"> Vermieter löst den Anteil am Hauswert ab, Dämmung über 50 Jahre, Fenster über 40 (dann darf die Miete um ein Fünfzigstel, bei Fenstern ein Vierzigstel des Betrags im Jahr steigen)')

# Ausgabe
rep('''+ z(`Heizen und Warmwasser${r.wp ? "" : " mit " + traeger}${r.c0 > 0 ? "<small>ohne den CO₂-Anteil, den der Vermieter trägt</small>" : ""}`, sEur((r.e0 - r.c0) / M), sEur((r.eH - r.cS) / M), sEur((r.eR - r.cS * r.fG) / M), sEur((r.eR - r.cS * r.fG) / M))''',
    '''+ z(`Heizen und Warmwasser${r.wp ? "" : " mit " + traeger}${r.c0 > 0 ? "<small>ohne den CO₂-Anteil, den der Vermieter trägt; mit der Reform nach dem Deckel</small>" : ""}`, sEur((r.e0 - r.c0) / M), sEur((r.eH - r.cS) / M), sEur(r1.eT / M), sEur(r4.eT / M))
    + z(`Grundpreis, Wartung, Zähler, Schornsteinfeger`, sEur(r.bk0 / M), sEur(r.bk1 / M), sEur(r.bkR(r.bk1) / M), sEur(r.bkR(r.bk1) / M))
    + (r1.gut > 0 ? z("Gutschrift des Vermieters<small>damit die Warmmiete nicht steigt</small>", "", "", sEur(-r1.gut / M), sEur(-r4.gut / M)) : "")''')
rep('''r.uBr > 0 ? `Aufschlag sinkt auf ${sPlus(r.uBr / M)} bis Jahr 40` : r.LT > 20 ? `Aufschlag läuft bis Jahr ${r.LT}, dann entfällt er` : "Aufschlag entfällt")''',
    '''r1.umlR > 0 ? `Aufschlag bleibt gleich, solange die zinslosen Kredite laufen${r.Hn > 0 ? " (bis Jahr " + SAN.LaufH + ")" : r.Tn > 0 ? " (bis Jahr " + r.LT + ")" : ""}` : "kein Aufschlag")''')
rep('Nach 20 Jahren ist die Wärmepumpe bezahlt: Nach heutigem Recht bleibt der Aufschlag, mit der Reform entfällt er.`;',
    'Nach heutigem Recht bleibt der Aufschlag auf Dauer. Mit der Reform schlägt der Vermieter einen festen Betrag auf, so dass Mieter und Vermieter gleich viel gewinnen, höchstens die Ersparnis des Mieters bei den Heizkosten, verglichen einmal bei der Umstellung ${r.jahr} mit Deckel, Grundpreis und Wartung.`;')
rep('''const kred = r.Tn > 0 ? `Wärmepumpe ${sEur(r.Tn)} über ${r.LT} Jahre` : "";''',
    '''const kred = [r.Tn > 0 ? `Wärmepumpe ${sEur(r.Tn)} über ${r.LT - SAN.TilgFrei} Jahre nach ${SAN.TilgFrei} ohne Tilgung` : "", r.Hn > 0 ? `Einbau, Heizkörper und Rohre ${sEur(r.Hn)} über ${SAN.LaufH} Jahre` : ""].filter(Boolean).join(", ");''')
rep('''[r.tech > 0 ? "Einbau der Wärmepumpe" : "", r.hk > 0 ? "Heizkörper und Rohre" : "", r.fen > 0 ? "Fenster" : "", r.bau > 0 ? "Dämmung" : ""]''',
    '''[r.fen > 0 ? "Fenster" : "", r.bau > 0 ? "Dämmung" : ""]''')
rep('''`${sPlus(r1.umlR)} in Jahr 1 bis ${SAN.TilgFrei}<small>${sPlus(r4.umlR)} ab Jahr ${SAN.TilgFrei + 1}: genau die Tilgung</small>`''',
    '''`${sPlus(r1.umlR)} jedes Jahr<small>so viel, dass Mieter und Vermieter gleich viel gewinnen, höchstens die Ersparnis der Mieter bei der Umstellung (${sPlus(r.S)} im Jahr); ist er negativ, schreibt der Vermieter ihn gut${r1.gut > 0 ? `; Gutschrift ${sEur(r1.gut)} im Jahr` : ""}${r.q0 > 0 && r.ue0 > 0 ? `; über dem Deckel trug er bei der Umstellung ${pct(r.q0, 0)}, ab 2035 alles; was er davon durch die Sanierung spart, gehört ihm` : ""}</small>`''')
rep('''`über 40 Jahre abgelöst, in 20 Jahren rund ${sEur(r.ablSum)} zurück`''', '''`abgelöst, Dämmung über ${SAN.LaufB} Jahre, Fenster über ${SAN.LaufF}, in 20 Jahren rund ${sEur(r.ablSum)} zurück`''')
rep('Reform: Die Wärmepumpe ohne Einbau bezahlt der zinslose Kredit, rund 40 % für Einbau, Rohre und Leitungen zählen wie Heizkörper, Fenster und Dämmung zum Anteil am Hauswert. Umgelegt wird die ganze Tilgung, die Grenze von 0,50 € je m² für Heizungen entfällt, die von 3 € je m² gilt weiter.',
    'Reform: Die Wärmepumpe ohne Einbau bezahlt ein zinsloser Kredit über 30 Jahre, die ersten 3 ohne Tilgung. Rund 40 % für Einbau, Rohre und Leitungen und die Heizkörper laufen im Mietshaus über einen zinslosen Kredit über 50 Jahre, Fenster und Dämmung über den Anteil am Hauswert. Der Vermieter schlägt einen festen Betrag auf, so dass Mieter und Vermieter im Schnitt der 20 Jahre gleich viel gewinnen, gegenüber dem Haus, das mit der Reform bei der alten Heizung bleibt; Tilgung, Ablösen, CO₂-Anteil und Deckel sind darin gezählt. Höchstens schlägt er die Ersparnis des Mieters auf, die Warmmiete steigt also nie, und was zur gleichen Warmmiete fehlt, schreibt er gut. Gewinnt der Vermieter schon ohne Aufschlag mehr, etwa weil er den Teil über dem Deckel nicht mehr trägt, schreibt er dem Mieter den Unterschied gut. Verglichen wird einmal bei der Umstellung, ausgehend von dem, was der Mieter nach dem Deckel für die Heizkosten zahlt (Wärme × mittlerer Strompreis aller Haushalte / 3, jedes Jahr amtlich festgestellt), mit Grundpreis, Wartung, Zähler und Schornsteinfeger auf beiden Seiten (geschätzt im Jahr ${eur(SAN.BkFossil)} und ${eur(SAN.BkFossilW)} je Wohnung mit ${traeger}, ${eur(SAN.BkWp)} und ${eur(SAN.BkWpW)} je Wohnung mit Wärmepumpe). Die Grenze von 0,50 € je m² für Heizungen entfällt, die von 3 € je m² gilt weiter.')
rep('''[r.Tn > 0 ? "Wärmepumpe bezahlt, ihr Aufschlag entfällt" : "", ""].filter(Boolean).join("; ") || "–"''',
    '''(r.Tn + r.Hn > 0 ? `Die zinslosen Kredite laufen weiter, ${r.Tn > 0 ? "für die Wärmepumpe bis Jahr " + r.LT : ""}${r.Tn > 0 && r.Hn > 0 ? ", " : ""}${r.Hn > 0 ? "für Heizkörper und Rohre bis Jahr " + SAN.LaufH : ""}; der Aufschlag endet mit der Tilgung` : "–")''')
open(P, 'w', encoding='utf-8').write(s); print('ok')
