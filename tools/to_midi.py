#!/usr/bin/env python3
"""to_midi.py — derive Standard MIDI Files from Swaralipi-JSON.

Derivation choices (documented, since MIDI is a lossy view):
  - Sa = C4 (MIDI 60); the corpus itself is tonic-free.
  - 1 matra = 1 quarter note. Default tempo 84 bpm (moderate laya);
    talamukta songs rendered at 60 bpm equivalents.
  - Kan (grace) notes take 1/8 matra, stolen from the front of the main note.
  - Sustains extend the previous note; melisma is inherent.
"""
import json, glob, sys
from pathlib import Path
import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage

ROOT = Path(__file__).parent.parent
OFFSET = {'S': 0, 'R': 2, 'G': 4, 'M': 5, 'P': 7, 'D': 9, 'N': 11}
TPQ = 480  # ticks per quarter (= per matra)

def midi_note(sw, tonic=60):
    o = OFFSET[sw['degree']]
    if sw.get('komal'): o -= 1
    if sw.get('kori'): o += 1
    return tonic + o + 12 * sw.get('saptak', 0)

def song_events(doc):
    """Flatten to [(midi_note or None, dur_in_matras, kan_list), ...]."""
    events = []
    for ln in doc['lines']:
        for cell in ln['cells']:
            units = cell['units']
            frac = 1.0 / len(units)
            for u in units:
                if u['type'] == 'swara':
                    events.append({'note': midi_note(u['swara']), 'dur': frac,
                                   'kan': [midi_note(k) for k in u.get('kan', [])]})
                elif u['type'] == 'sustain':
                    if events:
                        events[-1]['dur'] += frac
                    # leading sustain with nothing before: silence
                    else:
                        events.append({'note': None, 'dur': frac, 'kan': []})
                else:  # rest
                    events.append({'note': None, 'dur': frac, 'kan': []})
    return events

def to_midi(doc, out_path, bpm=84):
    if doc['taal']['talamukta']:
        bpm = 60
    mid = MidiFile(ticks_per_beat=TPQ)
    tr = MidiTrack(); mid.tracks.append(tr)
    tr.append(MetaMessage('track_name', name=doc['title']['translit'], time=0))
    tr.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm), time=0))
    tr.append(Message('program_change', program=73, time=0))  # flute-ish placeholder
    pending = 0
    KAN = TPQ // 8
    for ev in song_events(doc):
        ticks = int(round(ev['dur'] * TPQ))
        if ev['note'] is None:
            pending += ticks
            continue
        main_ticks = ticks
        for k in ev['kan']:
            tr.append(Message('note_on', note=k, velocity=70, time=pending)); pending = 0
            tr.append(Message('note_off', note=k, velocity=0, time=KAN))
            main_ticks -= KAN
        main_ticks = max(main_ticks, TPQ // 8)
        tr.append(Message('note_on', note=ev['note'], velocity=80, time=pending)); pending = 0
        tr.append(Message('note_off', note=ev['note'], velocity=0, time=main_ticks))
    mid.save(out_path)
    return sum(e['dur'] for e in song_events(doc))

if __name__ == '__main__':
    outdir = ROOT / 'derived' / 'midi'
    outdir.mkdir(parents=True, exist_ok=True)
    for f in sorted(glob.glob(str(ROOT / 'data' / 'songs' / '*.json'))):
        doc = json.load(open(f, encoding='utf-8'))
        total = to_midi(doc, outdir / f"{doc['id']}.mid")
        print(f"{doc['id']:36s} {total:6.1f} matras -> {doc['id']}.mid")
