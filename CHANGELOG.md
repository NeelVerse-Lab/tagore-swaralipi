# Changelog

All notable changes to this corpus are recorded here. The dataset follows semantic-ish versioning:
the **major.minor** version describes the corpus state, and any change to the *schema* bumps the
schema version independently (see `schema/SCHEMA.md`).

## [0.1.0] — 2026-08-11

First public release.

### Added
- 10 Rabindrasangeet encoded in **Swaralipi-JSON v0.1** — akarmatrik-faithful symbolic notation
  with swara/saptak/matra-fraction timing, taal cycles, komal & kori swaras as first-class notes,
  kan (grace) notes, and syllable-aligned Bengali lyrics.
- Coverage: ektaal, dadra, kaharba, tintal, khemta and one **talamukta** (free-rhythm) song;
  three raga-angas; two bhanga gaan built on Scottish airs.
- `schema/` — JSON Schema validator and the design rationale behind the format.
- `tools/` — full reproducible pipeline: source parser, dataset builder, validator, text renderer
  and re-parser, MIDI and MusicXML converters, and a dependency-free additive synthesizer.
- `derived/` — MIDI and MusicXML for every song.
- `audio/` — reference audio synthesized purely from the notation, no recordings involved.
- `docs/DECODING.md` — how the source archive's font-encoded notation was decoded, with the
  three-way triangulation evidence.
- `docs/DATASET_CARD.md` — coverage, intended uses, limitations, rights, prior art.
- `experiment/` — blind AI-continuation experiment with A/B audio and writeup.
- `tests/` — 116 integrity checks (schema, taal arithmetic, musical sanity, provenance, lossless
  round-trip) run in CI on every push and pull request.

### Notes on determinism
- `tools/to_musicxml.py` normalises music21's encoding date, version stamp and randomly
  generated part ids, so every derived file is byte-reproducible from the canonical JSON on any
  machine. CI asserts this on every push — a diff in `derived/` therefore always means a real
  change to the data, never a rerun artefact.

### Notes on sources
- Witness pages are **not redistributed**; `tools/fetch_sources.py` retrieves them from the cited
  URLs on demand and `sources/raw/` is git-ignored. Rationale in `sources/README.md`.
- Witness URLs use the archive's precomposed Bengali nukta characters (য় ড় ঢ়). Unicode NFC does
  not produce these — they are composition exclusions — so four of the ten URLs would otherwise
  return an empty viewer page that *looks* like a successful fetch. An opt-in network test
  (`RUN_NETWORK_TESTS=1`) checks every citation against the live archive.

### Known limitations
- Archive-derived, not verified against printed Swarabitan pages — this is the v0.2 milestone.
- 22 note-units across 3 songs use an undecoded source-notation variant; pitch confident, vowel
  semantics flagged `uncertain`.
- Section labels (sthayi/antara/…) are inferred from double-bar structure, not stated by the source.
- Meend spans are preserved positionally but not semantically.

[0.1.0]: https://github.com/NeelVerse-Lab/tagore-swaralipi/releases/tag/v0.1.0
