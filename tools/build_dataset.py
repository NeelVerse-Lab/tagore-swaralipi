#!/usr/bin/env python3
"""Assemble canonical Swaralipi-JSON song files from parsed NLTR grids + curated metadata."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from parse_nltr import parse_song

ROOT = Path(__file__).parent.parent
RETRIEVED = "2026-08-11"

# Witness URLs must use the archive's precomposed Bengali nukta characters
# (য় ড় ঢ়). See tools/fetch_sources.py — Unicode NFC does not do this for you.

# Songs checked line-by-line against scans of the printed Swarabitan (Visva-Bharati),
# not only against the online witness. docs/VERIFICATION.md holds the full record:
# which page images were consulted, what matched, and every discrepancy found.
SCAN_VERIFIED = {
    "purano-sei-diner-katha": {
        "swarabitan_volume": 32,
        "song_number_in_volume": 16,
        "scan": "https://archive.org/details/in.ernet.dli.2015.339540",
        "checked": "2026-08-11",
        "scope": "lines 1-6 (sthayi through first antara): every matra and lyric syllable",
        "result": "exact match",
        "printed_header": "মিশ্র ভূপালী । একতাল",
        "notes": [
            "The printed header confirms ektaal and supplies a raga the online witness omits: Mishra Bhupali, a pentatonic raga — consistent both with the song's Auld Lang Syne origin and with the pentatonic note-set the data itself shows.",
            "Line 4, matra 5: the udara mark under the second ধা is ambiguous in this scan. We keep the witness reading (udara), which fits the surrounding low-register phrase.",
        ],
    },
    "bhalobese-sokhi": {
        "swarabitan_volume": 56,
        "song_number_in_volume": 19,
        "scan": "https://archive.org/details/in.ernet.dli.2015.336651",
        "checked": "2026-08-11",
        "scope": "lines 1-2 (sthayi): every matra and lyric syllable",
        "result": "exact match",
        "printed_header": "none — no raga/taal line is printed for this song",
        "notes": [
            "Resolves a conflict with a secondary source. geetabitan.com lists this song as Dadra; the printed page carries no taal line and no vibhag dandas anywhere in the notation, which is how Swarabitan sets a talamukta (free-rhythm) song. The talamukta reading stands.",
            "Three-note matras in the print (গমপা, গমগা) match the corpus's matra-fraction encoding exactly.",
        ],
    },
    "gram-chhara-oi-ranga-matir-path": {
        "swarabitan_volume": 9,
        "song_number_in_volume": 22,
        "scan": "https://archive.org/details/in.ernet.dli.2015.339565",
        "checked": "2026-08-11",
        "scope": "line 1 (sthayi): all 16 matras and lyric syllables",
        "result": "exact match",
        "printed_header": "বাংলা । কাহারবা",
        "notes": [
            "The printed header confirms kaharba and gives the anga as বাংলা (Bangla), correcting the 'Baul-anga' attribution previously recorded here from tradition rather than from a source.",
            "Validates the corpus's kan (grace-note) encoding: where we write a kan, the print sets the ornamenting swara as a smaller raised glyph (মগা) — the akarmatrik convention for kan.",
        ],
    },
}

TAALS = {
    "ektaal":  {"name": {"bn": "একতাল", "translit": "ektaal"}, "matras": 12, "vibhags": [3, 3, 3, 3],
                "beats": ["sam", "taali", "khali", "taali"], "talamukta": False},
    "dadra":   {"name": {"bn": "দাদরা", "translit": "dadra"}, "matras": 6, "vibhags": [3, 3],
                "beats": ["sam", "khali"], "talamukta": False},
    "kaharba": {"name": {"bn": "কাহারবা", "translit": "kaharba"}, "matras": 8, "vibhags": [4, 4],
                "beats": ["sam", "khali"], "talamukta": False},
    "khemta":  {"name": {"bn": "খেমটা", "translit": "khemta"}, "matras": 6, "vibhags": [3, 3],
                "beats": ["sam", "khali"], "talamukta": False},
    "tintal":  {"name": {"bn": "তিনতাল", "translit": "tintal"}, "matras": 16, "vibhags": [4, 4, 4, 4],
                "beats": ["sam", "taali", "khali", "taali"], "talamukta": False},
    "talamukta": {"name": {"bn": "তালমুক্ত", "translit": "talamukta"}, "matras": None, "vibhags": None,
                  "beats": None, "talamukta": True},
}

NLTR_BASE = "https://rabindra-rachanabali.nltr.org"

SONGS = [
    {
        "file": "nltr-purano-0", "id": "purano-sei-diner-katha",
        "title": {"bn": "পুরানো সেই দিনের কথা", "translit": "Purano sei diner katha"},
        "parjaay": {"bn": "প্রেম ও প্রকৃতি", "en": "Love and Nature"},
        "raga_anga": "মিশ্র ভূপালী (Mishra Bhupali), as printed in Swarabitan vol. 32 — a bhanga gaan on the Scots air 'Auld Lang Syne'",
        "taal": "ektaal",
        "url": NLTR_BASE + "/node/16053?gaan=পুরানো সেই দিনের কথা ভুলবি কি রে হায়.xml",
        "secondary": [{"site": "geetabitan.com", "url": "https://www.geetabitan.com/lyrics/P/purano-sei-diner-kotha-lyric.html",
                       "agreement": "taal (ektaal), parjaay, Auld-Lang-Syne origin, written 1885"},
                      {"site": "notesandsargam.com", "url": "https://notesandsargam.com/purano-shei-diner-kotha/",
                       "agreement": "melodic contour matches throughout (independent romanized sargam)"}],
        "confidence": {"level": "high",
                       "notes": ["Lines 1-6 verified against the printed Swarabitan vol. 32 scan (exact match)",
                                 "Line 4, matra 5: udara mark on the second ধা is ambiguous in the scan; witness reading kept"]},
    },
    {
        "file": "nltr-phule-1", "id": "phule-phule-dhole-dhole",
        "title": {"bn": "ফুলে ফুলে ঢ'লে ঢ'লে", "translit": "Phule phule dhole dhole"},
        "parjaay": {"bn": "প্রকৃতি", "en": "Nature"},
        "raga_anga": "Bhanga gaan — melody adapted from the Scots air 'Ye Banks and Braes'; from the gitinatya Kalmrigaya",
        "taal": "khemta",
        "url": NLTR_BASE + "/node/16053?gaan=29_6.xml",
        "secondary": [],
        "confidence": {"level": "high",
                       "notes": ["parjaay attribution traditional, not stated in primary witness"]},
    },
    {
        "file": "nltr-anandaloke", "id": "anandaloke-mangalaloke",
        "title": {"bn": "আনন্দলোকে মঙ্গলালোকে", "translit": "Anandaloke mangalaloke"},
        "parjaay": {"bn": "পূজা", "en": "Worship (Brahmasangeet)"},
        "raga_anga": None,
        "taal": "ektaal",
        "url": NLTR_BASE + "/node/16053?gaan=আনন্দলোকে মঙ্গলালোকে.xml",
        "secondary": [],
        "confidence": {"level": "high",
                       "notes": ["parjaay attribution traditional, not stated in primary witness"]},
    },
    {
        "file": "nltr-ekla", "id": "ekla-chalo-re",
        "title": {"bn": "যদি তোর ডাক শুনে কেউ না আসে", "translit": "Jodi tor dak shune keu na ase (Ekla chalo re)"},
        "parjaay": {"bn": "স্বদেশ", "en": "Patriotic"},
        "raga_anga": "Baul sur",
        "taal": "dadra",
        "url": NLTR_BASE + "/node/16053?gaan=যদি তোর ডাক শুনে কেউ না আসে.xml",
        "secondary": [{"site": "geetabitan.com", "url": "https://www.geetabitan.com/lyrics/J/jodi-tor-daak-shune-lyric.html",
                       "agreement": "taal (dadra), parjaay (Swadesh), Baul anga"},
                      {"site": "notesandsargam.com", "url": "https://notesandsargam.com/jodi-tor-dak-shune-keu-na-ashe-rabindra-sangeet/",
                       "agreement": "melodic contour matches (independent romanized sargam)"}],
        "confidence": {"level": "high", "notes": []},
    },
    {
        "file": "aguner-nltr", "id": "aguner-poroshmoni",
        "title": {"bn": "আগুনের পরশমণি ছোঁয়াও প্রাণে", "translit": "Aguner poroshmoni chhoyao prane"},
        "parjaay": {"bn": "পূজা", "en": "Worship"},
        "raga_anga": None,
        "taal": "dadra",
        "url": NLTR_BASE + "/node/16053?gaan=আগুনের পরশমণি ছোঁয়াও প্রাণে.xml",
        "secondary": [],
        "confidence": {"level": "high",
                       "notes": ["parjaay attribution traditional, not stated in primary witness",
                                 "4 note-units use the rare i-vowel token form; pitch reading confident, vowel-form semantics flagged"]},
    },
    {
        "file": "nltr-tumirobe-0", "id": "tumi-robe-nirobe",
        "title": {"bn": "তুমি রবে নীরবে", "translit": "Tumi robe nirobe"},
        "parjaay": {"bn": "প্রেম", "en": "Love (Prem-Boichitra)"},
        "raga_anga": "Behag",
        "taal": "ektaal",
        "url": NLTR_BASE + "/node/16053?gaan=তুমি রবে নীরবে হৃদয়ে মম.xml",
        "secondary": [{"site": "geetabitan.com", "url": "https://www.geetabitan.com/lyrics/T/tumi-robe-nirobe-lyric.html",
                       "agreement": "taal (ektaal), parjaay (Prem), raag Behag, written 1895, notated by Indira Debi Chaudhurani"},
                      {"site": "notesandsargam.com", "url": "https://notesandsargam.com/tumi-robe-nirobe/",
                       "agreement": "melodic contour matches (independent romanized sargam)"}],
        "confidence": {"level": "high",
                       "notes": ["2 note-units use the rare i-vowel token form; pitch reading confident, vowel-form semantics flagged"]},
    },
    {
        "file": "nltr-majhe", "id": "majhe-majhe-tobo-dekha-pai",
        "title": {"bn": "মাঝে মাঝে তব দেখা পাই", "translit": "Majhe majhe tobo dekha pai"},
        "parjaay": {"bn": "পূজা", "en": "Worship"},
        "raga_anga": None,
        "taal": "ektaal",
        "url": NLTR_BASE + "/node/16053?gaan=মাঝে মাঝে তব দেখা পাই.xml",
        "secondary": [],
        "confidence": {"level": "high",
                       "notes": ["parjaay attribution traditional, not stated in primary witness"]},
    },
    {
        "file": "nltr-bhalobese-0", "id": "bhalobese-sokhi",
        "title": {"bn": "ভালোবেসে সখী, নিভৃত যতনে", "translit": "Bhalobese sokhi, nibhrite jotone"},
        "parjaay": {"bn": "প্রেম", "en": "Love"},
        "raga_anga": None,
        "taal": "talamukta",
        "url": NLTR_BASE + "/node/16053?gaan=ভালোবেসে, সখী, নিভৃত যতনে.xml",
        "secondary": [],
        "confidence": {"level": "high",
                       "notes": ["Sthayi verified against the printed Swarabitan vol. 56 scan (exact match)",
                                 "talamukta (free rhythm): confirmed by the printed page, which carries no taal line and no vibhag dandas — this overrides a secondary source that lists the song as Dadra",
                                 "parjaay attribution traditional, not stated in any witness"]},
    },
    {
        "file": "nltr-esho", "id": "esho-shyamalo-sundoro",
        "title": {"bn": "এসো শ্যামল সুন্দর", "translit": "Esho shyamalo sundoro"},
        "parjaay": {"bn": "প্রকৃতি (বর্ষা)", "en": "Nature (Monsoon)"},
        "raga_anga": None,
        "taal": "tintal",
        "url": NLTR_BASE + "/node/16053?gaan=এসো শ্যামল সুন্দর.xml",
        "secondary": [],
        "confidence": {"level": "high",
                       "notes": ["parjaay attribution traditional, not stated in primary witness"]},
    },
    {
        "file": "nltr-gram-0", "id": "gram-chhara-oi-ranga-matir-path",
        "title": {"bn": "গ্রামছাড়া ওই রাঙা মাটির পথ", "translit": "Gram chhara oi ranga matir path"},
        "parjaay": {"bn": "প্রকৃতি", "en": "Nature"},
        "raga_anga": "বাংলা (Bangla), as printed in Swarabitan vol. 9",
        "taal": "kaharba",
        "url": NLTR_BASE + "/node/16053?gaan=গ্রামছাড়া ওই রাঙা মাটির পথ.xml",
        "secondary": [{"site": "notesandsargam.com", "url": "https://notesandsargam.com/gram-chhara-oyi-ranga-matir-poth/",
                       "agreement": "melodic contour matches (independent romanized sargam)"}],
        "confidence": {"level": "high",
                       "notes": ["Sthayi verified line-by-line against the printed Swarabitan vol. 9 scan (exact match); raga/taal now taken from the printed header rather than tradition",
                                 "12 note-units use the rare i-vowel token form; pitch reading confident, vowel-form semantics still flagged",
                                 "Verification covered line 1; lines 2-21 remain archive-derived"]},
    },
]

def guess_sections(lines, n):
    """Label lines by section using section_bar marks as boundaries (best-effort)."""
    sections = []
    current = 0
    names = ["sthayi", "antara", "sanchari", "abhog", "body5", "body6", "body7", "body8"]
    for ln in lines:
        sections.append(names[min(current, len(names) - 1)])
        if any(m["type"] == "section_bar" and m["cell"] >= len(ln["cells"]) - 1 for m in ln["marks"]):
            current += 1
    return sections

def build():
    outdir = ROOT / "data" / "songs"
    outdir.mkdir(parents=True, exist_ok=True)
    for cfg in SONGS:
        parsed = parse_song(ROOT / "sources" / "raw" / f"{cfg['file']}.html")
        lines = []
        secs = guess_sections(parsed["lines"], len(parsed["lines"]))
        taal = TAALS[cfg["taal"]]
        for i, (ln, sec) in enumerate(zip(parsed["lines"], secs), start=1):
            for c in ln["cells"]:
                for u in c["units"]:
                    u.pop("_raw", None)
            entry = {"line_no": i, "section": sec, "cells": ln["cells"], "marks": ln["marks"]}
            if taal["matras"] and len(ln["cells"]) < taal["matras"]:
                entry["anacrusis"] = True
            lines.append(entry)
        doc = {
            "schema_version": "0.1",
            "id": cfg["id"],
            "title": cfg["title"],
            "composer": "Rabindranath Tagore",
            "parjaay": cfg["parjaay"],
            "raga_anga": cfg["raga_anga"],
            "taal": taal,
            "sections": sorted(set(secs), key=secs.index),
            "lines": lines,
            "provenance": {
                "primary_witness": {
                    "archive": "SNLTR Rabindra Rachanabali digital edition (digitization of Swarabitan, Visva-Bharati)",
                    "url": cfg["url"],
                    "retrieved": RETRIEVED,
                    "taal_as_stated": parsed["meta"]["taal"] or "",
                },
                "scan_verification": SCAN_VERIFIED.get(cfg["id"]),
                "secondary_witnesses": cfg["secondary"],
                "encoding_method": "automated parse of the witness's notation grid (tools/parse_nltr.py) + manual review of every line",
                "known_deviations": [],
            },
            "confidence": cfg["confidence"],
        }
        out = outdir / f"{cfg['id']}.json"
        out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"wrote {out.name}: {len(lines)} lines, "
              f"{sum(len(l['cells']) for l in lines)} cells")

if __name__ == "__main__":
    build()
