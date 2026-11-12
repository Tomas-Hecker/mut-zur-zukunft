"""Hängt an alle Links auf das Buch-PDF ?v=<Prüfsumme>, damit Browser nach einem Update die neue Fassung laden."""
import hashlib, glob, re
PDF = 'Wir-koennen-uns-die-Zukunft-leisten.pdf'
v = hashlib.md5(open('buch/' + PDF, 'rb').read()).hexdigest()[:8]
for f in glob.glob('buch/*.html') + ['index.html']:
    s = open(f, encoding='utf-8').read()
    n = re.sub(re.escape(PDF) + r'(\?v=[0-9a-f]+)?"', f'{PDF}?v={v}"', s)
    if n != s: open(f, 'w', encoding='utf-8').write(n)
print('PDF-Version', v)
