#!/usr/bin/env python3
"""validate.py — structural (JSON Schema) + musical (taal arithmetic) validation."""
import json, glob, sys
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).parent.parent
OFFSET = {'S': 0, 'R': 2, 'G': 4, 'M': 5, 'P': 7, 'D': 9, 'N': 11}

def semitone(sw):
    o = OFFSET[sw['degree']]
    if sw.get('komal'): o -= 1
    if sw.get('kori'): o += 1
    return o + 12 * sw.get('saptak', 0)

def swara_name(sw):
    n = sw['degree']
    if sw.get('komal'): n = n.lower()
    if sw.get('kori'): n = 'M#'
    return n + {1: "'", -1: ","}.get(sw.get('saptak', 0), '')

def check(path):
    d = json.load(open(path, encoding='utf-8'))
    problems, warnings = [], []
    schema = json.load(open(ROOT / 'schema' / 'swaralipi.schema.json'))
    errs = list(Draft202012Validator(schema).iter_errors(d))
    for e in errs:
        problems.append(f"schema: {list(e.path)[:6]} {e.message[:90]}")
    taal = d['taal']
    notes_used = {}
    for ln in d['lines']:
        ncells = len(ln['cells'])
        for c in ln['cells']:
            for u in c['units']:
                if u['type'] == 'swara':
                    notes_used[swara_name(u['swara'])] = notes_used.get(swara_name(u['swara']), 0) + 1
        if not taal['talamukta']:
            m = taal['matras']
            if ncells % m != 0 and not ln.get('anacrusis'):
                # lines may end with pickup cells for the next cycle (as printed) — warn only
                warnings.append(f"line {ln['line_no']}: {ncells} matras not a multiple of {m}-matra cycle")
    # first unit of first non-anacrusis line should not be a bare sustain
    body = [l for l in d['lines'] if not l.get('anacrusis')]
    if body and body[0]['cells'][0]['units'][0]['type'] == 'sustain':
        warnings.append("first body line begins with a sustain")
    return d, problems, warnings, notes_used

if __name__ == '__main__':
    fail = False
    for f in sorted(glob.glob(str(ROOT / 'data' / 'songs' / '*.json'))):
        d, problems, warnings, notes = check(f)
        cyc = 'talamukta' if d['taal']['talamukta'] else f"{d['taal']['matras']}-matra {d['taal']['name']['translit']}"
        order = sorted(notes, key=lambda n: (0 if ',' in n else (2 if "'" in n else 1), 'SrRgGmMPdDnN'.find(n[0])))
        print(f"{d['id']:34s} {cyc:22s} notes: {' '.join(order)}")
        for p in problems: fail = True; print("   PROBLEM:", p)
        for w in warnings: print("   warn:", w)
    sys.exit(1 if fail else 0)
