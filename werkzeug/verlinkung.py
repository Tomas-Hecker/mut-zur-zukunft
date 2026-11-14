"""Verlinkung Buch <-> Rechner einbauen (Bausteine aus broschuere-mut-zur-zukunft/verlinkung/). Wiederholbar.
Läuft nach gen.py (Steuerrechner) und nach buch-bauen.py."""
import re, shutil
R = '/home/user/mut-zur-zukunft/'
V = '/mnt/project-files/broschuere-mut-zur-zukunft/verlinkung/'
shutil.copy(V + 'rechner-buchlinks.js', R + 'steuerrechner/buchlinks.js')
shutil.copy(V + 'tools-buchlinks.js', R + 'tools-buchlinks.js')
def tag(p, t):
    s = open(p).read()
    if t not in s:
        assert s.count('</body>') == 1, p
        s = s.replace('</body>', t + '\n</body>'); open(p, 'w').write(s)
tag(R + 'steuerrechner/index.html', '<script src="buchlinks.js"></script>')
for d in ['balkon-rechner', 'eauto-rechner', 'energie-rechner', 'heizungsrechner']:
    tag(R + d + '/index.html', '<script src="../tools-buchlinks.js"></script>')
for f, ext, a, b in [('buch.css', 'buch-rechnerlinks.css', '/* RECHNERLINKS ANFANG */', '/* RECHNERLINKS ENDE */'),
                     ('buch.js', 'buch-rechnerlinks.js', '/* RECHNERLINKS ANFANG */', '/* RECHNERLINKS ENDE */')]:
    p = R + 'buch/' + f; s = open(p).read()
    s = re.sub(re.escape(a) + '.*?' + re.escape(b) + '\n?', '', s, flags=re.S).rstrip('\n')
    s += '\n' + a + '\n' + open(V + ext).read().rstrip('\n') + '\n' + b + '\n'
    open(p, 'w').write(s)
print('verlinkung ok')
