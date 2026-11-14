// Mikrosimulation: rechnet jeden künstlichen Haushalt nach heutigem Recht und mit der Reform, mit demselben Rechenkern wie der
// Steuerrechner (kern.js), und fügt hinzu, was der Kern nicht kennt: Vermögen, Erbschaften und Verhalten.
// Läuft in Node (node lauf.js) und im Browser (seite/index.html). Alle Annahmen stehen in STANDARD und lassen sich überschreiben.
"use strict";

const STANDARD = {
  // Rechenkern wie Version 31: Konsum 2.300,2, Miete und Mietwert 214,5, Härteausgleich aus
  kern: { Konsum: 2300.2, Miete: 214.5, Nutzwert: 214.5, HAAn: 0 },
  eichung: "konsum",           // "konsum" (Standard seit 14.11.): Konsum genau wie VGR 2025 und Version 31; "sparquote": Konsum aus Einkommen und Sparquote der VGR
  sparquoteZiel: 0.104,        // Sparquote der privaten Haushalte 2025 (Statistisches Bundesamt, VGR): rund 10,4 %
  sparRentner: -0.10, sparSelbst: 0.06,   // Versatz der Sparquote für Rentner- und Selbständigenhaushalte: geeicht mit eichen_sparen.js auf
                               // den Abstand der Konsumquoten in der EVS 2018 (Fachserie 15 Heft 4, Tabelle 1.2)
  konsumZiel: 2085.7,          // Mrd. €: Konsum ohne Mietwert, 2.300,2 − 214,5 wie im Blatt Verteilung; die Sparquoten werden darauf geeicht
  kapKonsum: [0.5, 0.25],      // Anteil der Kapitalerträge nach Steuer, der ausgegeben wird (unter / ab 1 Mio. € Vermögen); der Rest
                               // wird wieder angelegt (Baker, Nagel, Wurgler 2007; Di Maggio, Kermani, Majlesi 2020)
  entsparGrenze: 0.05,         // Entsparen im Jahr höchstens 5 % des Geldvermögens
  beamtePlus: 0.302,           // Bezüge steigen um 13 % (Beihilfe wird ausgezahlt, 22,6 Mrd. €) und um 17,2 % (Anpassung 30 Mrd. € auf rund
                               // 174 Mrd. € Bezüge); eine Zulage gleicht aus, was bei gleichem Einkauf dann noch fehlt
  // Verhalten (Stufen wie der Eichpunkt: <100 Tsd., 100–200, 200–400, 400–800 Tsd., 0,8–1 Mio., 1–10, 10–100, >100 Mio. €)
  verhalten: true,
  mpc: [0.75, 0.6, 0.5, 0.4, 0.35, 0.25, 0.15, 0.1],   // Anteil des Plus, der im selben Jahr ausgegeben wird
  mpcGrundsicherung: 1.0,
  plusVererbt: null,           // Anteil des angelegten Plus, der vererbt wird (null = „vererbt“ je Stufe; 1 = alles angelegt und vererbt)
  mpcMittelZiel: 0.5,          // Version 32: im Mittel (gewichtet mit dem Plus) wird die Hälfte ausgegeben; null = Anteile je Stufe unverändert         // z. B. 0.5: alle Anteile so skaliert, dass im Mittel (gewichtet mit dem Plus) die Hälfte ausgegeben wird
  kuerzung: [1.0, 0.8, 0.5, 0.25, 0.25, 0.25, 0.25, 0.25],  // Anteil eines Minus, um den der Haushalt seinen Einkauf SOFORT kürzt
                               // (Version 32: Vermögende ein Viertel; wer wenig hat, muss sofort sparen)
  minusAusErbe: null,          // Anteil eines nicht gekürzten Minus, der am Ende am Erbe fehlt (null = wie „vererbt“ je Stufe;
                               // 1 = Variante „Reiche geben weiter so viel aus und vererben nur weniger“, dazu kuerzung = 0)
  kuerzungLang: 1.0,           // Anteil, um den der Einkauf nach und nach (im Dauerzustand) gekürzt ist
  vererbt: [0.05, 0.2, 0.3, 0.4, 0.5, 0.6, 0.75, 0.85], // Anteil des Angelegten, der am Ende vererbt statt selbst ausgegeben wird
  vererbtAlter: 0.15,          // Rentnerhaushalte vererben mehr vom Angelegten
  // Erbschaften
  q65: 0.0095, gompertz: 0.105, // Sterberate mit 65 (Mittel Frauen und Männer) und Anstieg je Lebensjahr (wie Rechenmodell RTSteig)
  paarFaktor: 0.6, paarVersatz: 6, // Paar: Nachlass erst beim zweiten Tod, Rate wie 0,5 × q(Alter + 6)
  schenkungQ: 0.009,           // Schenkungen großer Vermögen im Jahr, Anteil des Vermögens über 500.000 €
  schenkSatzHeute: 0.04,
  kinderJeNachlass: 2,
  staatsanteil: 0.5, famFrei: 400000, famKindQ: 0.25, andFrei: 20000,
  realStart: 0.25, realLang: 0.5, // fällig, wenn Geld ins Private fließt (wie Gesamtrechnung: 25 % am Start, langfristig 50 %)
  // Ausgleich (Version 32, Tomas 14.11.2026: Rentner bis 300 €, 10 € je Erwachsenem); hier 0, die Seite und steuerlast.js setzen ihn
  ausgleichRentnerMonat: 0,    // heutige Rentner: Minus wird bis zu diesem Betrag im Monat ausgeglichen, läuft mit ihnen aus
  pauschaleErwMonat: 0,        // jeder Erwachsene bekommt diesen Betrag im Monat
};

