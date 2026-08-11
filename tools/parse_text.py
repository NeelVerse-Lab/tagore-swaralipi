#!/usr/bin/env python3
"""parse_text.py — parse sargam-text (see render_text.py) back into Swaralipi-JSON lines.
Used for round-trip testing and for ingesting model-composed continuations."""
import re

DEGREES = {'S': 'S', 'R': 'R', 'G': 'G', 'M': 'M', 'P': 'P', 'D': 'D', 'N': 'N'}

def parse_swara(txt):
    txt = txt.strip()
    m = re.match(r"^(M#|[SRGMPDNsrgdn])([',]?)$", txt)
    if not m:
        raise ValueError(f"bad swara: {txt!r}")
    core, oct_ = m.groups()
    sw = {}
    if core == 'M#':
        sw = {'degree': 'M', 'kori': True}
    elif core.islower():
        sw = {'degree': core.upper(), 'komal': True}
        if core.upper() not in ('R', 'G', 'D', 'N'):
            raise ValueError(f"invalid komal: {txt!r}")
    else:
        sw = {'degree': core}
    sw['saptak'] = {"'": 1, ",": -1}.get(oct_, 0)
    return sw

def parse_unit(txt):
    txt = txt.strip()
    if txt == '-':
        return {'type': 'sustain'}
    if txt in ('·', 'x'):
        return {'type': 'rest'}
    kan = []
    m = re.match(r'^\(([^)]+)\)(.+)$', txt)
    if m:
        kt, txt = m.groups()
        # kan cluster: e.g. (N) or (S'R')
        for km in re.findall(r"M#[',]?|[SRGMPDNsrgdn][',]?", kt):
            kan.append(parse_swara(km))
    u = {'type': 'swara', 'swara': parse_swara(txt)}
    if kan:
        u['kan'] = kan
    return u

def parse_cell(txt):
    units = [parse_unit(p) for p in txt.split('/') if p.strip()]
    if not units:
        raise ValueError(f"empty cell: {txt!r}")
    return units

def parse_lines(text, section='antara'):
    """Parse alternating notation/lyric rows into schema line objects."""
    rows = []
    sec_of_row = []
    cur = section
    for r in text.splitlines():
        s = r.strip()
        if not s or s.startswith('#'):
            continue
        m = re.match(r'^\[([a-z0-9_]+)\]$', s)
        if m:
            cur = m.group(1)
            continue
        rows.append(r)
        sec_of_row.append(cur)
    out = []
    i = 0
    line_no = 1
    while i < len(rows):
        nrow = rows[i]
        lrow = rows[i + 1] if i + 1 < len(rows) else ''
        has_lyr = bool(re.search(r'[ঀ-৺]', lrow)) or (lrow.strip() and set(lrow.replace('|', '').split()) <= {'·', '৹'})
        ncells = [c for c in nrow.replace('|', ' ').split() if c]
        lcells = [c for c in lrow.replace('|', ' ').split() if c] if has_lyr else []
        cells = []
        for j, ct in enumerate(ncells):
            lyr = lcells[j] if j < len(lcells) else None
            melisma = lyr in ('৹', '·', None) or (lyr and all(ch in '৹·' for ch in lyr))
            cells.append({'units': parse_cell(ct),
                          'lyric': None if melisma else lyr,
                          'melisma': bool(melisma and lyr not in (None, '·'))})
        out.append({'line_no': line_no, 'section': sec_of_row[i], 'cells': cells, 'marks': []})
        line_no += 1
        i += 2 if has_lyr else 1
    return out
