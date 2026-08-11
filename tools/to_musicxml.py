#!/usr/bin/env python3
"""to_musicxml.py — derive MusicXML from Swaralipi-JSON via music21.

Lossy view: Sa mapped to C4, matra = quarter note, taal cycle = time signature
(12-matra ektaal -> 12/4, dadra -> 6/4, kaharba -> 8/4, tintal -> 16/4;
talamukta -> unmetered, notated in free 4/4 with a text direction).
Kan notes become grace notes; lyrics attach per note in Bengali.
"""
import json, glob
from fractions import Fraction
from pathlib import Path
from music21 import stream, note, meter, tempo, metadata, expressions, duration as m21dur

ROOT = Path(__file__).parent.parent
OFFSET = {'S': 0, 'R': 2, 'G': 4, 'M': 5, 'P': 7, 'D': 9, 'N': 11}

def m21_pitch(sw):
    o = OFFSET[sw['degree']]
    if sw.get('komal'): o -= 1
    if sw.get('kori'): o += 1
    return 60 + o + 12 * sw.get('saptak', 0)

def build(doc):
    s = stream.Part()
    s.append(tempo.MetronomeMark(number=84))
    taal = doc['taal']
    if taal['talamukta']:
        s.append(meter.TimeSignature('4/4'))
        s.append(expressions.TextExpression('talamukta (free rhythm)'))
    else:
        s.append(meter.TimeSignature(f"{taal['matras']}/4"))
    events = []  # (pitch|None, quarterLength(Fraction), lyric, kan_list)
    for ln in doc['lines']:
        for cell in ln['cells']:
            units = cell['units']
            frac = Fraction(1, len(units))
            first = True
            for u in units:
                if u['type'] == 'swara':
                    lyr = cell.get('lyric') if first else None
                    events.append([m21_pitch(u['swara']), frac, lyr,
                                   [m21_pitch(k) for k in u.get('kan', [])]])
                elif u['type'] == 'sustain' and events:
                    events[-1][1] += frac
                else:
                    events.append([None, frac, None, []])
                first = False
    for p, ql, lyr, kans in events:
        if p is None:
            n = note.Rest()
        else:
            n = note.Note(p)
            if lyr:
                n.lyric = lyr
        n.duration = m21dur.Duration(float(ql) if (ql.denominator & (ql.denominator - 1) == 0) else ql)
        if kans and p is not None:
            for k in reversed(kans):
                g = note.Note(k).getGrace()
                s.append(g)
        s.append(n)
    sc = stream.Score()
    sc.metadata = metadata.Metadata()
    sc.metadata.title = f"{doc['title']['bn']} ({doc['title']['translit']})"
    sc.metadata.composer = doc['composer']
    sc.append(s)
    return sc

if __name__ == '__main__':
    outdir = ROOT / 'derived' / 'musicxml'
    outdir.mkdir(parents=True, exist_ok=True)
    for f in sorted(glob.glob(str(ROOT / 'data' / 'songs' / '*.json'))):
        doc = json.load(open(f, encoding='utf-8'))
        sc = build(doc)
        out = outdir / f"{doc['id']}.musicxml"
        sc.write('musicxml', fp=str(out))
        print('wrote', out.name)
