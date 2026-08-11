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
        "raga_anga": "Bhanga gaan — melody adapted from the Scots air 'Auld Lang Syne'",
        "taal": "ektaal",
        "url": NLTR_BASE + "/node/16053?gaan=পুরানো সেই দিনের কথা ভুলবি কি রে হায়.xml",
        "secondary": [{"site": "geetabitan.com", "url": "https://www.geetabitan.com/lyrics/P/purano-sei-diner-kotha-lyric.html",
                       "agreement": "taal (ektaal), parjaay, Auld-Lang-Syne origin, written 1885"},
                      {"site": "notesandsargam.com", "url": "https://notesandsargam.com/purano-shei-diner-kotha/",
                       "agreement": "melodic contour matches throughout (independent romanized sargam)"}],
        "confidence": {"level": "high", "notes": []},
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
                       "notes": ["talamukta (free rhythm): primary witness states তালমুক্ত; cell durations are relative, no cycle implied",
                                 "parjaay attribution traditional, not stated in primary witness"]},
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
        "raga_anga": "Baul-anga (traditional attribution)",
        "taal": "kaharba",
        "url": NLTR_BASE + "/node/16053?gaan=গ্রামছাড়া ওই রাঙা মাটির পথ.xml",
        "secondary": [{"site": "notesandsargam.com", "url": "https://notesandsargam.com/gram-chhara-oyi-ranga-matir-poth/",
                       "agreement": "melodic contour matches (independent romanized sargam)"}],
        "confidence": {"level": "medium",
                       "notes": ["12 note-units use the rare i-vowel token form; pitch reading confident, vowel-form semantics flagged",
                                 "parjaay/raga attribution traditional, not stated in primary witness"]},
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
