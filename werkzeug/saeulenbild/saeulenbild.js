/* Säulenbild für den Steuerrechner: „Brutto, Abzüge und was im Portemonnaie bleibt“ (Stand 16.11.2026, von Tomas freigegeben: eine Säule je Seite).
   sbDaten(h, r, p)     macht aus den Eingaben h und dem Ergebnis r = haushalt(h) die Werte der beiden Säulen, alles in € im Jahr.
                        p.kst: Satz der Körperschaftsteuer mit Soli (A.KStS, Standard 0,15825), nur für Haushalte mit GmbH.
   sbZeichnen(el, d, o) zeichnet Titel, Info-Knopf, Schalter „im Monat / im Jahr“, die zwei Säulen und die Tabelle in das Element el.
                        o.praemieMonat: Prämie der Krankenkasse für den Infotext (Standard 50); o.nachWechsel: Funktion, die nach dem Umschalten Monat/Jahr läuft.
                        o.invest.setze(q): läuft, wenn der Schieber „Investitionsquote“ bewegt wird (nur bei GmbH). q ist der Anteil des Gewinns, der im
                        Unternehmen bleibt (0 bis 1 − p.kst). Die Seite setzt dann die Ausschüttung auf Gewinn × (1 − p.kst − q) und rechnet neu.
   sbAenderung(el, d)   zeichnet die Balken „Was sich ändert“ (rechts mehr Geld, links weniger).
   Gerechnet wird bei gleichem Einkauf wie heute: bleibt(Reform) − bleibt(heute) = r.vgl + r.entfall, die Zahl im Kopf des Rechners.
   Der Arbeitgeberanteil (und bei Rentnern der Anteil der Rentenkasse an der Krankenkasse) steht in der Säule „Heute“ schraffiert über dem Brutto:
   Er wird heute am Lohnzettel vorbei an die Sozialkassen gezahlt und in der Reform ausgezahlt. So sind beide Säulen vergleichbar.
   GmbH (16.11.2026, Wunsch von Tomas): Was vom Gewinn im Unternehmen bleibt und investiert wird, steht als eigenes Feld über „Bleibt im Portemonnaie“.
   Es ist in beiden Säulen gleich groß: Gewinn − Körperschaftsteuer − Ausschüttung von heute. Der Unterschied der Säulen liegt so ganz im Portemonnaie. */
const SB = { teiler: 12, info: false, tip: null, wieder: null, nach: null, invest: null, nr: 0 };
const SB_FELD = { "sb-bleibt": ["Bleibt im<br>Portemonnaie", "Bleibt"], "sb-firma": ["Bleibt im<br>Unternehmen", "Firma"] };
// Abzüge, von unten nach oben über dem Feld „Bleibt“: Schlüssel, Name heute, Name in der Reform (falls anders), Farbe, Schriftfarbe
const SB_ABZ = [
  ["unterhalt", "Unterhalt für Kinder in Ausbildung", null, "--sb-u", "--sb-on-u"],
  ["mwst", "Mehrwertsteuer", null, "--s4", "--sb-on-s4"],
  ["ausg", "Ausgabensteuer (neu)", null, "--s5", "--sb-on-s5"],
  ["sv", "Sozialbeiträge und Krankenversicherung", "Prämie der Krankenkasse", "--s1", "--sb-on-s1"],
  ["est", "Einkommensteuer und Soli", null, "--s2", "--sb-on-s2"],
  ["kap", "Steuern auf Kapital und Gewinne", null, "--s3", "--sb-on-s3"],
];
const SB_DIREKT = {
  ag: ["Arbeitgeberanteile", "Zahlt der Betrieb heute zusätzlich zum Brutto direkt an die Sozialkassen. In der Reform werden sie als Lohn ausgezahlt.", "heute direkt an die Sozialkassen, in der Reform als Lohn ausgezahlt", "Arbeitgeberanteile, als Lohn ausgezahlt"],
  rente: ["Anteil der Rentenkasse an der Krankenkasse", "Zahlt die Rentenkasse heute zusätzlich zur Rente direkt an die Krankenkasse. In der Reform wird er als Rente ausgezahlt.", "heute direkt an die Krankenkasse, in der Reform als Rente ausgezahlt", "Anteil der Rentenkasse, als Rente ausgezahlt"],
};
const SB_NEU = { gs: "Höhere Grundsicherung", bsz: "Bestandsschutz für heutige Rentner", ausgl: "Ausgleich", rpz: "Zuschlag zur Rente: Sie kauft 2 % mehr" };
const sbSum = o => Object.values(o || {}).reduce((a, x) => a + x, 0);