function zahl(x) { return typeof x === "number" ? x : 0; }

function erzeugeKern(K, opt) {
  Object.assign(K.A, structuredClone(K.A0));
  K.sicherheitAnwenden();
  Object.assign(K.A, opt.kern, opt.kernExtra || {});
  K.abgeleitet();
  return K;
}

function eingabe(sp, i, spar) {
  const pens = sp.pension[i];
  return {
    erw: sp.erw[i], kinder: sp.kinder[i], kid6: sp.kid6[i], kid3: sp.kid3[i],
    lohn1: sp.lohn1[i], std1: sp.std1[i], lohn2: sp.lohn2[i], std2: sp.std2[i], mini: sp.mini[i], rente: sp.rente[i],
    gewinn: sp.gewinn[i], kap: sp.kap[i], gmbh: sp.gmbh[i], aus: sp.aus[i], transfer: sp.transfer[i], verm: sp.verm[i],
    vermiet: sp.vermiet[i] + pens, vermietCash: sp.vermietCash[i] + pens, _frei: sp.leist ? sp.leist[i] : 0,
    miet: sp.miet[i], hb: sp.hb[i], kinderlos: sp.kinderlos[i], spar, pkv: sp.pkv[i], vorsorge: sp.abzug ? sp.abzug[i] : 0,
    rentner: sp.rentner[i], bs: sp.bs[i], allein: sp.allein[i], vollj: sp.vollj[i], unterhalt: sp.unterhalt[i], pg: 0, bjob: 0, vz: 0,
  };
}

// Patch für vermietCash: der Kern zählt h.vermiet im verfügbaren Einkommen; die nicht steuerpflichtigen Mieten (Abschreibung, Zinsen)
// kommen hier als Kapitalertrag ohne Steuer dazu, indem sie über verm (Ausgaben aus Vermögen) laufen würden — das wäre falsch,
// deshalb rechnen wir den Unterschied selbst: verf + (vermietCash − vermiet).

function sparquote(verf, rentner, transfer, a0) {
  if (transfer > 0) return 0;
  let s = a0 + 0.10 * Math.log(Math.max(verf, 5000) / 30000) + 0.08 * Math.max(0, Math.log(Math.max(verf, 1) / 100000));   // Rentner sparen in Deutschland im Mittel weiter (EVS)
  return Math.min(0.75, Math.max(-0.10, s));
}

function stufeVon(W) { const g = [1e5, 2e5, 4e5, 8e5, 1e6, 1e7, 1e8]; let j = 0; while (j < g.length && W >= g[j]) j++; return j; }

