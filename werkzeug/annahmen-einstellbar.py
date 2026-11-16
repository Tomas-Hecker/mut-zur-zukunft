#!/usr/bin/env python3
"""Steuerrechner: Jede Zahl in „Woher die Zahlen kommen“ lässt sich ändern. Statt des festen Werts steht ein Eingabefeld;
eine Änderung rechnet alles neu (Haushalt, Gesamtrechnung, Schulden, CO₂). „Buch: …“ zeigt den Wert aus dem Buch,
ein Knopf setzt alles zurück. Läuft nach jedem Neubau des Steuerrechners (gen.py); ein zweiter Lauf ändert nichts."""
p = 'steuerrechner/index.html'
s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
if 'qin' not in s:
    rep('''      const wert = geaendert ? `${fmtQ(A[k], u)}<small class="qalt">Buch: ${esc(anz)}</small>` : esc(anz);''',
        '''      const wert = u && k in A && typeof A[k] === "number"
            ? `<span class="qe"><input class="qin" type="number" step="any" inputmode="decimal" data-k="${esc(k)}" data-u="${u}" value="${qAnz(A[k], u)}" aria-label="${esc(lbl)}"><span class="qu">${Q_EINH[u] || ""}</span></span>`
              + (geaendert ? `<small class="qalt">Buch: ${esc(anz)} <button type="button" class="qback" data-k="${esc(k)}">zurück</button></small>` : "")
            : esc(anz);''')
    rep('''  box.querySelectorAll("details").forEach(d => d.addEventListener("toggle", postHeight));''',
        '''  box.querySelectorAll("details").forEach(d => d.addEventListener("toggle", postHeight));
      box.querySelectorAll(".qin").forEach(el => el.addEventListener("change", () => {
        const v = parseFloat(String(el.value).replace(",", ".")); if (!isFinite(v)) return;
        A[el.dataset.k] = el.dataset.u === "pct" ? v / 100 : v; qNeu(el.dataset.k);
      }));
      box.querySelectorAll(".qback").forEach(b => b.onclick = () => { A[b.dataset.k] = A0[b.dataset.k]; qNeu(b.dataset.k); });
      const n = Object.keys(A0).filter(k => typeof A0[k] === "number" && A[k] !== A0[k]).length;
      $("qreset").hidden = !n; $("qreset").textContent = "Alle Annahmen auf die Werte aus dem Buch zurücksetzen";''')
    rep('''function renderQuellen() {''', '''const Q_EINH = { eur: "€", eurm: "€/Monat", mrd: "Mrd. €", mio: "Mio.", pct: "%", pkt: "Punkte", std: "Std.", jahre: "Jahre", eurkg: "€/kg", miot: "Mio. t" };
    const qAnz = (v, u) => u === "pct" ? +(v * 100).toFixed(4) : +v.toFixed(6);
    function qNeu(k) {   // nach einer Änderung alles neu rechnen, Fokus auf der Zeile halten
      updateAll();
      const z = document.getElementById("ann-" + k), el = z && z.querySelector(".qin"); if (el) el.focus({ preventScroll: true });
    }
    function renderQuellen() {''')
    rep('''<div class="qgroups" id="qgroups">''', '''<button type="button" id="qreset" class="qreset" hidden onclick="for (const k in A0) if (typeof A0[k] === 'number') A[k] = A0[k]; updateAll();"></button>
    <div class="qgroups" id="qgroups">''')
    rep('''table.q td:nth-child(2) { white-space: nowrap; font-weight: 600; }''',
        '''table.q td:nth-child(2) { white-space: nowrap; font-weight: 600; }
    .qe { display: inline-flex; align-items: center; gap: 4px; }
    .qin { width: 7.5em; padding: 4px 6px; font: inherit; font-weight: 600; text-align: right; border: 1px solid var(--line); border-radius: 6px; background: var(--card, #fff); color: inherit; }
    .qin:focus { outline: 2px solid var(--accent); outline-offset: 1px; }
    .qu { font-weight: 400; color: var(--muted); font-size: .86rem; }
    .qalt .qback { margin-left: 4px; padding: 0 6px; font-size: .8rem; border: 1px solid var(--line); border-radius: 999px; background: none; color: inherit; cursor: pointer; }
    .qreset { margin: 8px 0 12px; padding: 8px 14px; border-radius: 999px; border: 1px solid var(--accent); background: none; color: var(--accent); font: inherit; font-weight: 600; cursor: pointer; }''')

# Schritt 2: auch Werte ohne Einheitenangabe einstellbar machen; Einheit aus dem angezeigten Wert ablesen

if 'qEinh' not in s:
    rep('''      const wert = u && k in A && typeof A[k] === "number"
            ? `<span class="qe"><input class="qin" type="number" step="any" inputmode="decimal" data-k="${esc(k)}" data-u="${u}" value="${qAnz(A[k], u)}" aria-label="${esc(lbl)}"><span class="qu">${Q_EINH[u] || ""}</span></span>`''',
        '''      const qe = typ !== "Berechnet" && k in A && typeof A0[k] === "number" ? qEinh(anz, A0[k], u) : null;
      const wert = qe
        ? `<span class="qe"><input class="qin" type="number" step="any" inputmode="decimal" data-k="${esc(k)}" data-u="${qe.u}" value="${qAnz(A[k], qe.u)}" aria-label="${esc(lbl)}"><span class="qu">${esc(qe.t)}</span></span>`''')
    rep('''const qAnz = (v, u) =>''', '''// Einheit eines Werts: aus der Liste oder aus dem angezeigten Wert („25 %“, „30 Jahren“, „4,9 Mrd. €“); sonst nicht einstellbar
function qEinh(anz, v, u) {
  if (u && Q_EINH[u] !== undefined) return { u, t: Q_EINH[u] };
  const m = String(anz).match(/^ *(-?[0-9.]*,?[0-9]+) *(.*)$/); if (!m) return null;
  const x = parseFloat(m[1].replace(/[.]/g, "").replace(",", ".")), t = m[2].trim();
  if (!isFinite(x)) return null;
  const nah = (a, b) => Math.abs(a - b) <= 1e-6 * Math.max(1, Math.abs(b)) + 0.005 * Math.abs(b);
  if (t.startsWith("%") && nah(x / 100, v)) return { u: "pct", t };
  if (nah(x, v)) return { u: "x", t };
  return null;
}
const qAnz = (v, u) =>''')
open(p, 'w', encoding='utf-8').write(s)
print('Annahmen einstellbar')
