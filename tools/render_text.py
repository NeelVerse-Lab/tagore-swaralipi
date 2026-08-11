#!/usr/bin/env python3
"""render_text.py — human-readable sargam text view of Swaralipi-JSON.

Compact notation ("sargam-text"):
  cell separator      : space          vibhag separator : |
  units within a cell : /              sustain          : -
  komal               : lowercase      kori Ma          : M#
  tara saptak         : trailing '     udara saptak     : trailing ,
  kan (grace)         : (X) prefix     lyric row        : aligned under cells
"""
import json, glob, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

def swara_txt(sw):
    n = sw['degree']
    if sw.get('komal'): n = n.lower()
    if sw.get('kori'): n = 'M#'
    return n + {1: "'", -1: ","}.get(sw.get('saptak', 0), '')

def unit_txt(u):
    if u['type'] == 'sustain': return '-'
    if u['type'] == 'rest': return '·'
    t = swara_txt(u['swara'])
    if u.get('kan'):
        t = '(' + ''.join(swara_txt(k) for k in u['kan']) + ')' + t
    return t

def cell_txt(c):
    return '/'.join(unit_txt(u) for u in c['units'])

def render(doc, lyrics=True):
    out = [f"# {doc['title']['bn']}  ({doc['title']['translit']})"]
    t = doc['taal']
    if t['talamukta']:
        out.append("# taal: talamukta (free rhythm)")
        vib = None
    else:
        out.append(f"# taal: {t['name']['translit']} — {t['matras']} matras, vibhags {t['vibhags']}")
        vib = t['vibhags']
    prev_sec = None
    for ln in doc['lines']:
        if ln['section'] != prev_sec:
            out.append(f"\n[{ln['section']}]")
            prev_sec = ln['section']
        cells = [cell_txt(c) for c in ln['cells']]
        lyrs = [(c['lyric'] or ('৹' if c['melisma'] else '·')) for c in ln['cells']]
        widths = [max(len(a), len(b) if lyrics else 0) for a, b in zip(cells, lyrs)]
        # vibhag bars
        def bar_positions():
            if not vib: return set()
            pos, acc, i = set(), 0, 0
            while acc < len(cells):
                acc += vib[i % len(vib)]
                pos.add(acc)
                i += 1
            return pos
        bars = bar_positions()
        def fmt(row):
            parts = []
            for i, (txt, w) in enumerate(zip(row, widths)):
                parts.append(txt.ljust(w))
                if (i + 1) in bars and i + 1 < len(row):
                    parts.append('|')
            return '  '.join(parts)
        out.append(fmt(cells))
        if lyrics:
            out.append(fmt(lyrs))
    return '\n'.join(out) + '\n'

if __name__ == '__main__':
    outdir = ROOT / 'data' / 'text'
    outdir.mkdir(parents=True, exist_ok=True)
    for f in sorted(glob.glob(str(ROOT / 'data' / 'songs' / '*.json'))):
        doc = json.load(open(f, encoding='utf-8'))
        (outdir / f"{doc['id']}.txt").write_text(render(doc), encoding='utf-8')
        print('wrote', f"{doc['id']}.txt")
