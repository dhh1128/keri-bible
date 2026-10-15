"""Assemble bible/*.md into keri-bible.md.

The chapters carry permanent anchors that are unique only within a chapter ({#thesis} appears in
all of them), so the assembled file prefixes each anchor with its chapter number and rewrites links
to match: `{#edges}` in chapter 05 becomes `{#05-edges}`, and a link to
`05-acdc-and-verifiable-data.md#edges` becomes `#05-edges`. The marker legend is taken from
docs/house-style.md, which is the single place it is written, and placed once after the contents.
"""
import glob, io, re, sys

ANCHOR = re.compile(r'\{#([a-z0-9-]+)\}')
XLINK = re.compile(r'\]\((\d\d)-[a-z0-9-]+\.md#([a-z0-9-]+)\)')
LOCAL = re.compile(r'\]\(#([a-z0-9-]+)\)')
HEADING = re.compile(r'^# (.*?)\s*\{#([a-z0-9-]+)\}\s*$')


def legend():
    style = open('docs/house-style.md', encoding='utf-8').read()
    body = style.split('\n## Provenance markers\n', 1)[1].split('\n## ', 1)[0]
    body = body.replace(' This section is the legend that `build-bible.py` and the site generate from.', '')
    return '## Provenance markers {#legend}\n' + body.rstrip('\n') + '\n'


def chapter(path):
    nn = path.split('/')[-1][:2]
    text = open(path, encoding='utf-8').read().rstrip('\n')
    out, fence = [], False
    for line in text.split('\n'):
        if line.startswith('```'):
            fence = not fence
        if not fence:
            line = ANCHOR.sub(lambda m: '{#%s-%s}' % (nn, m.group(1)), line)
            line = LOCAL.sub(lambda m: '](#%s-%s)' % (nn, m.group(1)), line)
            line = XLINK.sub(lambda m: '](#%s-%s)' % (m.group(1), m.group(2)), line)
        out.append(line)
    title, anchor = HEADING.match(out[0]).groups()
    return title, anchor, '\n'.join(out)


chapters = [chapter(p) for p in sorted(glob.glob('bible/*.md'))]
out = io.StringIO()
out.write('# The KERI Bible\n\n## Table of Contents\n\n')
for title, anchor, _ in chapters:
    out.write(f'- [{title}](#{anchor})\n')
out.write('\n---\n\n' + legend())
for _, _, body in chapters:
    out.write('\n---\n\n' + body + '\n')
sys.stdout.write(out.getvalue())
