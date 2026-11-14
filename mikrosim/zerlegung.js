// Warum haben Haushalte weniger? Zerlegung: derselbe Haushalt ohne Kapitalerträge und Mieten, ohne Verzehr von Erspartem, ohne Mietwert
const K = require("./kern.js"); const fs = require("fs"); const S = require("./simulation.js");
const pop = JSON.parse(fs.readFileSync(__dirname + "/bevoelkerung.json")); const opt = process.argv[2] ? JSON.parse(fs.readFileSync(process.argv[2])) : {};
const e = S.rechne(K, pop, opt); const sp = pop.spalten;
const grund = { kapital: 0, erspartes: 0, mietwert: 0, sonst: 0 }, grundM = { kapital: 0, erspartes: 0, mietwert: 0, sonst: 0 };
const nachTyp = {};
for (const r of e.R) {
  const i = r.i; if (sp.typ[i] === "kind_erw" || r.plus / 12 >= -0.5) continue;
  const w = sp.w[i];
  // ohne Kapitalerträge: Konsum um den Teil kürzen, der aus ihnen kam
  const p2 = { ...pop, n: 1, spalten: Object.fromEntries(Object.entries(sp).map(([k, v]) => [k, [v[i]]])) };
  const t = (mod) => { const q = structuredClone(p2); for (const [k, v] of Object.entries(mod)) q.spalten[k] = [v]; return q; };
  let g = "sonst";
  const ohneKap = S.rechne(K, t({ kap: 0, aus: 0, vermietCash: 0, vermiet: 0, gmbh: 0 }), { ...opt, eichung: "fest", a0fest: e.a0 }).R[0].plus;
  if (ohneKap >= -6) g = "kapital";
  else { const ohneVerm = S.rechne(K, t({ kap: 0, aus: 0, vermietCash: 0, vermiet: 0, gmbh: 0, verm: 0, geld: 0 }), { ...opt, eichung: "fest", a0fest: e.a0 }).R[0].plus;
    if (ohneVerm >= -6) g = "erspartes";
    else { const ohneMiet = S.rechne(K, t({ kap: 0, aus: 0, vermietCash: 0, vermiet: 0, gmbh: 0, verm: 0, geld: 0, miet: 0, hb: 0 }), { ...opt, eichung: "fest", a0fest: e.a0 }).R[0].plus; if (ohneMiet >= -6) g = "mietwert"; } }
  grund[g] += w; grundM[g] += w * r.plus;
  const ty = sp.typ[i].startsWith("rentner") ? "Rentner" : "Erwerbsalter"; nachTyp[ty + "/" + g] = (nachTyp[ty + "/" + g] || 0) + w;
}
for (const k in grund) console.log(k.padEnd(10), (grund[k] / 1e6).toFixed(2), "Mio.", Math.round(grundM[k] / grund[k] / 12), "€/Monat");
console.log(Object.fromEntries(Object.entries(nachTyp).map(([k, v]) => [k, Math.round(v / 1e5) / 10])));
if (process.env.SONST) { let c = 0; for (const r of e.R) { const i = r.i; if (sp.typ[i] === "kind_erw" || r.plus / 12 >= -100 || sp.rentner[i] || sp.kap[i] + sp.vermietCash[i] + sp.aus[i] > 500 || sp.eigen[i]) continue; if (c++ < 12) console.log(JSON.stringify({ typ: sp.typ[i], l1: Math.round(sp.lohn1[i]), l2: Math.round(sp.lohn2[i]), gew: Math.round(sp.gewinn[i]), pens: Math.round(sp.pension[i]), beamt: sp.beamter[i], selbst: sp.selbst[i], pkv: sp.pkv[i], mini: Math.round(sp.mini[i]), leist: Math.round(sp.leist[i]), verf: Math.round(r.verf), konsum: Math.round(r.konsum), plusM: Math.round(r.plus / 12) })); } }