function sbDaten(h, r, p = {}) {
  const brutto = r.einkommen + (h.verm || 0);                      // alles, was hereinkommt, samt Entnahme aus Erspartem
  const mitU = r.entfall > 0.5;                                    // Unterhalt für Kinder in Ausbildung nur zeigen, wenn er sich ändert
  const direkt = { ag: r.ausSum + r.agRP, rente: r.rentePlus };    // heute am Brutto vorbei gezahlt, in der Reform ausgezahlt
  const neu = { gs: r.gsPlus, bsz: r.bsz || 0, ausgl: (r.ausgB || 0) + (r.ausgR || 0), rpz: r.rpz || 0 };   // kommt in der Reform vom Staat dazu; rpz = Rentenzuschlag ab Rechenkern V35 (dort sind ausgB und ausgR 0)
  const heute = { brutto, direkt, abz: { sv: r.heute.sv, est: r.heute.est, kap: r.heute.kap, mwst: r.heute.mwst, unterhalt: mitU ? r.unterhalt : 0 } };
  // Der Bestandsschutz für heutige Rentner erlässt Ausgabensteuer: Er wird dort abgezogen; nur was darüber hinausgeht, zählt als Geld vom Staat
  const ausg0 = r.ausgUeb + r.atg - r.anr, bszAbzug = Math.min(neu.bsz, Math.max(0, ausg0)); neu.bsz -= bszAbzug;
  const reform = { brutto: brutto + sbSum(direkt) + sbSum(neu), direkt, neu, bszAbzug,
    abz: { sv: r.svNeu, mwst: r.mwst + r.pw, ausg: ausg0 - bszAbzug, unterhalt: mitU ? r.unterhalt - r.entfall : 0 } };
  heute.bleibt = heute.brutto - sbSum(heute.abz); reform.bleibt = reform.brutto - sbSum(reform.abz);
  // GmbH: Der Teil des Gewinns, der in der Firma bleibt, ist kein Geld im Portemonnaie. Er steht in beiden Säulen gleich groß als eigenes Feld.
  let firma = null;
  if (h.gmbh > 0.5) {
    const satz = p.kst == null ? 0.15825 : p.kst, kst = h.gmbh * satz, aus = h.aus || 0, inv = Math.max(0, h.gmbh - kst - aus);
    firma = { gewinn: h.gmbh, kst, aus, inv, privat: h.gmbh - inv, quote: inv / h.gmbh, max: 1 - satz };
    heute.firma = inv; reform.firma = inv; heute.bleibt -= inv; reform.bleibt -= inv;
  }
  return { heute, reform, firma, plus: r.vgl + r.entfall };
}

function sbFmt() {
  const t = SB.teiler, n = x => Math.round(x / t) || 0, zahl = x => n(x).toLocaleString("de-DE").replace("-", "−");
  return { zahl, eur: x => zahl(x) + " €", sgn: x => (n(x) > 0 ? "+" : n(x) < 0 ? "−" : "±") + Math.abs(n(x)).toLocaleString("de-DE") + " €", einheit: t === 12 ? "im Monat" : "im Jahr" };
}
function sbTip(e, html) {
  if (!SB.tip) { SB.tip = document.createElement("div"); SB.tip.className = "sb-tip"; SB.tip.hidden = true; document.body.append(SB.tip); }
  const t = SB.tip; if (!html) { t.hidden = true; return; }
  t.innerHTML = html; t.hidden = false;
  const r = e.currentTarget.getBoundingClientRect(), x = e.clientX || r.left + r.width / 2, y = e.clientY || r.top;
  t.style.left = Math.max(8, Math.min(x + 14, window.innerWidth - 262)) + "px"; t.style.top = Math.max(8, Math.min(y + 14, window.innerHeight - t.offsetHeight - 8)) + "px";
}
function sbSeg(col, name, wert, ganz, px, bg, fg, cls, seite, zusatz) {
  const F = sbFmt(), s = document.createElement("div"); s.className = "sb-seg" + (cls ? " " + cls : "");
  s.style.height = Math.max(3, px) + "px"; if (bg) { s.style.background = `var(${bg})`; s.style.color = `var(${fg})`; }
  if (SB_FELD[cls] && px >= 30) s.innerHTML = `<small>${px >= 50 && col.clientWidth >= 84 ? SB_FELD[cls][0] : SB_FELD[cls][1]}</small>${F.eur(wert)}`;
  else if (px >= 17) s.textContent = F.eur(wert);
  const ant = Math.round(100 * wert / ganz);
  s.tabIndex = 0; s.setAttribute("aria-label", `${name}, ${seite}: ${F.eur(wert)} ${F.einheit}, ${ant} % der Säule`);
  const html = `<b>${name}</b><br>${seite}: ${F.eur(wert)} ${F.einheit}<br>${ant} % der Säule${zusatz ? "<br>" + zusatz : ""}`;
  s.onpointermove = e => sbTip(e, html); s.onpointerleave = () => sbTip(); s.onfocus = e => sbTip(e, html); s.onblur = () => sbTip();
  col.append(s); return s;
}

