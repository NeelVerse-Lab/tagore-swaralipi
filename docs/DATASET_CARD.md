# Dataset Card — Ten Songs of Tagore, In Data (Swaralipi Corpus v0.1)

## Summary

Ten Rabindrasangeet encoded from akarmatrik swaralipi into **Swaralipi-JSON**, a symbolic format
built for Bengali notation rather than adapted from Western ones: swara degree with komal/kori
forms as first-class notes, three saptaks, matra-fraction timing, taal cycles with sam/taali/khali
structure, and Bengali lyrics aligned syllable-to-matra. Ships with derived MIDI and MusicXML,
notation-synthesized reference audio, the full digitization pipeline, and a blind AI-continuation
experiment.

| | |
|---|---|
| **Version** | 0.1 (archive-derived) |
| **Released** | 11 August 2026 |
| **Size** | 10 songs · 214 notated lines · 2,543 matra-cells · 3,195 units (2,183 pitched) |
| **Languages** | Bengali (lyrics, titles, taal names); English (documentation) |
| **Licence** | Data CC BY 4.0 · Code MIT |
| **Curator** | Indranil (Neel) Banerjee |

## What's in it

| Field | Description |
|---|---|
| `title`, `parjaay`, `raga_anga` | Bengali title + transliteration; thematic category; raga/anga association where tradition assigns one |
| `taal` | Name, matra count, vibhag structure, sam/taali/khali labels — or `talamukta: true` for free-rhythm songs |
| `lines[].cells[]` | One cell = one matra. Cells hold 1..n units that divide the matra evenly |
| `units[]` | `swara` (degree, komal/kori, saptak, optional kan grace notes), `sustain` (the akarmatrik dash), or `rest` |
| `cells[].lyric` | The Bengali syllable under that matra; `melisma: true` where the previous syllable continues |
| `lines[].marks` | Bar lines, vibhag separators, repeat and alternate spans preserved from the page |
| `provenance` | Witness archive, URL, retrieval date, taal as stated by the source, secondary witnesses and their agreement, encoding method |
| `confidence` | `high`/`medium`/`low` with written notes on what is unresolved |

### Coverage

Four taal families (ektaal 12 · dadra 6 · kaharba 8 · tintal 16 · khemta 6), one talamukta
(free-rhythm) song, three raga-angas, two bhanga gaan built on Scottish airs, and songs from the
Puja, Prem, Prakriti and Swadesh parjaays. The sample was chosen for **structural diversity**, so
that the schema is exercised across the tradition's range rather than tuned to one song type.

## How it was made

