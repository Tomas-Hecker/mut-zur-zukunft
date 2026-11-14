// Steuerlast heute und mit der Reform (Startjahr, gleicher Einkauf), nach Einkommenszehnteln und Vermögensstufen.
// Mit Tomas' Wahl für Version 32 (14.11., 10:36): Rentner beim Start bis 300 € im Monat ausgeglichen, 10 € im Monat je Erwachsenem,
// Hausregel 2 % des Kaufpreises statt Mietwert bis 40 m² je Erwachsenem plus 15 m² je Kind (wie wahl-v32/haus40.js).
// Aufruf: node steuerlast.js [ohne]  ->  steuerlast.json und steuerlast/index.html   („ohne“: Reform ohne Ausgleich und Hausregel)
const fs = require("fs"); const K = require("./kern.js"); const S = require("./simulation.js");
const pop0 = require("./bevoelkerung.json"); const sp = pop0.spalten; const n = pop0.n;
const WAHL = process.argv[2] !== "ohne";
// Tomas 14.11. 10:51: Hausregel nur für Häuser, die nach dem Start gekauft werden. Im ersten Jahr greift sie daher bei keinem Haushalt.
// Mit "haus" als Argument wird sie zum Vergleich auf alle Eigentümer angewandt.
const HAUS = process.argv.includes("haus");
// Hausregel: Fläche aus dem Hauswert (Eigentümer im Mittel 125,8 m²), innerhalb der Grenze 2 % des Kaufpreises statt Mietwert
let wert = 0, hhN = 0;
for (let i = 0; i < n; i++) if (sp.eigen[i] && sp.hauswert[i] > 0 && sp.typ[i] !== "kind_erw") { wert += sp.w[i] * sp.hauswert[i]; hhN += sp.w[i]; }
const QM = wert / (hhN * 125.8);
const miet = Float64Array.from(sp.miet);
if (WAHL && HAUS) for (let i = 0; i < n; i++) {
  if (!sp.eigen[i] || !(sp.hauswert[i] > 0) || !(sp.miet[i] > 0)) continue;
  const drin = Math.min(1, (40 * Math.max(1, sp.erw[i]) + 15 * sp.kinder[i]) / (sp.hauswert[i] / QM));
  miet[i] = sp.miet[i] * (drin * 0.02 * sp.hauswert[i] / sp.miet[i] + (1 - drin));
}
const pop = { ...pop0, spalten: { ...sp, miet } };
const e = S.rechne(K, pop, WAHL ? { ausgleichRentnerMonat: 300, pauschaleErwMonat: 10 } : {}); const opt = e.opt;
// Ausgleich: heutige Rentner bis 300 € im Monat, alle Erwachsenen 10 € im Monat
// Ausgleich rechnet simulation.js (r.ausgl), r.plus enthält ihn schon
const ausgleich = r => r.ausgl || 0;
const H = [];
let maxFehler = 0, maxEk = 0;
for (const r of e.R) {
  const i = r.i; if (sp.typ[i] === "kind_erw") continue;
  const beamte = sp.beamter[i] ? opt.beamtePlus * sp.pension[i] + r.zulage : 0;
  // Erbschaft: erwartete Steuer im Jahr (Sterbewahrscheinlichkeit × Steuer auf den Nachlass, dazu Schenkungen)
  const erbH = e.erbe.heute[i], erbR = e.erbe.anspruch[i] * opt.realStart, erbL = e.erbe.anspruch[i] * opt.realLang;
  const heute = { est: r.heute.est, sv: r.heute.sv, kap: r.heute.kap, mwst: r.heute.mwst, erb: erbH };
  const x = ausgleich(r);
  const reform = { ausg: r.atg + r.ausgUeb, mwst: r.heute.mwst + r.pw, sv: r.svNeu, aus: -(r.gut - r.bsz) - beamte, bsz: -r.bsz, ausgl: -x, erb: erbR, erbLang: erbL };
  const sh = heute.est + heute.sv + heute.kap + heute.mwst + heute.erb;
  const sr = reform.ausg + reform.mwst + reform.sv + reform.aus + reform.bsz + reform.ausgl + reform.erb;
  const srL = sr - erbR + erbL;
  // Probe: Unterschied der Lasten ohne Erbschaft = Plus bei gleichem Einkauf (Beamte samt Zulage)
  maxFehler = Math.max(maxFehler, Math.abs((sh - erbH - (sr - erbR)) - r.plus));
  // Einkommensarten (Summe = r.einkommen, geprüft) und Vermögensarten
  const ek = { lohn: sp.lohn1[i] + (sp.erw[i] === 2 ? sp.lohn2[i] : 0) + sp.mini[i], rente: sp.rente[i] + sp.pension[i], firma: sp.gewinn[i] + sp.gmbh[i],
    kap: sp.kap[i], miete: sp.vermietCash[i], sozial: sp.transfer[i] + sp.kinder[i] * 259 * 12 + (sp.leist ? sp.leist[i] : 0) };
  maxEk = Math.max(maxEk, Math.abs(Object.values(ek).reduce((a, b) => a + b, 0) - r.einkommen));
  const verm = { haus: sp.hauswert[i], immo: sp.immo[i], geld: sp.geld[i], betrieb: sp.betrieb[i] };
  const spar = r.verf - r.konsum - sp.vollj[i] * sp.unterhalt[i] * 12;
  H.push({ w: sp.w[i], ek: r.einkommen, W: sp.W[i], heute, reform, sh, sr, srL, netto: r.plus / 12, rentner: sp.rentner[i] > 0, eka: ek, verm, spar, sparR: spar + r.plus, erbH, erbR, erbL });
}
function gruppen(schluessel, namen) {
  const g = namen.map(n => ({ name: n, hh: 0, ek: 0, heute: { est: 0, sv: 0, kap: 0, mwst: 0, erb: 0 }, reform: { ausg: 0, mwst: 0, sv: 0, aus: 0, bsz: 0, ausgl: 0, erb: 0, erbLang: 0 }, sh: 0, sr: 0, srL: 0, mehr: 0, wen: 0, wenSum: 0, wenRent: 0 }));
  for (const h of H) {
    const x = g[schluessel(h)]; x.hh += h.w; x.ek += h.w * h.ek; x.sh += h.w * h.sh; x.sr += h.w * h.sr; x.srL += h.w * h.srL;
    if (h.netto > 0.5) x.mehr += h.w; else if (h.netto < -0.5) { x.wen += h.w; x.wenSum += h.w * h.netto; if (h.rentner) x.wenRent += h.w; }
    for (const k in h.heute) x.heute[k] += h.w * h.heute[k]; for (const k in h.reform) x.reform[k] += h.w * h.reform[k];
  }
  const totH = g.reduce((s, x) => s + x.sh, 0), totR = g.reduce((s, x) => s + x.sr, 0), totL = g.reduce((s, x) => s + x.srL, 0);
  return g.map(x => {
    const m = v => Math.round(v / x.hh / 12);
    const o = { name: x.name, haushalte_mio: +(x.hh / 1e6).toFixed(2), einkommen_monat: m(x.ek),
      heute: Object.fromEntries(Object.entries(x.heute).map(([k, v]) => [k, m(v)])), reform: Object.fromEntries(Object.entries(x.reform).map(([k, v]) => [k, m(v)])),
      last_heute_monat: m(x.sh), last_reform_monat: m(x.sr), last_reform_lang_monat: m(x.srL),
      quote_heute: +(100 * x.sh / x.ek).toFixed(1), quote_reform: +(100 * x.sr / x.ek).toFixed(1), quote_reform_lang: +(100 * x.srL / x.ek).toFixed(1),
      anteil_heute: +(100 * x.sh / totH).toFixed(1), anteil_reform: +(100 * x.sr / totR).toFixed(1), anteil_reform_lang: +(100 * x.srL / totL).toFixed(1),
      summe_heute_mrd: +(x.sh / 1e9).toFixed(1), summe_reform_mrd: +(x.sr / 1e9).toFixed(1), summe_reform_lang_mrd: +(x.srL / 1e9).toFixed(1),
      mehr_prozent: +(100 * x.mehr / x.hh).toFixed(1), weniger_prozent: +(100 * x.wen / x.hh).toFixed(1), weniger_mio: +(x.wen / 1e6).toFixed(2),
      weniger_mittel_monat: x.wen ? Math.round(-x.wenSum / x.wen) : 0, weniger_rentner_mio: +(x.wenRent / 1e6).toFixed(2) };
    return o;
  });
}
// Zehntel nach Haushaltseinkommen vor Steuern (alle Einkommen samt Renten und Grundsicherung)
const sortiert = H.map((h, k) => k).sort((a, b) => H[a].ek - H[b].ek);
const gesamt = H.reduce((s, h) => s + h.w, 0); let kum = 0; const zehntel = new Array(H.length);
for (const k of sortiert) { zehntel[k] = Math.min(9, Math.floor(10 * kum / gesamt)); kum += H[k].w; }
const grenzen = []; kum = 0; let next = 1;
for (const k of sortiert) { kum += H[k].w; if (next < 10 && kum >= next * gesamt / 10) { grenzen.push(Math.round(H[k].ek / 12)); next++; } }
const idx = new Map(H.map((h, k) => [h, k]));
const z = gruppen(h => zehntel[idx.get(h)], ["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10."].map(s => s + " Zehntel"));
const vs = gruppen(h => Math.min(5, S.stufeVon(h.W)), ["unter 100.000 €", "100.000 bis 200.000 €", "200.000 bis 400.000 €", "400.000 bis 800.000 €", "800.000 € bis 1 Mio. €", "über 1 Mio. €"]);
const tot = { heute_mrd: +(H.reduce((s, h) => s + h.w * h.sh, 0) / 1e9).toFixed(1), reform_mrd: +(H.reduce((s, h) => s + h.w * h.sr, 0) / 1e9).toFixed(1), reform_lang_mrd: +(H.reduce((s, h) => s + h.w * h.srL, 0) / 1e9).toFixed(1) };
// oberstes Prozent nach Einkommen
const top1 = { sh: 0, sr: 0, srL: 0 }; kum = 0;
for (const k of sortiert) { kum += H[k].w; if (kum > 0.99 * gesamt) { top1.sh += H[k].w * H[k].sh; top1.sr += H[k].w * H[k].sr; top1.srL += H[k].w * H[k].srL; } }
// Haushalte mit mehr und weniger (gleicher Einkauf, mit Ausgleich)
let nMehr = 0, nWen = 0, nAll = 0;
for (const r of e.R) { if (sp.typ[r.i] === "kind_erw") continue; const m = r.plus / 12; nAll += sp.w[r.i]; if (m > 0.5) nMehr += sp.w[r.i]; else if (m < -0.5) nWen += sp.w[r.i]; }
// Einkommen × Vermögen: 10 × 10 Felder (Zehntel nach Haushaltseinkommen und nach Nettovermögen)
const sortW = H.map((h, k) => k).sort((a, b) => H[a].W - H[b].W);
const vz = new Array(H.length); const vgrenzen = []; kum = 0; next = 1;
for (const k of sortW) { vz[k] = Math.min(9, Math.floor(10 * kum / gesamt)); kum += H[k].w; if (next < 10 && kum >= next * gesamt / 10) { vgrenzen.push(Math.round(H[k].W)); next++; } }
const leer = () => ({ hh: 0, n: 0, plus: 0, mehr: 0, wen: 0, ek: 0, W: 0, dl: 0, dlL: 0 });
const M = Array.from({ length: 10 }, () => Array.from({ length: 10 }, leer));
const randE = Array.from({ length: 10 }, leer), randV = Array.from({ length: 10 }, leer), alle = leer();
H.forEach((h, k) => { for (const c of [M[zehntel[k]][vz[k]], randE[zehntel[k]], randV[vz[k]], alle]) {
  c.hh += h.w; c.n++; c.plus += h.w * h.netto; c.ek += h.w * h.ek; c.W += h.w * h.W; c.dl += h.w * (h.sh - h.sr); c.dlL += h.w * (h.sh - h.srL);
  if (h.netto > 0.5) c.mehr += h.w; else if (h.netto < -0.5) c.wen += h.w; } });
