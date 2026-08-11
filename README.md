# দশটি গান, ডেটায় — Ten Songs of Tagore, In Data

[![Validate corpus](https://github.com/NeelVerse-Lab/tagore-swaralipi/actions/workflows/validate.yml/badge.svg)](https://github.com/NeelVerse-Lab/tagore-swaralipi/actions/workflows/validate.yml)
[![Data: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-blue.svg)](LICENSE)
[![Code: MIT](https://img.shields.io/badge/code-MIT-green.svg)](LICENSE)
[![Songs: 10](https://img.shields.io/badge/songs-10-orange.svg)](data/songs)
[![Schema: v0.1](https://img.shields.io/badge/schema-v0.1-lightgrey.svg)](schema/SCHEMA.md)

**A micro-dataset of Rabindrasangeet swaralipi in machine-readable symbolic notation — to our knowledge, the first openly licensed one — plus one experiment: a frontier AI model composing a continuation of a Tagore song, in-grammar, with audio.**

> **Can you read swaralipi?** You are who this project needs most, and you don't need to write a
> line of code. See [how to verify a song](CONTRIBUTING.md#1-verify-a-song-against-the-printed-swarabitan) —
> it takes ten minutes, and you'll be credited in the data itself.

Rabindranath Tagore left behind roughly 2,200 songs, and — almost uniquely among song traditions of that scale — nearly all of them were *notated*, in the akarmatrik swaralipi system, across the ~64 volumes of **Swarabitan**. That notation has been in the public domain in India since 1 January 2002. Yet in 2026, if you want to compute over Rabindrasangeet — study its melodic grammar, train a model on it, analyse how Tagore bent a Scots air into a khemta — there is no open symbolic dataset. The notation exists as page scans and font-locked websites. This repository is a small, careful first move against that gap.

## What's here

| Path | Contents |
|---|---|
| `data/songs/` | 10 songs in **Swaralipi-JSON** — the canonical, akarmatrik-faithful encoding (swara + saptak + matra-fraction + taal cycle + Bengali lyric alignment + provenance) |
| `data/text/` | The same 10 songs as human-readable **sargam-text** (round-trip verified) |
| `derived/midi/`, `derived/musicxml/` | Auto-derived MIDI and MusicXML views (lossy by design; the JSON is canonical) |
| `audio/` | Reference audio synthesized *purely from the notation* — no recordings involved |
| `schema/` | `SCHEMA.md` (design rationale) and a JSON Schema validator |
| `tools/` | The full pipeline: witness fetcher, parser, validators, converters, synthesizer — every file in `data/` is reproducible from the cited sources |
| `docs/DECODING.md` | How the source archive's font-encoded notation was decoded, with the cross-source triangulation evidence |
| `docs/DATASET_CARD.md` | Formal dataset card — coverage, intended uses, limitations, rights, prior art |
| `docs/VERIFICATION.md` | What was checked against the printed Swarabitan, what matched, and what it corrected |
| `experiment/` | **"Claude continues Tagore"** — a blind composition experiment with A/B audio ([writeup](experiment/EXPERIMENT.md)) |
| `index.html` | The [listening page](https://neelverse-lab.github.io/tagore-swaralipi/) — notation beside audio, built by `tools/build_site.py` |
| `tests/` | 126 integrity checks — schema, taal arithmetic, provenance, lossless round-trip. Run in CI on every PR |

## The ten songs

| Song | Taal | Notes |
|---|---|---|
| পুরানো সেই দিনের কথা | Ektaal (12) | Mishra Bhupali; bhanga gaan on "Auld Lang Syne" — **scan-verified** |
| ফুলে ফুলে ঢ'লে ঢ'লে | Khemta (6) | Bhanga gaan on "Ye Banks and Braes" |
| আনন্দলোকে মঙ্গলালোকে | Ektaal (12) | Brahmasangeet; uses kori Ma |
| যদি তোর ডাক শুনে কেউ না আসে (একলা চলো রে) | Dadra (6) | Baul sur; komal Dha/Ni inflections |
| আগুনের পরশমণি | Dadra (6) | Both Ma forms |
| তুমি রবে নীরবে | Ektaal (12) | Behag; the M#-beside-P signature is visible in the data |
| মাঝে মাঝে তব দেখা পাই | Ektaal (12) | Mixed Ga and Ni forms (Jhinjhoti-anga) |
| ভালোবেসে সখী, নিভৃত যতনে | **Talamukta** (free) | Free rhythm, confirmed on the printed page — **scan-verified** |
| এসো শ্যামল সুন্দর | Tintal (16) | Textbook Desh note-set in the data |
| গ্রামছাড়া ওই রাঙা মাটির পথ | Kaharba (8) | বাংলা (Bangla) anga — **scan-verified** |

Four taal families, one free-rhythm song, three raga-angas, two Scottish borrowings: a deliberately diverse structural sample of the tradition.

## Why a *symbolic* dataset matters

Audio corpora of Rabindrasangeet exist. But audio entangles the composition with a performance. The swaralipi is the composition itself — what Tagore (via his notators: Jyotirindranath Tagore, Dinendranath Tagore, Indira Devi Chaudhurani and others) fixed on the page. Symbolic data is what lets you ask: *what are the grammar rules of this music?* Which taals carry which cadence idioms? How does a Behag song treat kori Ma? What did Tagore change when he took a pentatonic Scots tune into ektaal? Every one of those questions becomes a query over this JSON.

And for the machine-learning era there is a sharper reason: **models learn the grammar of what they can read.** Western music has centuries of digitized scores; Rabindrasangeet has essentially none. A tradition absent from the data is absent from the models. This micro-dataset is 10 songs — 0.5% of the songbook — released to prove the pipeline and the schema, and to invite the community to scale it.


## Listen — every note here is synthesized from the notation

**🎧 [Open the listening page](https://neelverse-lab.github.io/tagore-swaralipi/)** — all ten songs with players, each next to the swaralipi
the audio is made from, plus the AI experiment side by side.

Nothing in `audio/` is a recording. Each file was generated from the JSON in `data/songs/`, so it
is a direct audible test of the digitization: if a song sounds right, the data is right, and if a
phrase sounds wrong, you have found a bug worth [reporting](../../issues/new?template=notation-correction.yml).

| | Listen | Read the notation |
|---|---|---|
| পুরানো সেই দিনের কথা — *ektaal, Mishra Bhupali* | [▶ play](https://raw.githubusercontent.com/NeelVerse-Lab/tagore-swaralipi/main/audio/purano-sei-diner-katha.mp3) | [sargam-text](data/text/purano-sei-diner-katha.txt) |
| যদি তোর ডাক শুনে (একলা চলো রে) — *dadra, Baul sur* | [▶ play](https://raw.githubusercontent.com/NeelVerse-Lab/tagore-swaralipi/main/audio/ekla-chalo-re.mp3) | [sargam-text](data/text/ekla-chalo-re.txt) |
| তুমি রবে নীরবে — *ektaal, Behag* | [▶ play](https://raw.githubusercontent.com/NeelVerse-Lab/tagore-swaralipi/main/audio/tumi-robe-nirobe.mp3) | [sargam-text](data/text/tumi-robe-nirobe.txt) |
| ভালোবেসে সখী — *talamukta (free rhythm)* | [▶ play](https://raw.githubusercontent.com/NeelVerse-Lab/tagore-swaralipi/main/audio/bhalobese-sokhi.mp3) | [sargam-text](data/text/bhalobese-sokhi.txt) |
| এসো শ্যামল সুন্দর — *tintal, Desh* | [▶ play](https://raw.githubusercontent.com/NeelVerse-Lab/tagore-swaralipi/main/audio/esho-shyamalo-sundoro.mp3) | [sargam-text](data/text/esho-shyamalo-sundoro.txt) |

*(all ten are in [`audio/`](audio) — the five above are a spread across the taal families)*

### The experiment, A/B

Same sthayi, same synthesizer, same tonic. The only difference is who wrote the second half.

| | |
|---|---|
| **Tagore's antara** | [▶ play](https://raw.githubusercontent.com/NeelVerse-Lab/tagore-swaralipi/main/experiment/purano_real_sthayi_antara.mp3) |
| **Claude's antara**, composed blind | [▶ play](https://raw.githubusercontent.com/NeelVerse-Lab/tagore-swaralipi/main/experiment/purano_claude_continuation.mp3) |

Could you pick which is his? The [writeup](experiment/EXPERIMENT.md) explains what the model got
right — and the one thing it got conventionally, where Tagore did not.

## Provenance and licensing — read this before reusing

- **Compositions**: Rabindranath Tagore (d. 1941). His works entered the Indian public domain on 1 January 2002; the government explicitly declined to extend Visva-Bharati's term in 2001.
- **Primary witness**: the [SNLTR Rabindra Rachanabali digital edition](https://rabindra-rachanabali.nltr.org/) (Govt. of West Bengal), itself a digitization of Swarabitan. This dataset **re-encodes the musical facts** — pitches, durations, taal structure, lyrics of public-domain songs — into an original schema; it redistributes nothing from any witness — no page images, no fonts, no HTML, no typographical arrangement. The witness pages are fetched on demand by `tools/fetch_sources.py` and are git-ignored (see [`sources/README.md`](sources/README.md)). Per-song witness URLs, retrieval dates and cross-witness agreement are recorded in each file's `provenance` block. Where an independent second witness existed (geetabitan.com metadata, romanized sargam archives), agreement is noted.
- **This is v0.1, archive-derived.** The v0.2 milestone is verification of every song against first-edition Swarabitan page scans (Internet Archive holds several volumes). Each file carries an honest `confidence` block; corrections are welcome and wanted — that is what the issue tracker is for.
- **License**: data (`data/`, `derived/`, `audio/`) **CC BY 4.0**; code (`tools/`, `schema/`) **MIT**. Cite as in `CITATION.cff`.

## Reproduce everything

```bash
pip install -r requirements.txt
python tools/fetch_sources.py    # download the cited witness pages (git-ignored)
python tools/build_dataset.py    # sources/raw HTML -> data/songs/*.json
python tools/validate.py         # JSON Schema + taal arithmetic + note-set report
python tools/render_text.py      # -> data/text (round-trip verified vs parse_text.py)
python tools/to_midi.py          # -> derived/midi
python tools/to_musicxml.py      # -> derived/musicxml
python tools/synth.py            # -> audio (needs ffmpeg)
python tools/build_site.py       # -> index.html (listening page)
python -m pytest tests/ -v       # 126 integrity checks
```


## How much of this is verified

Three of the ten songs have been checked **matra by matra against scans of the printed
Swarabitan**, not just against the online archive they were encoded from. That check is written up
in [`docs/VERIFICATION.md`](docs/VERIFICATION.md) with the volume, page and scan URL for each, so
you can repeat it rather than trust it. What it produced:

- **পুরানো সেই দিনের কথা** (vol. 32) — exact match over six lines, *and* the printed header gave us
  a raga the online witness omits: **Mishra Bhupali**, a pentatonic raga. That independently
  corroborates both the song's *Auld Lang Syne* origin and our decoding, since the note-set in our
  data came out pentatonic without us ever assuming it.
- **ভালোবেসে সখী** (vol. 56) — exact match, and it **settled a conflict between sources**. A
  secondary source lists this song as dadra; the printed page has no taal header and no vibhag
  bars anywhere, which is how Swarabitan sets a *talamukta* song. Our talamukta reading stands,
  and now says why.
- **গ্রামছাড়া ওই রাঙা মাটির পথ** (vol. 9) — exact match, **one metadata correction** (the anga is
  বাংলা as printed, not the "Baul" we had from tradition), and it validated the corpus's *kan*
  (grace-note) encoding: where we mark a kan, the print sets that swara as a smaller raised
  glyph — the akarmatrik convention. A guess became evidence.

The other seven songs remain archive-derived and their `confidence` blocks say so. Their volume
numbers are listed in the verification doc, so the remaining work is well-defined and anyone who
reads swaralipi can take a row.

## Contributing

**The single most valuable thing anyone can do here is read a Swarabitan page and tell us what we
got wrong.** That needs no programming — see
[CONTRIBUTING.md](CONTRIBUTING.md#1-verify-a-song-against-the-printed-swarabitan). Corrections are
credited by name in the data.

Also wanted: [new songs](CONTRIBUTING.md#2-add-a-song) (especially unusual taals and un-represented
parjaays), [better tooling](CONTRIBUTING.md#3-improve-the-tooling) (akarmatrik rendering, meend-aware
synthesis, format bridges), and [schema work](CONTRIBUTING.md#4-extend-the-schema). Bengali, Hindi
and English are all welcome in issues and discussions.

## The experiment

We gave a frontier LLM (Claude Fable 5) the nine other songs plus only the sthayi of *Purano sei diner katha*, and asked it to compose the antara — melody for Tagore's actual lyrics, in ektaal, in the song's idiom. It returned a continuation with **zero grammar violations** (12-matra cycles exact, strictly pentatonic note-set, a properly prepared cadence back to the sthayi) — and one deeply revealing *stylistic* divergence from what Tagore actually wrote. The full method, the A/B audio, and what it says about convention versus genius: [`experiment/EXPERIMENT.md`](experiment/EXPERIMENT.md).

## Roadmap

- **v0.2** — Swarabitan scan verification; the three reserve songs (আলো আমার আলো, ক্লান্তি আমার, আমার পরান যাহা চায়); meend arcs as first-class spans
- **v0.5** — 50 songs across all six parjaays; contributor guide for notation-literate volunteers
- **v1.0** — the full Swarabitan, if the community wants it as much as we do

---

*Built in Bengal's own notation system, for Bengal's own songs, in the open.*