1. **Source.** The [SNLTR Rabindra Rachanabali digital edition](https://rabindra-rachanabali.nltr.org/)
   of Swarabitan serves akarmatrik notation as HTML grids in a custom font encoding — Latin token
   codes, one table cell per matra column.
2. **Decoding.** That token language was decoded and cross-checked three independent ways:
   against a second, unrelated archive of romanized sargam for the same songs; against music
   theory (the decoded note-sets reproduce each song's traditional raga signature — Behag's kori
   Ma in *Tumi robe nirobe*, Desh's both-Ni in *Esho shyamalo sundoro*, the pentatonic frame of
   the *Auld Lang Syne* bhanga gaan); and by ear, since audio synthesized purely from the decoded
   data is recognizably the songs. Full evidence chain: [`docs/DECODING.md`](DECODING.md).
3. **Encoding.** `tools/parse_nltr.py` parses the grid; `tools/build_dataset.py` assembles
   canonical JSON with curated metadata and provenance. Every line was reviewed by hand.
4. **Verification.** JSON Schema validation, taal arithmetic, note-set sanity, and a lossless
   round-trip (JSON → human-readable sargam-text → JSON) — all in `tests/`, all run in CI.

Everything in `data/`, `derived/` and `audio/` is reproducible with the commands in the README.
The witness pages themselves are **not redistributed** — `tools/fetch_sources.py` retrieves them
from the cited URLs on demand (see [`sources/README.md`](../sources/README.md)).

## Intended uses

Music information retrieval on a tradition with almost no symbolic data; computational musicology
(phrase grammar, taal-cadence idiom, how Tagore reworked borrowed melodies); pedagogy and notation
rendering; symbolic-music modelling; and cultural-heritage preservation. It is deliberately small:
a proof of schema and pipeline, and an invitation to scale.

## Limitations — read before relying on this

- **Partially scan-verified.** 3 of 10 songs have been checked matra-by-matra against scans of the
  printed Swarabitan (all three: exact match; see [VERIFICATION.md](VERIFICATION.md)). The other
  seven are archive-derived and say so in their `confidence` block. Completing the remaining seven
  is the v0.2 milestone; their volume numbers are already identified.
- **Ten songs is 0.5% of the songbook.** Any statistical claim drawn from this corpus is a claim
  about ten songs.
- **Performance is not notation.** Swaralipi records the composition. Rabindrasangeet in
  performance carries ornamentation, rhythmic elasticity and expressive choices that no page holds.
  Do not mistake this data for how the music sounds.
- **Not encoded:** absolute pitch (the tonic is the singer's choice), tempo (the page doesn't
  specify it), harmony (the tradition is melodic), and meend spans (marked positionally, not
  semantically).
- **22 note-units across 3 songs** use a source-notation variant we could not fully decode. Pitch
  is confident; the vowel/duration semantics are flagged `uncertain` in the data.
- **Section labels** (sthayi/antara/…) are inferred from double-bar structure, not stated by the
  witness.
- **Derived formats are lossy by design.** MIDI and MusicXML cannot hold taal cycle structure or
  the komal/kori letter distinction. The JSON is canonical; treat the rest as views.

## Provenance and rights

- **Compositions**: Rabindranath Tagore (1861–1941). His works entered the Indian public domain on
  1 January 2002, after the government declined Visva-Bharati's request to extend its term.
- **Notation source**: the SNLTR digital edition, itself a digitization of Swarabitan
  (Visva-Bharati, ~64 volumes, first published 1936–1955; notated by Dinendranath Tagore and
  later transcribers).
- **What this dataset contains**: an original re-encoding of musical facts — pitches, durations,
  taal structure, lyrics — of public-domain songs, into a schema authored for this project. It
  redistributes no page images, fonts, HTML, or typographical arrangement from any archive. Every
  song records its witness, the exact URL, and the retrieval date.
- **Attribution requested**: cite this dataset (see `CITATION.cff`) and, where relevant, the SNLTR
  edition and Swarabitan as the notation's lineage.

## Prior and adjacent work

To our knowledge this is the first openly licensed *symbolic* Rabindrasangeet dataset (checked
across Hugging Face, GitHub, Zenodo and the MIR literature, August 2026). Adjacent efforts, none
of which occupy this niche:

- **SANGEET** ([arXiv:2306.04148](https://arxiv.org/abs/2306.04148)) — XML dataset of Hindustani
  compositions from Bhatkhande's *Kramik Pustak Malika*; different repertoire, no stated licence.
- **SwaralipiXML** ([spec](https://indic-music.github.io/swaralipixml.html)) — an XML interchange
  format for Indic notation including akarmatrik; a format with an example, not a corpus.
- **Saraga / CompMusic** ([datasets](https://compmusic.upf.edu/datasets)) — open Indian art music
  corpora; audio with annotations, not symbolic scores.
- **`Pradipta/tagore_songs`** (Hugging Face) — Rabindrasangeet lyrics and metadata; no melody.

## Citation

```bibtex
@dataset{banerjee2026swaralipi,
  author  = {Banerjee, Indranil},
  title   = {Ten Songs of Tagore, In Data: A Symbolic Corpus of Rabindrasangeet Swaralipi},
  year    = {2026},
  version = {0.1.0},
  license = {CC-BY-4.0},
  url     = {https://github.com/NeelVerse-Lab/tagore-swaralipi}
}
```

## Maintenance

Corrections are the point, not an interruption — see [CONTRIBUTING.md](../CONTRIBUTING.md).
Contributors whose corrections change the data are credited in that song's provenance block.
Roadmap: v0.2 scan verification and three reserve songs · v0.5 fifty songs across all parjaays ·
v1.0 as far as the community wants to carry it.
