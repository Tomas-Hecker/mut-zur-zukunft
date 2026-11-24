#!/usr/bin/env python3
"""Steuerrechner, Balken „Heute / Vorschlag“: Der Vorschlag zeigt die echten Beträge (Prämie der Krankenkasse, Mehrwertsteuer,
Ausgabensteuer). Was gegengerechnet wird (höhere Grundsicherung, ausgezahlte Arbeitgeberanteile, Ausgleich), liegt schraffiert
am Ende des Balkens und wird abgezogen; die Zahl links bleibt die Summe unterm Strich. Vorher wurde das Gegengerechnete anteilig
von allen Teilen abgezogen, dann sah es so aus, als sinke die Mehrwertsteuer. Im Vorschlag heißt „Sozialbeiträge“ jetzt „Prämie der
Krankenkasse“, weil Rente und Pflege aus der Steuer kommen. Läuft nach jedem Neubau (gen.py); ein zweiter Lauf ändert nichts."""
p = 'steuerrechner/index.html'
s = open(p, encoding='utf-8').read()
if 'seg-gut' in s:
    raise SystemExit
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:90]
    s = s.replace(a, b)
rep('''  const max = Math.max(r.sumH, r.sumV, 1);
  const bars = $("bars"); bars.innerHTML = "";
  const netto = o => { const n = { ...o }, ks = ["sv", "mwst", "ausg"], pos = ks.reduce((a, k) => a + Math.max(0, n[k]), 0), f = pos > 0 ? Math.max(0, pos + (o.gut || 0)) / pos : 0; for (const k of ks) n[k] = Math.max(0, n[k]) * f; n.gut = 0; return n; };   // Gegengerechnetes anteilig abziehen
  [["Heute", r.heute, r.sumH], ["Vorschlag", netto(r.vorschlag), r.sumV]].forEach(([lbl, o, s]) => {
    const row = document.createElement("div"); row.className = "barrow";
    row.innerHTML = `<div class="lbl">${lbl}<small>${eur(s)}</small></div>`;
    const tr = document.createElement("div"); tr.className = "track"; tr.style.width = (s / max * 100) + "%";
    tr.setAttribute("role", "img"); tr.setAttribute("aria-label", `${lbl}: ${eur(s)} Steuern und Abgaben im Jahr`);
    KAT.forEach(([k, name, col]) => {
      if (o[k] <= 0.5) return;''',
'''  const brutto = o => KAT.reduce((a, [k]) => a + Math.max(0, o[k] || 0), 0);
  const gutV = Math.max(0, -(r.vorschlag.gut || 0));   // was im Vorschlag gegengerechnet wird, als positiver Betrag
  const max = Math.max(brutto(r.heute), brutto(r.vorschlag), 1);
  const bars = $("bars"); bars.innerHTML = "";
  const katName = (k, name, lbl) => k === "sv" && lbl === "Vorschlag" && A.RVPVSt ? "Prämie der Krankenkasse" : name.replace(/ [(]im Vorschlag.*[)]$/, "");
  [["Heute", r.heute, r.sumH, 0], ["Vorschlag", r.vorschlag, r.sumV, gutV]].forEach(([lbl, o, s, gut]) => {
    const row = document.createElement("div"); row.className = "barrow";
    row.innerHTML = `<div class="lbl">${lbl}<small>${eur(s)}</small></div>`;
    const br = brutto(o), g = Math.min(gut, br);
    const tr = document.createElement("div"); tr.className = "track"; tr.style.width = (br / max * 100) + "%";
    tr.setAttribute("role", "img"); tr.setAttribute("aria-label", `${lbl}: ${eur(br)} Steuern und Abgaben${g > 0.5 ? `, davon ${eur(g)} ausgeglichen, unterm Strich ${eur(s)}` : ""} im Jahr`);
    if (g > 0.5) {
      const gs = document.createElement("div"); gs.className = "seg-gut"; gs.style.width = (g / br * 100) + "%";
      gs.onpointermove = e => showTip(e, `<b>Gleicht aus: ${eur(g)}</b><br>höhere Grundsicherung oder Rente, ausgezahlte Arbeitgeberanteile, Ausgleich. Unterm Strich bleiben ${eur(s)}.`); gs.onpointerleave = hideTip;
      tr.append(gs);
    }
    KAT.forEach(([k, name0, col]) => {
      const name = katName(k, name0, lbl);
      if (o[k] <= 0.5) return;''')
rep('''    sl.innerHTML = KAT.filter(([k]) => o[k] > 0.5).map(([k, n, c]) => `<span><i style="background:var(${c})"></i>${n} ${eur(o[k])}</span>`).join("");''',
    '''    sl.innerHTML = KAT.filter(([k]) => o[k] > 0.5).map(([k, n, c]) => `<span><i style="background:var(${c})"></i>${katName(k, n, lbl)} ${eur(o[k])}</span>`).join("")
      + (g > 0.5 ? `<span><i class="gut"></i>davon ausgeglichen −${eur(g)}, unterm Strich ${eur(s)}</span>` : "");''')
rep('''.seg { height: 100%; min-width: 0; }''', '''.seg { height: 100%; min-width: 0; }
.seg-gut { position: absolute; right: 0; top: 0; bottom: 0; z-index: 1; border-left: 2px solid var(--fg, #1d2321);
  background: repeating-linear-gradient(135deg, rgba(255,255,255,.78) 0 5px, rgba(255,255,255,.25) 5px 10px); }
.segl i.gut { background: repeating-linear-gradient(135deg, #fff 0 2px, #999 2px 4px); border: 1px solid var(--muted); }''')
rep('''  ["sv", "Sozialbeiträge und Krankenversicherung", "--s1"],''', '''  ["sv", "Sozialbeiträge und Krankenversicherung (im Vorschlag nur die Prämie der Krankenkasse)", "--s1"],''')
rep('''<b>Sozialbeiträge und Krankenkasse: ${eur(r.svNeu)}</b>''', '''<b>${A.RVPVSt ? "Prämie der Krankenkasse" : "Sozialbeiträge und Krankenkasse"}: ${eur(r.svNeu)}</b>''')
open(p, 'w', encoding='utf-8').write(s)
print('Balken mit echten Beträgen')