function rechne(K, pop, optIn = {}) {
  const opt = { ...STANDARD, ...optIn, kern: { ...STANDARD.kern, ...(optIn.kern || {}) } };
  erzeugeKern(K, opt);
  const A = K.A, sp = pop.spalten, n = pop.n;
  const w = sp.w;
  // 1) Verfügbares Einkommen heute (Sparquote 0). Konsum = (Einkommen ohne Kapitalerträge) × (1 − Sparquote)
  //    + Kapitalerträge nach Steuer × kapKonsum + Verzehr von Erspartem. Wer mehr ausgibt, als er einnimmt (Sparquote unter null),
  //    entspart: Das läuft wie Ausgaben aus altem Vermögen (Altvermögenskonto), soweit Geldvermögen da ist.
  const verf0 = new Float64Array(n), kapN = new Float64Array(n);
  for (let i = 0; i < n; i++) {
    const h = eingabe(sp, i, 0);
    const extra = h.vermietCash - h.vermiet + h._frei;
    const r = K.haushalt(h);
    verf0[i] = r.verf - r.unterhalt + extra;
    const kb = sp.kap[i] + sp.aus[i] + sp.vermietCash[i];
    kapN[i] = Math.max(0, Math.min(verf0[i], kb - r.heute.kap - (kb > 0 ? 0.25 * sp.vermiet[i] : 0)));
  }
  const kq = i => (sp.W[i] >= 1e6 ? opt.kapKonsum[1] : opt.kapKonsum[0]);
  const plan = (i, a0) => {
    const basis = verf0[i] - kapN[i];
    const s = sparquote(basis, sp.rentner[i], sp.transfer[i], a0 + (sp.rentner[i] ? opt.sparRentner : sp.selbst[i] ? opt.sparSelbst : 0));
    let konsum = basis * (1 - s) + kapN[i] * kq(i) + sp.verm[i];
    const entspar = s < 0 ? Math.min(-s * basis, Math.max(0, sp.geld[i]) * opt.entsparGrenze) : 0;
    // Leistungen wie Arbeitslosen-, Kranken- und Elterngeld: Die Reform müsste sie so anpassen, dass derselbe Einkauf möglich bleibt.
    // Der Teil des Konsums, den sie bezahlen, bleibt deshalb außerhalb des Rechenkerns (für den Haushalt neutral).
    const leist = sp.leist ? sp.leist[i] * Math.min(1, 1 - s) : 0;
    return { konsum, verm: sp.verm[i] + entspar, leist };
  };
  const konsumSumme = a0 => { let s = 0; for (let i = 0; i < n; i++) s += w[i] * plan(i, a0).konsum; return s / 1e9; };
  let verfSumme = 0; for (let i = 0; i < n; i++) verfSumme += w[i] * verf0[i];
  const ziel = opt.eichung === "konsum" ? opt.konsumZiel : (1 - opt.sparquoteZiel) * verfSumme / 1e9;
  let lo = -0.5, hi = 0.6;
  if (opt.eichung !== "fest") for (let k = 0; k < 50; k++) { const m = (lo + hi) / 2; if (konsumSumme(m) > ziel) lo = m; else hi = m; }
  const a0 = opt.eichung === "fest" ? opt.a0fest : (lo + hi) / 2;
  // 2) Rechenkern je Haushalt
  const ps = A.NormPkt / 100 + A.SichPkt / 100;
  const mwstSatzNeu = A.MwStQ + A.NormAnteil * ((0.19 + ps) / (1.19 + ps) - 0.19 / 1.19);
  const R = [];
  for (let i = 0; i < n; i++) {
    const h = eingabe(sp, i, 0);
    const extra = h.vermietCash - h.vermiet + h._frei;
    const pl = plan(i, a0);
    h.verm = pl.verm;
    // Der Kern rechnet Konsum = (verf − unterhalt) × (1 − spar) + verm, ohne die steuerfreien Einnahmen: spar passend setzen
    const kernVerf = verf0[i] - extra;
    h.spar = kernVerf > 0 ? 1 - (pl.konsum - pl.leist - pl.verm) / kernVerf : 0;
    const r = K.haushalt(h);
    // Beamte und Pensionäre: Bezüge + 13 %, Zulage gleicht aus, was bei gleichem Einkauf noch fehlt
    let plus = r.vgl, zulage = 0;
    if (sp.beamter[i]) {
      plus += opt.beamtePlus * sp.pension[i];   // bei gleichem Einkauf bleibt das Mehr an Bezügen ganz übrig
      if (plus < 0) { zulage = -plus; plus = 0; }
    }
    // Ausgleich: Rentner bis zur Grenze (aus dem Minus vor der Pauschale), dazu die Pauschale je Erwachsenem
    const ausgl = (sp.rentner[i] > 0 ? Math.min(Math.max(0, -plus), 12 * opt.ausgleichRentnerMonat) : 0) + 12 * opt.pauschaleErwMonat * sp.erw[i];
    plus += ausgl;
    // Steueranteil eines zusätzlichen Euros, den der Haushalt ausgibt (Ausgabensteuer und Mehrwertsteuer), mit Altvermögenskonto
    const ueber2 = r.konsum + r.pw + r.mietw - r.alt - r.frei;
    const tauM = ueber2 > 0 ? (A.Satz3 + mwstSatzNeu) / (1 + A.Satz3) : mwstSatzNeu;
    const tauLang = (r.konsum + r.pw + r.mietw - r.frei) > 0 ? (A.Satz3 + mwstSatzNeu) / (1 + A.Satz3) : mwstSatzNeu;
    R.push({ i, plus, ausgl, zulage, bsz: r.bsz, heute: r.heute, vorschlag: r.vorschlag, sumH: r.sumH, ausg: r.ausg, ausgUeb: r.ausgUeb,
      mwst: r.mwst + pl.leist * A.MwStQ, mwstNeu: r.mwstNeu + pl.leist * mwstSatzNeu, konsum: r.konsum + pl.leist, konsumLeist: pl.leist, verf: verf0[i], einkommen: r.einkommen + extra, tauM, tauLang,
      mietw: r.mietw, alt: r.alt, pw: r.pw, atg: r.atg, kk: r.kk, pq: r.pq, kapKons: kapN[i] * kq(i), ueberS: ueber2 > 0,
      svNeu: r.svNeu, gut: r.gut, teile: { ausSum: r.ausSum, agRP: r.agRP, rentePlus: r.rentePlus, gsPlus: r.gsPlus, anr: r.anr, bsz: r.bsz } });
  }
  // 3) Erbschaften: Nachlässe aus Vermögen und Sterblichkeit, heute und mit Staatsanteil (Dauerzustand, Mrd. € im Jahr)
  const erbe = erbschaften(opt, sp, n);
  // 4) Verhalten: Plus ausgeben, Minus einsparen, Rest anlegen und später ausgeben oder vererben
  const verh = verhalten(opt, sp, R, erbe);
  return { opt, a0, R, erbe, verh, n, pop, verfSumme: verfSumme / 1e9 };
}