const feld = c => ({ haushalte_mio: +(c.hh / 1e6).toFixed(3), faelle: c.n, plus_monat: c.hh ? Math.round(c.plus / c.hh) : null,
  mehr_prozent: c.hh ? +(100 * c.mehr / c.hh).toFixed(1) : null, weniger_prozent: c.hh ? +(100 * c.wen / c.hh).toFixed(1) : null,
  einkommen_monat: c.hh ? Math.round(c.ek / c.hh / 12) : null, vermoegen: c.hh ? Math.round(c.W / c.hh) : null,
  // weniger Last in % des Einkommens (positiv = mehr Geld), mit Erbe im ersten Jahr und voll wirksam
  entlastung_prozent: c.ek > 0 ? +(100 * c.dl / c.ek).toFixed(1) : null, entlastung_lang_prozent: c.ek > 0 ? +(100 * c.dlL / c.ek).toFixed(1) : null,
  entlastung_monat: c.hh ? Math.round(c.dl / c.hh / 12) : null, entlastung_lang_monat: c.hh ? Math.round(c.dlL / c.hh / 12) : null });
const matrix = { zeilen_einkommen_spalten_vermoegen: M.map(z => z.map(feld)), einkommen: randE.map(feld), vermoegen: randV.map(feld), alle: feld(alle), vermoegen_grenzen: vgrenzen };
// Welche Einkommen und Vermögen die Last tragen
// Einkommen: die Last eines Haushalts ohne Erbe wird nach dem Anteil jeder Einkommensart an seinem Einkommen verteilt.
// Erbe: die erwartete Erbschaftsteuer (heute) und der Staatsanteil (Reform) nach dem Anteil jeder Vermögensart am Nachlass;
// heute mit den Bewertungsregeln (Immobilien zu drei Vierteln, Firmen zu 85 % verschont), mit der Reform alles voll.
const EKN = { lohn: "Löhne und Gehälter", rente: "Renten und Pensionen", firma: "Gewinne eigener Firmen", kap: "Zinsen und Dividenden", miete: "Mieten", sozial: "Sozialleistungen und Kindergeld" };
const VN = { haus: "selbst bewohnte Häuser", immo: "vermietete Häuser und Wohnungen", geld: "Geld und Wertpapiere", betrieb: "Firmen" };
const ea = Object.fromEntries(Object.keys(EKN).map(k => [k, { basis: 0, h: 0, r: 0, rL: 0 }]));
const va = Object.fromEntries(Object.keys(VN).map(k => [k, { basis: 0, h: 0, r: 0, rL: 0 }]));
let ohneEkH = 0, ohneEkR = 0;
for (const h of H) {
  const lh = h.sh - h.heute.erb, lr = h.sr - h.reform.erb;
  if (h.ek > 0) for (const k in ea) { const y = h.eka[k]; ea[k].basis += h.w * y; ea[k].h += h.w * lh * y / h.ek; ea[k].r += h.w * lr * y / h.ek; ea[k].rL += h.w * lr * y / h.ek; }
  else { ohneEkH += h.w * lh; ohneEkR += h.w * lr; }
  const bh = { haus: 0.75 * h.verm.haus, immo: 0.75 * h.verm.immo, geld: h.verm.geld, betrieb: 0.15 * h.verm.betrieb };
  const sH = Object.values(bh).reduce((a, b) => a + b, 0), sR = Object.values(h.verm).reduce((a, b) => a + b, 0);
  for (const k in va) { va[k].basis += h.w * h.verm[k]; if (sH > 0) va[k].h += h.w * h.erbH * bh[k] / sH; if (sR > 0) { va[k].r += h.w * h.erbR * h.verm[k] / sR; va[k].rL += h.w * h.erbL * h.verm[k] / sR; } }
}
const arten = {
  einkommen: Object.entries(ea).map(([k, a]) => ({ art: k, name: EKN[k], einkommen_mrd: +(a.basis / 1e9).toFixed(1), heute_mrd: +(a.h / 1e9).toFixed(1), reform_mrd: +(a.r / 1e9).toFixed(1), reform_lang_mrd: +(a.rL / 1e9).toFixed(1),
    je100_heute: +(100 * a.h / a.basis).toFixed(1), je100_reform: +(100 * a.r / a.basis).toFixed(1) })),
  erbe: Object.entries(va).map(([k, a]) => ({ art: k, name: VN[k], bestand_bio: +(a.basis / 1e12).toFixed(2), heute_mrd: +(a.h / 1e9).toFixed(1), reform_mrd: +(a.r / 1e9).toFixed(1), reform_lang_mrd: +(a.rL / 1e9).toFixed(1) })),
  ohne_einkommen_mrd: { heute: +(ohneEkH / 1e9).toFixed(2), reform: +(ohneEkR / 1e9).toFixed(2) },
};
// Vermögensaufbau: Sparen je Haushalt bei gleichem Einkauf (das Plus der Reform wird ganz gespart), Erbe an den Staat
const vg = ["unter 100.000 €", "100.000 bis 200.000 €", "200.000 bis 400.000 €", "400.000 bis 800.000 €", "800.000 € bis 1 Mio. €", "über 1 Mio. €"].map(n => ({ name: n, hh: 0, sH: 0, sR: 0, eH: 0, eR: 0, eL: 0, W: 0, ek: 0, x: 0 }));
for (const h of H) { const g = vg[Math.min(5, S.stufeVon(h.W))]; g.hh += h.w; g.sH += h.w * h.spar; g.sR += h.w * h.sparR; g.eH += h.w * h.erbH; g.eR += h.w * h.erbR; g.eL += h.w * h.erbL; g.W += h.w * h.W; g.ek += h.w * h.ek; g.x -= h.w * h.reform.ausgl; }
const aufbau = vg.map(g => ({ name: g.name, haushalte_mio: +(g.hh / 1e6).toFixed(2), vermoegen_mittel: Math.round(g.W / g.hh),
  sparen_heute_monat: Math.round(g.sH / g.hh / 12), sparen_reform_monat: Math.round(g.sR / g.hh / 12), wachstum_heute: +(100 * g.sH / g.W).toFixed(1), wachstum_reform: +(100 * g.sR / g.W).toFixed(1), sparquote_heute: +(100 * g.sH / g.ek).toFixed(1), sparquote_reform: +(100 * g.sR / g.ek).toFixed(1), einkommen_monat: Math.round(g.ek / g.hh / 12), sparen_heute_mrd: +(g.sH / 1e9).toFixed(1), sparen_reform_mrd: +(g.sR / 1e9).toFixed(1),
  erbe_heute_mrd: +(g.eH / 1e9).toFixed(1), erbe_reform_mrd: +(g.eR / 1e9).toFixed(1), erbe_reform_lang_mrd: +(g.eL / 1e9).toFixed(1) }));
