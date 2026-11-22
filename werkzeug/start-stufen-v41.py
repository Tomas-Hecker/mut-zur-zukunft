#!/usr/bin/env python3
"""Nachträge vom 22.11.2026 zum Buch Version 41 im Steuerrechner (wie version-41/modell-v41, Kern vom 22.11.2026, Liesmich.md):
- Start in drei Stufen (StartStufen): Erziehung und Pflege als Bürgerjob im ersten Jahr mit einem Drittel des Lohns, im zweiten mit zwei
  Dritteln, dann ganz; bringt Elterngeld oder Pflegegeld mehr, gilt das Höhere (ep_eg_anrechnung). Der Berufscoach kommt ebenso in drei
  Stufen und zählt erst nach dem Verhalten (coach_stufen_j).
- Kleine Regeln aus der Rechtsprüfung (KleinAn): Kindergeld über 5.000 €, Erziehung in anderen EU-Staaten, Gleitzone erstes Zuhause,
  zählen nach dem Verhalten (klein_j).
Läuft nach abend-v41.py. Ein zweiter Lauf ändert nichts."""
import json
p = 'steuerrechner/index.html'
s = open(p, encoding='utf-8').read()
if 'Nachträge 22.11.2026' in s:
    raise SystemExit
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)
A = {"StartStufen": 1, "EPEGHochAnt": 0.2, "EPEGHochMon": 12, "EPEGRestMon": 15.5, "KleinAn": 1, "KleinKG": 1.54, "KleinEU": 0.6, "KleinGrESt": 0.7}
rep('const A = structuredClone(ANNAHMEN);', f'''// Nachträge 22.11.2026 (Buch Version 41): Start in drei Stufen, kleine Regeln aus der Rechtsprüfung
Object.assign(ANNAHMEN, {json.dumps(A)});
const A = structuredClone(ANNAHMEN);''')
rep('''function epKosten() {
  const L = A.EPLohn, geb = A.FamGeb * 1e6;''', '''// Nachtrag 22.11.2026: Stufe der neuen Leistungen im Jahr (1/3, 2/3, dann ganz) und angerechnetes Elterngeld je Kind in den Stufen
function startStufe(jahr) { return A.StartStufen ? Math.min(1, Math.max(0, (jahr - A.Prognose.ReformStart + 1) / 3)) : 1; }
function epEgAnrechnung(s = 1) {
  const voll = A.EPEG - A.EPEGUeber;
  if (s >= 1) return voll;
  const L = A.EPLohn, a = A.EPEGHochAnt, ma = A.EPEGHochMon, mb = A.EPEGRestMon, lo = A.EPEGMin;
  const hoch = L + A.EPEGUeber / (a * ma), hi = 2 * (A.EPEG - a * hoch * ma) / ((1 - a) * mb) - lo;
  const teil = c => { const cc = Math.max(lo, Math.min(hi, c)); return ((cc * cc - lo * lo) / 2 + c * (hi - cc)) / (hi - lo); };
  return a * Math.min(hoch, s * L) * ma + (1 - a) * mb * teil(s * L);
}
function coachStufenJ(k) { return A.StartStufen ? A.CoachAn * (A.CoachN * A.CoachK / 1e9 + A.KILernN * A.KILernEur * 12 / 1e3) * (1 - Math.min(1, k / 3)) : 0; }
function kleinJ(k) { return -(A.KleinAn || 0) * (A.KleinKG + A.KleinEU - A.KleinGrESt); }
function epKosten(s = 1) {
  const L = A.EPLohn * s, geb = A.FamGeb * 1e6;''')
rep('const eltern = (monate - A.EPGSElt * 12) * L - (geb * A.EPEGQuote * (A.EPEG - A.EPEGUeber) - A.EPGSElt * A.EPGSEltEG * 12 * A.EPEGMin);',
    'const eltern = (monate - A.EPGSElt * 12) * L - (geb * A.EPEGQuote * epEgAnrechnung(s) - A.EPGSElt * A.EPGSEltEG * 12 * Math.min(A.EPEGMin, L));')
rep('const [e, p] = epKosten(); return e + p * epPfl(jahr)', 'const [e, p] = epKosten(startStufe(jahr)); return e + p * epPfl(jahr)')
rep(' - strassenfondsJ(y) + gesundheitJ(y);   // Nachtrag 21.11.2026: Gesundheitsaufschlag;',
    ' - strassenfondsJ(y) + gesundheitJ(y) + coachStufenJ(y) + kleinJ(y);   // Nachträge 22.11.2026: Berufscoach in Stufen, kleine Regeln; Nachtrag 21.11.2026: Gesundheitsaufschlag;')
open(p, 'w', encoding='utf-8').write(s)
print('Nachträge 22.11.2026 eingebaut')
