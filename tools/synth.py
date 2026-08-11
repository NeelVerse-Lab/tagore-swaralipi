#!/usr/bin/env python3
"""synth.py — render Swaralipi-JSON to audio with a small additive synth.

No soundfonts, no external assets: a harmonium-flavoured additive voice
(odd-rich harmonic stack, soft attack, breath of vibrato) synthesised in numpy.
Sa is rendered at C#4 (~277 Hz), a common Rabindrasangeet tonic region.
"""
import json, sys, subprocess
from pathlib import Path
import numpy as np

ROOT = Path(__file__).parent.parent
SR = 44100
OFFSET = {'S': 0, 'R': 2, 'G': 4, 'M': 5, 'P': 7, 'D': 9, 'N': 11}
SA_HZ = 277.18  # C#4

def freq(sw):
    o = OFFSET[sw['degree']]
    if sw.get('komal'): o -= 1
    if sw.get('kori'): o += 1
    o += 12 * sw.get('saptak', 0)
    return SA_HZ * (2 ** (o / 12))

def events_of(doc):
    evs = []
    for ln in doc['lines']:
        for cell in ln['cells']:
            units = cell['units']
            frac = 1.0 / len(units)
            for u in units:
                if u['type'] == 'swara':
                    evs.append({'f': freq(u['swara']), 'dur': frac,
                                'kan': [freq(k) for k in u.get('kan', [])]})
                elif u['type'] == 'sustain' and evs:
                    evs[-1]['dur'] += frac
                else:
                    evs.append({'f': None, 'dur': frac, 'kan': []})
    return evs

def voice(f0, dur_s, amp=0.28):
    n = int(dur_s * SR)
    if n <= 0: return np.zeros(0)
    t = np.arange(n) / SR
    vib = 1 + 0.004 * np.sin(2 * np.pi * 5.4 * t)          # gentle vibrato
    phase = 2 * np.pi * f0 * np.cumsum(vib) / SR
    h = (1.00 * np.sin(phase) + 0.42 * np.sin(2 * phase) + 0.24 * np.sin(3 * phase)
         + 0.10 * np.sin(4 * phase) + 0.06 * np.sin(5 * phase))
    a = min(0.030, dur_s / 4); r = min(0.060, dur_s / 3)
    env = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    if na: env[:na] = np.linspace(0, 1, na)
    if nr: env[-nr:] *= np.linspace(1, 0, nr)
    return amp * h * env

def render(doc, matra_s=0.66, tanpura=True):
    evs = events_of(doc)
    total = sum(e['dur'] for e in evs) * matra_s + 1.0
    out = np.zeros(int(total * SR) + SR)
    pos = 0.0
    KAN_S = 0.07
    for e in evs:
        dur_s = e['dur'] * matra_s
        if e['f'] is None:
            pos += dur_s
            continue
        t0 = pos
        for kf in e['kan']:
            w = voice(kf, KAN_S, amp=0.2)
            i = int(t0 * SR); out[i:i+len(w)] += w
            t0 += KAN_S; dur_s -= KAN_S
        w = voice(e['f'], max(dur_s, 0.08))
        i = int(t0 * SR); out[i:i+len(w)] += w
        pos += e['dur'] * matra_s
    if tanpura:  # Sa-Pa drone bed
        t = np.arange(len(out)) / SR
        drone = 0.030 * np.sin(2*np.pi*SA_HZ/2*t) + 0.022 * np.sin(2*np.pi*SA_HZ*t) \
              + 0.014 * np.sin(2*np.pi*SA_HZ*1.5*t) + 0.010 * np.sin(2*np.pi*SA_HZ*2*t)
        fade = np.minimum(1, np.arange(len(out)) / (2*SR)) * np.minimum(1, (len(out)-np.arange(len(out))) / (2*SR))
        out += drone * fade
    peak = np.abs(out).max()
    if peak > 0: out = out / peak * 0.85
    return out

def write_wav(x, path):
    import wave, struct
    with wave.open(str(path), 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())

if __name__ == '__main__':
    songs = sys.argv[1:] or None
    outdir = ROOT / 'audio'
    outdir.mkdir(exist_ok=True)
    import glob
    for f in sorted(glob.glob(str(ROOT / 'data' / 'songs' / '*.json'))):
        doc = json.load(open(f, encoding='utf-8'))
        if songs and doc['id'] not in songs: continue
        matra = 0.9 if doc['taal']['talamukta'] else 0.66
        x = render(doc, matra_s=matra)
        wav = outdir / f"{doc['id']}.wav"
        write_wav(x, wav)
        mp3 = outdir / f"{doc['id']}.mp3"
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(wav), '-b:a', '160k', str(mp3)], check=True)
        wav.unlink()
        print('rendered', mp3.name, f"{len(x)/SR:.0f}s")