const out = { stand: new Date().toISOString().slice(0, 10), wahl: WAHL, hausregel_alle: HAUS, mehr_prozent: +(100 * nMehr / nAll).toFixed(1), weniger_mio: +(nWen / 1e6).toFixed(1), probe_max_abweichung_eur: +maxFehler.toFixed(2), zehntel_grenzen_monat: grenzen, matrix, arten, aufbau, probe_einkommensarten_eur: +maxEk.toFixed(2), ausgleich_mrd: +(vg.reduce((a, g) => a + g.x, 0) / 1e9).toFixed(1), gesamt: tot,
  oberstes_prozent: { anteil_heute: +(100 * top1.sh / (tot.heute_mrd * 1e9)).toFixed(1), anteil_reform: +(100 * top1.sr / (tot.reform_mrd * 1e9)).toFixed(1), anteil_reform_lang: +(100 * top1.srL / (tot.reform_lang_mrd * 1e9)).toFixed(1) },
  zehntel: z, vermoegen: vs };
fs.writeFileSync(__dirname + "/steuerlast.json", JSON.stringify(out, null, 1));
console.log("Wahl", WAHL, "Hausregel für alle", HAUS, "mehr", out.mehr_prozent, "% weniger", out.weniger_mio, "Mio. Probe", maxFehler.toFixed(2), "Grenzen", grenzen.join(" "), JSON.stringify(tot), JSON.stringify(out.oberstes_prozent));
for (const x of [...z, ...vs]) console.log(x.name.padEnd(24), x.haushalte_mio, x.einkommen_monat, "heute", x.last_heute_monat, x.quote_heute + "%", "reform", x.last_reform_monat, x.quote_reform + "%", x.quote_reform_lang + "%", "Anteil", x.anteil_heute, x.anteil_reform, x.anteil_reform_lang, JSON.stringify(x.heute), JSON.stringify(x.reform));
// Seite bauen: steuerlast/index.html aus der Vorlage mit den Daten
const vorlage = fs.readFileSync(__dirname + "/steuerlast/vorlage.html", "utf8");
fs.writeFileSync(__dirname + "/steuerlast/index.html", vorlage.replace("/*DATEN*/null", () => JSON.stringify(out)));