function q(opt, a) { return Math.min(1, opt.q65 * Math.exp(opt.gompertz * (a - 65))); }

function erbstHeute(teil, betrieb, immo) {   // Steuerklasse I je Kind: Freibetrag 400.000 €, Sätze 7 bis 30 %; Betriebe zu 85 % verschont,
  // Immobilien im Mittel mit drei Vierteln des Marktwerts bewertet
  teil -= 0.25 * immo;
  const stufen = [[75000, 0.07], [300000, 0.11], [600000, 0.15], [6e6, 0.19], [13e6, 0.23], [26e6, 0.27], [Infinity, 0.30]];
  const verschont = teil > 26e6 ? 0.7 : 0.85;
  const x = Math.max(0, teil - betrieb * verschont - 400000);
  const satz = stufen.find(s => x <= s[0])[1];
  return x * satz;
}

function erbschaften(opt, sp, n) {
  const E = { nachlass: new Float64Array(n), rate: new Float64Array(n), heute: new Float64Array(n), anspruch: new Float64Array(n), schenk: new Float64Array(n) };
  for (let i = 0; i < n; i++) {
    if (sp.typ[i] === "kind_erw") continue;
    const a = sp.alter[i];
    const h = sp.erw[i] === 2 ? opt.paarFaktor * q(opt, a + opt.paarVersatz) : q(opt, a);
    const W = Math.max(0, sp.W[i]);
    const k = sp.kinderlos[i] ? 0 : opt.kinderJeNachlass;
    const betrieb = sp.betrieb[i];
    // heute
    let st;
    if (k > 0) st = k * erbstHeute(W / k, betrieb / k, (sp.hauswert[i] + sp.immo[i]) / k);
    else st = Math.max(0, W - opt.andFrei - 0.85 * betrieb) * 0.3;
    // Reform: Staatsanteil über dem Familienfreibetrag (ein Viertel mehr je weiterem Kind), sonst über dem Freibetrag für andere
    const frei = k > 0 ? opt.famFrei * (1 + opt.famKindQ * (k - 1)) : opt.andFrei * 2;
    const ans = opt.staatsanteil * Math.max(0, W - frei);
    E.rate[i] = h; E.nachlass[i] = h * W; E.heute[i] = h * st; E.anspruch[i] = h * ans;
    // Schenkungen großer Vermögen (heute weitgehend wie Erbschaft besteuert, Freibeträge alle zehn Jahre neu)
    E.schenk[i] = opt.schenkungQ * Math.max(0, W - 5e5);
    // Schenkungen: heute im Mittel rund 4 % Steuer (Freibeträge alle zehn Jahre, Betriebe verschont); im Vorschlag wie ein Erbe,
    // der Freibetrag ist bei großen Vermögen meist schon verbraucht (80 % über dem Freibetrag)
    E.heute[i] += opt.schenkSatzHeute * E.schenk[i];
    E.anspruch[i] += opt.staatsanteil * 0.8 * E.schenk[i];
  }
  return E;
}

