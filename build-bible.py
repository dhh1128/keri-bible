import glob, re, sys, io

def anchor(t):
    a = t.lower()
    a = re.sub(r'[^\w\s-]', '', a)          # drop punctuation, keep word chars/space/hyphen
    a = a.replace(' ', '-')
    return a

files = sorted(glob.glob('bible/*.md'))
titles, bodies = [], []
for f in files:
    txt = open(f, encoding='utf-8').read().rstrip('\n')
    t = txt.split('\n', 1)[0].lstrip('# ').strip()
    titles.append(t); bodies.append(txt)

out = io.StringIO()
out.write('# The KERI Bible\n\n## Table of Contents\n\n')
for t in titles:
    out.write(f'- [{t}](#{anchor(t)})\n')
for b in bodies:
    out.write('\n---\n\n' + b + '\n')
sys.stdout.write(out.getvalue())