function sbZeichnen(el, d, o = {}) {
  SB.wieder = () => sbZeichnen(el, d, o); SB.nach = o.nachWechsel || null;
  el.classList.add("sb");
  if (!el.querySelector(".sb-plot")) {
    el.innerHTML = `<div class="sb-head"><h3 class="sb-title">Brutto, Abzüge und was im Portemonnaie bleibt</h3><button type="button" class="sb-info-btn" aria-expanded="false" aria-label="Erklärung zu den Säulen">i</button></div>
      <div class="sb-info" hidden></div>
      <div class="sb-row" role="group" aria-label="Zeitraum"><span class="sb-lbl">Beträge</span><button type="button" class="sb-chip" data-t="12">im Monat</button><button type="button" class="sb-chip" data-t="1">im Jahr</button></div>
      <div class="sb-inv" hidden></div>
      <div><div class="sb-plot"></div><div class="sb-axis"></div><p class="sb-unit"></p></div>
      <div class="sb-scroll"><table class="sb-t" lang="de"></table></div>`;
    el.querySelector(".sb-info-btn").onclick = () => { SB.info = !SB.info; SB.wieder(); };
    el.querySelectorAll(".sb-chip").forEach(b => b.onclick = () => { SB.teiler = +b.dataset.t; SB.wieder(); if (SB.nach) SB.nach(); });
    let rt; window.addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(() => SB.wieder && SB.wieder(), 120); });
  }
  if (!el.querySelector(".sb-inv")) { const k = document.createElement("div"); k.className = "sb-inv"; k.hidden = true; el.querySelector(".sb-row").after(k); }   // Gerüst aus einer älteren Fassung
  const F = sbFmt(), H = d.heute, V = d.reform, dir = sbSum(H.direkt), neu = sbSum(V.neu), fi = d.firma || null;
  SB.invest = o.invest && o.invest.setze || null;
  const ganzH = H.brutto + dir, ganzV = V.brutto, max = Math.max(ganzH, ganzV, 1);
  const ph = parseFloat(getComputedStyle(el).getPropertyValue("--sb-plot-h")) || 320, f = ph / max;
  // Schalter und Infotext
  el.querySelectorAll(".sb-chip").forEach(b => b.setAttribute("aria-pressed", +b.dataset.t === SB.teiler));
  const ib = el.querySelector(".sb-info-btn"), info = el.querySelector(".sb-info"); ib.setAttribute("aria-expanded", SB.info); info.hidden = !SB.info;
  const pm = Math.round(o.praemieMonat || 50);
  info.innerHTML = `<p><b>Brutto</b> ist alles, was hereinkommt: Lohn, Rente, Erträge, Geld vom Staat und was du aus Erspartem entnimmst.</p>
    <p><b>Arbeitgeberanteile</b> zahlt der Betrieb heute zusätzlich zu deinem Brutto für Rente, Pflege und Krankenkasse direkt an die Sozialkassen. Auf dem Konto siehst du sie nicht, sie gehören aber zu dem, was deine Arbeit kostet. Darum stehen sie schraffiert oben auf der Säule „Heute“. In der Reform bekommst du sie als Lohn ausgezahlt, das Brutto ist entsprechend höher. Bei Rentnern ist es der Anteil der Rentenkasse an der Krankenkasse.</p>
    <p><b>Abzüge</b> sind alle Steuern und Beiträge. Die Mehrwertsteuer zählt dazu, auch wenn sie im Preis steckt. Heute geht das meiste vom Lohn ab, in der Reform erst beim Ausgeben. Sozialbeiträge gibt es in der Reform nicht mehr, nur die Prämie der Krankenkasse von ${pm} € im Monat je Erwachsenem.</p>
    <p><b>Bleibt im Portemonnaie</b> ist, was für dich übrig ist: der Wert deines Einkaufs ohne die Steuern darin und was du zurücklegst.</p>
    ${fi ? `<p><b>Bleibt im Unternehmen</b> ist der Teil des Gewinns, den die GmbH behält und investiert. Er ist in beiden Säulen gleich groß, damit der Vergleich stimmt. Heute zahlt die Firma vorher Körperschaftsteuer auf den ganzen Gewinn, und auf die Ausschüttung kommt Abgeltungsteuer. In der Reform bleibt der Gewinn in der Firma steuerfrei. Besteuert wird erst, was du für dich ausgibst. Was dabei mehr im Portemonnaie bleibt als heute, ist noch nicht ausgegeben: Gibst du es aus, fällt darauf Ausgabensteuer an, lässt du es in der Firma, bleibt es steuerfrei. Die Gewerbesteuer von heute, rund 14 % des Gewinns, ist vorsichtshalber nicht mitgerechnet.</p>` : ""}
    <p>Gerechnet ist mit demselben Einkauf wie heute. Darum passt der Unterschied der beiden unteren Felder genau zur Zahl oben im Rechner. ${SB.teiler === 12 ? "Alle Beträge gelten im Monat. Mit dem Schalter „im Jahr“ siehst du das ganze Jahr." : "Alle Beträge gelten im Jahr. Mit dem Schalter „im Monat“ siehst du einen Monat."}</p>`;
  // GmbH: Schieber für die Investitionsquote und was mit dem Gewinn geschieht
  const inv = el.querySelector(".sb-inv"); inv.hidden = !fi;
  if (fi) {
    if (!inv.firstChild) {
      const id = "sb-q" + (++SB.nr);
      inv.innerHTML = `<div class="sb-inv-regler"><div class="sb-inv-kopf"><label for="${id}">Investitionsquote</label><output for="${id}"></output></div>
        <input type="range" class="sb-range" id="${id}" min="0" step="1">
        <div class="sb-inv-skala"><span>0 %: alles ausschütten</span><span class="sb-inv-max"></span></div></div>
        <p class="sb-inv-satz"></p>
        <div class="sb-scroll"><table class="sb-t sb-gt" lang="de"></table></div>`;
      inv.querySelector("input").oninput = e => { if (SB.invest) SB.invest(+e.target.value / 100); };
    }
    const pz = Math.round(100 * fi.quote), mx = Math.floor(100 * fi.max + 1e-9), ks = Math.round(100 * (1 - fi.max)), rg = inv.querySelector("input");
    inv.querySelector(".sb-inv-regler").hidden = !SB.invest;
    rg.max = mx; rg.value = Math.min(mx, pz); rg.setAttribute("aria-valuetext", `${pz} % des Gewinns bleiben im Unternehmen`);
    inv.querySelector("output").textContent = pz + "\u00a0%";
    inv.querySelector(".sb-inv-max").textContent = `${mx} %: heute das Höchste`;
    inv.querySelector(".sb-inv-satz").innerHTML = `Vom Gewinn der GmbH bleiben <b>${pz}\u00a0%</b> im Unternehmen und werden investiert, heute wie in der Reform. Heute zahlt die Firma vorher ${ks}\u00a0% Körperschaftsteuer, darum sind höchstens ${mx}\u00a0% möglich. In der Reform zahlt sie auf den Gewinn keine Steuer. Besteuert wird erst, was du für dich ausgibst.`;
    const gz = (n, h, v) => `<tr><td>${n}</td><td>${h}</td><td>${v}</td></tr>`, lk = (lang, kurz) => `<span class="sb-lang">${lang}</span><span class="sb-kurz">${kurz}</span>`;   // in der schmalen Spalte die kurze Fassung
    inv.querySelector("table").innerHTML = `<thead><tr><th>${lk("Gewinn der GmbH, Euro " + F.einheit, "Euro " + F.einheit)}</th><th>${(o.namen || ["Heute"])[0]}</th><th>${(o.namen || [0, "Reform"])[1]}</th></tr></thead><tbody>`
      + gz("Gewinn", F.zahl(fi.gewinn), F.zahl(fi.gewinn))
      + gz(`<i class="sb-sw" style="background:var(--sb-firma)"></i>${lk("bleibt im Unternehmen, investiert", "investiert")}`, F.zahl(fi.inv), F.zahl(fi.inv))
      + gz(lk("Körperschaftsteuer der Firma", "Steuer der Firma"), "−" + F.zahl(fi.kst), "0")
      + gz(`${lk("geht ins Private", "ins Private")}<small>heute als Ausschüttung</small>`, F.zahl(fi.aus), F.zahl(fi.privat)) + "</tbody>";
  }
  // Säulen
  const plot = el.querySelector(".sb-plot"), axis = el.querySelector(".sb-axis"); plot.innerHTML = ""; axis.innerHTML = "";
  const nb = t => t.replace(" ", "\u00a0");   // Betrag und Eurozeichen bleiben in einer Zeile
  const dirName = H.direkt.ag > 0.5 && H.direkt.rente > 0.5 ? "Arbeitgeber- und Rentenkassenanteil" : H.direkt.rente > 0.5 ? "Anteil der Rentenkasse" : "Arbeitgeberanteil";
  const top = { heute: `Brutto<b>${F.eur(H.brutto)}</b>${dir > 0.5 ? `<span class="sb-dz">+\u00a0${nb(F.eur(dir))} ${dirName}</span>` : ""}`,
    reform: `Brutto<b>${F.eur(V.brutto)}</b>${dir > 0.5 ? `<span class="sb-dz">mit ${dirName}</span>` : ""}${neu > 0.5 ? `<span class="sb-dz">${nb(F.sgn(neu))} vom Staat dazu</span>` : ""}` };
  const seg = {}, namen = o.namen || ["Heute", "Reform"];
  [[namen[0], H, "heute", ganzH], [namen[1], V, "reform", ganzV]].forEach(([titel, s, key, ganz], gi) => {
    const w = document.createElement("div"); w.className = "sb-colwrap"; w.innerHTML = `<div class="sb-top" lang="de">${top[key]}</div>`;
    const c = document.createElement("div"); c.className = "sb-col"; c.setAttribute("role", "group"); w.append(c); plot.append(w);   // erst einhängen, dann füllen: die Felder fragen die Breite der Säule ab
    c.setAttribute("aria-label", `${titel}: vom Brutto ${F.eur(s.brutto)} bleiben ${F.eur(s.bleibt)} ${F.einheit} im Portemonnaie${s.firma > 0.5 ? ` und ${F.eur(s.firma)} im Unternehmen` : ""}`);
    seg[key] = sbSeg(c, "Bleibt im Portemonnaie", s.bleibt, ganz, Math.max(0, s.bleibt) * f, "--sb-bleibt", "--sb-on-bleibt", "sb-bleibt", titel);
    if (s.firma > 0.5) sbSeg(c, "Bleibt im Unternehmen", s.firma, ganz, s.firma * f, "--sb-firma", "--sb-on-firma", "sb-firma", titel, "Vom Gewinn der GmbH, investiert. In beiden Säulen gleich viel.");
    for (const [k, nH, nV, bg, fg] of SB_ABZ) if (s.abz[k] > 0.5) sbSeg(c, key === "reform" && nV ? nV : nH, s.abz[k], ganz, s.abz[k] * f, bg, fg, "", titel);
    if (key === "heute") for (const k in SB_DIREKT) if (H.direkt[k] > 0.5) sbSeg(c, SB_DIREKT[k][0], H.direkt[k], ganz, H.direkt[k] * f, null, null, "sb-direkt", titel, SB_DIREKT[k][1]);
    const gn = document.createElement("div"); gn.className = "sb-gname"; gn.textContent = titel; axis.append(gn);
    if (gi === 0) { const m = document.createElement("div"); m.className = "sb-mid"; plot.append(m); axis.append(m.cloneNode()); }
  });
  el.querySelector(".sb-unit").textContent = `Alle Beträge in Euro ${F.einheit}, bei gleichem Einkauf wie heute.`;
  // Unterschied: gestrichelte Linie auf Höhe „bleibt heute“ bis zur Reform-Säule, Marke am Rand der Reform-Säule, Zahl in der Lücke
  const plus = V.bleibt - H.bleibt;
  requestAnimationFrame(() => {
    plot.querySelectorAll(".sb-guide,.sb-halo,.sb-dbar,.sb-dlab").forEach(n => n.remove());
    const pr = plot.getBoundingClientRect(), a = seg.heute.getBoundingClientRect(), b = seg.reform.getBoundingClientRect();
    const yH = a.top - pr.top, yV = b.top - pr.top, x1 = a.right - pr.left + 3, x2 = b.left - pr.left - 3;
    const mk = (cls, css) => { const n = document.createElement("div"); n.className = cls; n.style.cssText = css; return n; };
    const halo = mk("sb-halo", `left:${x1}px;width:${x2 - x1}px;top:${yH - 2}px`), g = mk("sb-guide", `left:${x1}px;width:${x2 - x1}px;top:${yH - 0.75}px`);
    const bar = mk("sb-dbar", `left:${x2 - 3}px;top:${Math.min(yH, yV)}px;height:${Math.max(3, Math.abs(yH - yV))}px;background:var(${plus >= 0 ? "--sb-mehr" : "--sb-weniger"})`);
    const mid = plot.querySelector(".sb-mid").getBoundingClientRect();
    const lab = mk("sb-dlab", ""); lab.innerHTML = `<b style="color:var(${Math.abs(plus) < 0.5 * SB.teiler ? "--fg" : plus > 0 ? "--good" : "--bad"})">${F.sgn(plus)}</b>${plus >= 0 ? "bleibt mehr" : "bleibt weniger"}`;
    plot.append(halo, g, bar, lab);
    // Die Zahl steht über der Linie. Reichen die Beschriftungen über den Säulen bis dorthin, steht sie unter der Linie.
    const tops = [...plot.querySelectorAll(".sb-top")].map(t => t.getBoundingClientRect()), frei = Math.max(...tops.map(t => t.bottom)) - pr.top + 4;
    const eng = tops.some(t => t.right > mid.left - 2 && t.left < mid.right + 2 && t.width > a.width);
    lab.style.left = (mid.left - pr.left + mid.width / 2) + "px";
    lab.style.top = (yH - 42 < frei && eng ? yH + 6 : Math.max(0, yH - 42)) + "px";
    if (lab.offsetWidth > mid.width - 4) { lab.innerHTML = lab.querySelector("b").outerHTML; if (!(yH - 42 < frei && eng)) lab.style.top = Math.max(0, yH - 24) + "px"; }
    if (lab.offsetWidth > mid.width - 4) lab.remove();
  });
  // Tabelle, zugleich Legende
  const sw = c => `<i class="sb-sw" style="background:var(${c})"></i>`, z = (n, h, v, cls) => `<tr${cls ? ` class="${cls}"` : ""}><td>${n}</td><td>${h}</td><td>${v}</td></tr>`;
  let t = `<thead><tr><th>Euro ${F.einheit}</th><th>${namen[0]}</th><th>${namen[1]}</th></tr></thead><tbody>`;
  t += z(`<b>Brutto</b>`, `<b>${F.zahl(H.brutto)}</b>`, `<b>${F.zahl(V.brutto)}</b>`);
  for (const k in SB_DIREKT) if (H.direkt[k] > 0.5) t += z(`<i class="sb-sw sb-direkt"></i>${SB_DIREKT[k][0]}<small>${SB_DIREKT[k][2]}</small>`, `+${F.zahl(H.direkt[k])}<small>zusätzlich</small>`, `<small>im Brutto</small>`, "sb-sub");
  for (const k in SB_NEU) if (V.neu[k] > 0.5) t += z(`neu vom Staat: ${SB_NEU[k]}`, "", "+" + F.zahl(V.neu[k]), "sb-sub");
  for (const [k, nH, nV, bg] of [...SB_ABZ].reverse()) if (H.abz[k] > 0.5 || V.abz[k] > 0.5)
    t += z(`${sw(bg)}${nH}${nV ? `<small>in der Reform: ${nV}</small>` : ""}${k === "ausg" && V.bszAbzug > 0.5 ? `<small>Bestandsschutz für heutige Rentner schon abgezogen: ${F.zahl(V.bszAbzug)}</small>` : ""}${k === "kap" && fi && fi.kst > 0.5 ? `<small>darin Körperschaftsteuer der GmbH: ${F.zahl(fi.kst)}</small>` : ""}`, H.abz[k] > 0.5 ? "−" + F.zahl(H.abz[k]) : "0", V.abz[k] > 0.5 ? "−" + F.zahl(V.abz[k]) : "0");
  if (fi && fi.inv > 0.5) t += z(`${sw("--sb-firma")}Bleibt im Unternehmen<small>investiert</small>`, F.zahl(fi.inv), F.zahl(fi.inv), "sb-rest");
  t += z(`${sw("--sb-bleibt")}Bleibt im Portemonnaie`, F.zahl(H.bleibt), F.zahl(V.bleibt), "sb-sum");
  el.querySelector(".sb-t:not(.sb-gt)").innerHTML = t + "</tbody>";
}