function verhalten(opt, sp, R, E) {
  const n = R.length;
  let mpc = opt.mpc.slice();
  if (opt.mpcMittelZiel != null) {
    let s = 0, p = 0;
    for (const r of R) { if (r.plus > 0) { const j = stufeVon(sp.W[r.i]); const m = sp.transfer[r.i] > 0 ? opt.mpcGrundsicherung : mpc[j]; s += sp.w[r.i] * r.plus * m; p += sp.w[r.i] * r.plus; } }
    const f = opt.mpcMittelZiel / (s / p);
    mpc = opt.mpcMittelZiel >= 1 ? mpc.map(() => 1) : mpc.map(x => Math.min(1, x * f));
  }
  const V = [];
  for (const r of R) {
    const i = r.i, j = stufeVon(sp.W[i]);
    let ausgegeben = 0, gekuerzt = 0, angelegt = 0;
    if (r.plus >= 0) { const m = sp.transfer[i] > 0 ? opt.mpcGrundsicherung : mpc[j]; ausgegeben = m * r.plus; angelegt = r.plus - ausgegeben; }
    else { gekuerzt = opt.kuerzung[j] * -r.plus; angelegt = r.plus + gekuerzt; }   // negativ: es wird weniger angelegt oder entspart
    let b = Math.min(0.95, opt.vererbt[j] + (sp.rentner[i] ? opt.vererbtAlter : 0));
    if (r.plus < 0 && opt.minusAusErbe != null) b = opt.minusAusErbe;
    if (r.plus >= 0 && opt.plusVererbt != null) b = opt.plusVererbt;
    // Steuer, die das Angelegte später bringt: selbst ausgegeben mit Ausgabensteuer und Mehrwertsteuer, vererbt mit dem Staatsanteil,
    // soweit der Nachlass über dem Freibetrag liegt (langfristig fällig zum Anteil realLang)
    const k = sp.kinderlos[i] ? 0 : opt.kinderJeNachlass;
    const frei = k > 0 ? opt.famFrei * (1 + opt.famKindQ * (k - 1)) : opt.andFrei * 2;
    const ueberFrei = sp.W[i] > frei ? 1 : 0;
    const spaeter = angelegt * ((1 - b) * r.tauLang + b * opt.staatsanteil * ueberFrei * opt.realLang);
    V.push({ i, j, ausgegeben, gekuerzt, angelegt, steuerJetzt: (ausgegeben - gekuerzt) * r.tauM, steuerSpaeter: spaeter, b });
  }
  return { mpc, V };
}

