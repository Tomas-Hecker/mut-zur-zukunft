#!/usr/bin/env python3
"""Tomas 28.11.2026, 13:02 UTC: Alle zinslosen Raten steigen jedes Jahr um 2 % (Rechenmodell rate-steigend-2026-11-28).
Der Rechner rechnet in heutigen Preisen: Eine Rate, die um 2 % im Jahr steigt, bleibt in Kaufkraft gleich. Die erste Rate
ist K × g / ((1 + g)^n − 1); entgangene Zinsen auf den Bestand in Euro des jeweiligen Jahres, auf heutige Preise umgerechnet.
Läuft nach sanierung-mietshaus-v41.py."""
import sys
P = 'steuerrechner/index.html'
s = open(P, encoding='utf-8').read()
if 'RateSteig' in s:
    print('schon drin'); sys.exit()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a)); s = s.replace(a, b)
rep('LaufF: 40, LaufH: 50, HalbJ: 30,', 'LaufF: 40, LaufH: 50, HalbJ: 30, RateSteig: 0.02,   // Raten steigen jedes Jahr um 2 % (Tomas 28.11.2026)\n ')
rep('tilgT = Tn / (LT - SAN.TilgFrei), tilgH = Hn / SAN.LaufH, tilgF = 0;',
    'g = SAN.RateSteig, rate1 = (K0, n) => g > 0 ? K0 * g / (Math.pow(1 + g, n) - 1) : K0 / n, tilgT = rate1(Tn, LT - SAN.TilgFrei), tilgH = rate1(Hn, SAN.LaufH), tilgF = 0;   // erste Rate; in heutigen Preisen bleibt sie gleich')
rep('const q = qJ(jahr + t - 1), tT = t > SAN.TilgFrei && restT > 1e-6 ? tilgT : 0, tH = restH > 1e-6 ? tilgH : 0;\n    zinsR += (restT + restH) * A.ZinsStart; restT -= tT; restH -= tH;',
    'const q = qJ(jahr + t - 1), tT = t > SAN.TilgFrei && restT > 1e-6 ? tilgT : 0, tH = restH > 1e-6 ? tilgH : 0, inf = Math.pow(1 + g, t - 1);\n'
    '    zinsR += (restT + restH) * A.ZinsStart / inf; restT -= tT * Math.pow(1 + g, Math.max(0, t - 1 - SAN.TilgFrei)) * (tT > 0); restH -= tH * inf;   // Bestand in Euro des Jahres')
rep('kred = [r.Tn > 0 ? `Wärmepumpe ${sEur(r.Tn)} über ${r.LT - SAN.TilgFrei} Jahre nach ${SAN.TilgFrei} ohne Tilgung` : "", r.Hn > 0 ? `Einbau, Heizkörper und Rohre ${sEur(r.Hn)} über ${SAN.LaufH} Jahre` : ""].filter(Boolean).join(", ");',
    'kred = [r.Tn > 0 ? `Wärmepumpe ${sEur(r.Tn)} über ${r.LT - SAN.TilgFrei} Jahre nach ${SAN.TilgFrei} ohne Tilgung` : "", r.Hn > 0 ? `Einbau, Heizkörper und Rohre ${sEur(r.Hn)} über ${SAN.LaufH} Jahre` : ""].filter(Boolean).join(", ") + (r.Tn + r.Hn > 0 ? `; die Rate steigt jedes Jahr um ${pct(SAN.RateSteig, 0)}, in heutigen Preisen bleibt sie gleich` : "");')
rep('Die Wärmepumpe ohne Einbau bezahlt ein zinsloser Kredit über 30 Jahre, die ersten 3 ohne Tilgung.',
    'Die Wärmepumpe ohne Einbau bezahlt ein zinsloser Kredit über 30 Jahre, die ersten 3 ohne Tilgung. Die Raten aller zinslosen Kredite steigen jedes Jahr um 2 %; gerechnet ist in heutigen Preisen, dort bleiben sie gleich, und der Aufschlag folgt ihnen, höchstens wie die Verbraucherpreise.')
open(P, 'w', encoding='utf-8').write(s); print('ok')