function sbAenderung(el, d) {
  const F = sbFmt(), H = d.heute, V = d.reform, plus = V.bleibt - H.bleibt;
  const items = [["Steuern und Beiträge von heute fallen weg", H.abz.sv + H.abz.est + H.abz.kap]];
  for (const k in SB_DIREKT) if (V.direkt[k] > 0.5) items.push([SB_DIREKT[k][3], V.direkt[k]]);
  for (const k in SB_NEU) if (V.neu[k] > 0.5) items.push([SB_NEU[k], V.neu[k]]);
  items.push(["Unterhalt für Kinder in Ausbildung entfällt", H.abz.unterhalt - V.abz.unterhalt], ["Prämie der Krankenkasse", -V.abz.sv], ["Derselbe Einkauf kostet mehr: höhere Mehrwertsteuer", -(V.abz.mwst - H.abz.mwst)], ["Ausgabensteuer (neu)", -(V.abz.ausg || 0)]);
  const rows = items.filter(([, v]) => Math.abs(v) > 0.5);
  const L = Math.max(1, ...rows.map(([, v]) => Math.max(0, -v)), Math.max(0, -plus)), R = Math.max(1, ...rows.map(([, v]) => Math.max(0, v)), Math.max(0, plus)), z0 = 100 * L / (L + R);
  const row = (n, v, net) => { const w = 100 * Math.abs(v) / (L + R), pos = v >= 0;
    return `<div class="sb-dvrow${net ? " sb-net" : ""}"><div class="sb-n">${n}</div><div class="sb-track" role="img" aria-label="${n}: ${F.sgn(v)} ${F.einheit}"><div class="sb-bar" style="left:${pos ? z0 : z0 - w}%;width:${w}%;background:var(${pos ? "--sb-mehr" : "--sb-weniger"});border-radius:${pos ? "0 4px 4px 0" : "4px 0 0 4px"}"></div><div class="sb-zero" style="left:${z0}%"></div></div><div class="sb-v">${F.sgn(v)}</div></div>`; };
  el.classList.add("sb");
  el.innerHTML = `<div class="sb-head"><h3 class="sb-title">Was sich ändert</h3></div>
    <p class="sb-note">Schritt für Schritt von heute zur Reform, in Euro ${F.einheit}. Die Balken zusammen ergeben den Unterschied aus dem Säulenbild.</p>
    <div class="sb-dvkey"><span><i class="sb-sw" style="background:var(--sb-mehr)"></i>nach rechts: mehr Geld</span><span><i class="sb-sw" style="background:var(--sb-weniger)"></i>nach links: weniger Geld</span></div>
    <div class="sb-dv" style="--sb-vw:calc(${Math.max(F.sgn(plus).length, ...rows.map(([, v]) => F.sgn(v).length))}ch + 14px)">${rows.map(([n, v]) => row(n, v)).join("")}${row("Unterm Strich", plus, true)}</div>`;
}
if (typeof module !== "undefined") module.exports = { sbDaten, sbSum };