// ---------------------------------------------------------------- Auswertung
function auswerten(erg) {
  const { R, pop, verh, erbe, opt } = erg;
  const sp = pop.spalten;
  const w = sp.w;
  const hh = i => sp.typ[i] !== "kind_erw";
  const S = (f, filt = () => true) => { let s = 0; for (const r of R) if (filt(r)) s += w[r.i] * f(r); return s; };
  const mrd = x => x / 1e9;
  const nHH = S(() => 1, r => hh(r.i));
  // Haushalte: Plus des Haushalts samt erwachsener Kinder wird hier je Steuerfall gezählt; „Haushalte“ = ohne die Kinder-Fälle
  const monat = r => r.plus / 12;
  const kach = {
    mehr: S(() => 1, r => hh(r.i) && monat(r) > 0.5) / nHH,
    gleich: S(() => 1, r => hh(r.i) && Math.abs(monat(r)) <= 0.5) / nHH,
    weniger20: S(() => 1, r => hh(r.i) && monat(r) < -0.5 && monat(r) >= -20) / nHH,
    weniger100: S(() => 1, r => hh(r.i) && monat(r) < -20 && monat(r) >= -100) / nHH,
    wenigerMehr: S(() => 1, r => hh(r.i) && monat(r) < -100) / nHH,
  };
  const wenigerN = S(() => 1, r => hh(r.i) && monat(r) < -0.5);
  const wenigerSum = S(r => -r.plus, r => hh(r.i) && monat(r) < -0.5);
  const plusSum = S(r => r.plus, r => r.plus > 0);
  const minusSum = S(r => -r.plus, r => r.plus < 0);
  const bs = S(r => r.bsz), bsN = S(() => 1, r => r.bsz > 0);
  const zul = S(r => r.zulage), zulN = S(() => 1, r => r.zulage > 0);
  const auf = {
    ausgabensteuer_start: mrd(S(r => r.ausgUeb)), ausgabensteuer_lang: mrd(S(r => r.ausg)),
    mwst_heute: mrd(S(r => r.mwst)), mwst_neu: mrd(S(r => r.mwstNeu)),
    est_heute: mrd(S(r => r.heute.est)), sv_heute: mrd(S(r => r.heute.sv)), kap_heute: mrd(S(r => r.heute.kap)),
    konsum: mrd(S(r => r.konsum)), mietwert_steuerpflichtig: mrd(S(r => r.mietw)), altvermoegen: mrd(S(r => r.alt)),
  };
  // nach Vermögensstufe
  const namen = ["unter 100.000 €", "100.000–200.000 €", "200.000–400.000 €", "400.000–800.000 €", "800.000 € – 1 Mio. €", "1–10 Mio. €", "10–100 Mio. €", "über 100 Mio. €"];
  const stufen = namen.map((name, j) => {
    const f = r => hh(r.i) && stufeVon(sp.W[r.i]) === j;
    const N = S(() => 1, f);
    const V = verh.V;
    const SV = (g) => { let s = 0; for (const v of V) if (f(R[v.i])) s += w[v.i] * g(v); return s; };
    return {
      stufe: name, haushalte_mio: N / 1e6, vermoegen_bio: S(r => sp.W[r.i], f) / 1e12,
      einkommen_mittel: S(r => r.einkommen, f) / N, konsum_mittel: S(r => r.konsum, f) / N,
      heute_mittel: S(r => r.sumH, f) / N,
      plus_monat_mittel: S(r => r.plus, f) / N / 12,
      anteil_mehr: S(() => 1, r => f(r) && r.plus / 12 > 0.5) / N,
      anteil_weniger: S(() => 1, r => f(r) && r.plus / 12 < -0.5) / N,
      plus_mrd: mrd(S(r => Math.max(0, r.plus), f)), minus_mrd: mrd(S(r => Math.max(0, -r.plus), f)),
      erbst_heute_mrd: mrd(SI(erbe.heute, f)), staatsanteil_anspruch_mrd: mrd(SI(erbe.anspruch, f)), nachlass_mrd: mrd(SI(erbe.nachlass, f)),
      steuer_jetzt_mrd: mrd(SV(v => v.steuerJetzt)), steuer_spaeter_mrd: mrd(SV(v => v.steuerSpaeter)),
      ausgegeben_mrd: mrd(SV(v => v.ausgegeben)), gekuerzt_mrd: mrd(SV(v => v.gekuerzt)), angelegt_mrd: mrd(SV(v => v.angelegt)),
    };
  });
  function SI(arr, f) { let s = 0; for (const r of R) if (f(r)) s += w[r.i] * arr[r.i]; return s; }
  // Verhalten gesamt
  const V = verh.V;
  const SVg = g => { let s = 0; for (const v of V) s += w[v.i] * g(v); return s; };
  const ausgegeben = SVg(v => v.ausgegeben), gekuerzt = SVg(v => v.gekuerzt), angelegtPlus = SVg(v => Math.max(0, v.angelegt)), angelegtMinus = SVg(v => Math.min(0, v.angelegt));
  const verhalten = {
    plus_mrd: mrd(plusSum), minus_mrd: mrd(minusSum),
    ausgegeben_mrd: mrd(ausgegeben), anteil_ausgegeben: ausgegeben / plusSum,
    gekuerzt_mrd: mrd(gekuerzt), anteil_gekuerzt: gekuerzt / minusSum,
    angelegt_mrd: mrd(angelegtPlus), weniger_angelegt_mrd: mrd(-angelegtMinus),
    steuer_jetzt_mrd: mrd(SVg(v => v.steuerJetzt)),
    steuer_jetzt_aus_plus_mrd: mrd(SVg(v => v.ausgegeben * R[v.i].tauM)), steuer_jetzt_aus_minus_mrd: mrd(-SVg(v => v.gekuerzt * R[v.i].tauM)),
    steuer_spaeter_mrd: mrd(SVg(v => v.steuerSpaeter)),
    mpc_je_stufe: verh.mpc,
  };
  const erbschaft = {
    nachlaesse_mio: SI(erbe.rate, r => hh(r.i)) / 1e6, nachlass_mrd: mrd(SI(erbe.nachlass, r => hh(r.i))),
    schenkungen_mrd: mrd(SI(erbe.schenk, r => hh(r.i))),
    erbst_heute_mrd: mrd(SI(erbe.heute, r => hh(r.i))),
    staatsanteil_anspruch_mrd: mrd(SI(erbe.anspruch, r => hh(r.i))),
    staatsanteil_start_mrd: mrd(SI(erbe.anspruch, r => hh(r.i))) * opt.realStart,
    staatsanteil_lang_mrd: mrd(SI(erbe.anspruch, r => hh(r.i))) * opt.realLang,
  };
  // Einkommenszehntel (je Haushalt, ohne Kinder-Fälle, Haushaltseinkommen vor Steuern)
  const hhR = R.filter(r => hh(r.i)).sort((a, b) => a.einkommen - b.einkommen);
  let cw = 0; const zehntel = Array.from({ length: 10 }, () => ({ N: 0, plus: 0, mehr: 0, weniger: 0, heute: 0, eink: 0, W: 0 }));
  for (const r of hhR) {
    const d = Math.min(9, Math.floor(10 * (cw + w[r.i] / 2) / nHH)); cw += w[r.i];
    const z = zehntel[d]; z.N += w[r.i]; z.plus += w[r.i] * r.plus; z.heute += w[r.i] * r.sumH; z.eink += w[r.i] * r.einkommen; z.W += w[r.i] * sp.W[r.i];
    if (r.plus / 12 > 0.5) z.mehr += w[r.i]; if (r.plus / 12 < -0.5) z.weniger += w[r.i];
  }
  const zt = zehntel.map((z, k) => ({ zehntel: k + 1, einkommen_mittel: z.eink / z.N, vermoegen_mittel: z.W / z.N, heute_mittel: z.heute / z.N,
    plus_monat_mittel: z.plus / z.N / 12, anteil_mehr: z.mehr / z.N, anteil_weniger: z.weniger / z.N }));
  return {
    haushalte_mio: nHH / 1e6, erwachsene_mio: S(r => sp.erw[r.i]) / 1e6, sparquote_achse: erg.a0, verfuegbar_mrd: erg.verfSumme,
    sparquote: 1 - mrd(S(r => r.konsum)) / erg.verfSumme,
    kacheln_100: Object.fromEntries(Object.entries(kach).map(([k, v]) => [k, Math.round(1000 * v) / 10])),
    weniger: { mio: wenigerN / 1e6, monat_mittel: wenigerSum / wenigerN / 12 },
    plus_mrd: mrd(plusSum), minus_mrd: mrd(minusSum),
    bestandsschutz: { mrd: mrd(bs), mio: bsN / 1e6, monat: bs / bsN / 12 },
    beamte_zulage: { mrd: mrd(zul), mio: zulN / 1e6 },
    aufkommen: auf, erbschaft, verhalten, stufen, zehntel: zt,
  };
}

if (typeof module !== "undefined") module.exports = { STANDARD, rechne, auswerten, stufeVon };
