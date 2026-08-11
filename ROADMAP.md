# Roadmap

Where this goes next, what each step needs, and which parts are claimable by someone other than
the maintainer. Items marked **help wanted** are ones a contributor can pick up without
coordinating first — say so in an issue and it's yours.

The guiding rule: **the corpus grows only as fast as it can be verified.** A hundred unverified
songs would be worth less than the ten we have, because the value of this data is that you can
check it.

---

## v0.2 — Verify what exists (next)

The single most important release. No new songs are strictly required; the goal is that every
existing song has been read against the printed Swarabitan rather than an online copy of it.

| Task | Notes | Status |
|---|---|---|
| **Verify the remaining seven songs against Swarabitan scans** | Volumes and archive IDs already identified in [`docs/VERIFICATION.md`](docs/VERIFICATION.md). One song ≈ one evening. **help wanted** | 3/10 done |
| **Add the second setting of মাঝে মাঝে তব দেখা পাই** | Swarabitan vol. 23 carries two distinct settings; we hold only the ektaal one. Needs a schema decision: sibling songs, or variants inside one file? | open |
| **Decode the 22 `i`-form tokens** | A source-notation variant we could not resolve. Pitch is confident, vowel/duration semantics are not. Needs someone who knows akarmatrik deeply. **help wanted** | open |
| **Resolve the ambiguous udara mark** | পুরানো, line 4 matra 5 — needs a cleaner scan or a print copy | open |
| **Three reserve songs** | আলো আমার আলো ওগো · ক্লান্তি আমার ক্ষমা করো · আমার পরান যাহা চায় — already researched, not yet encoded | open |
| **Mint a DOI** | Connect the repo to Zenodo so each release gets a citable DOI. Without one, academics can cite the dataset but not durably. Maintainer task, ~15 minutes | open |

**Definition of done:** every song's `provenance.scan_verification` is populated, and
`docs/VERIFICATION.md` reports 10/10 with every discrepancy written down.

---

## v0.3 — Make the notation legible again

Right now the data round-trips to plain sargam text. It should round-trip to something a Bengali
musician recognises on sight.

- **Akarmatrik renderer** — Bengali script, taal grids, vibhag bars, lyrics aligned under notes,
  kan set as raised glyphs, meend as arcs. Output SVG/PDF from the JSON. **help wanted** — this is
  the highest-visibility piece of tooling in the project, and it makes every correction visible as
  a corrected *page*.
- **Meend as first-class spans** — currently preserved positionally, not semantically. Needs a
  schema change (`schema_version` bump) and a migration note.
- **Better synthesis** — meend glides and gamaka. The present synth is deliberately plain; plain is
  honest but it undersells the music.
- **Bengali-language documentation** — README and CONTRIBUTING in Bengali. The people best placed
  to verify this data should not have to read English to help. **help wanted**

---

## v0.5 — Fifty songs, all parjaays

Scale, but only behind verification.

- 50 songs spanning all six parjaays, with deliberate coverage of rare taals (nabataal, ekadashi,
  rupakda, jhampak) and Tagore's own rhythmic inventions.
- More bhanga gaan, with their source tunes identified — this is what makes the comparative
  analysis in [`docs/USE_CASES.md`](docs/USE_CASES.md) possible.
- **A contributor verification workflow**: a script that takes a song ID, pulls the right scan page,
  shows it beside the corpus text, and writes the verification block for you. Removes most of the
  friction from the task that matters most.
- **Format bridges** — export to SwaralipiXML, ABC, LilyPond, Humdrum `**kern`, so the data reaches
  existing musicology toolchains rather than asking them to learn ours. **help wanted**
- **Mirror to Hugging Face** so ML researchers find it where they look.

---

## v1.0 — As far as the community carries it

Not a fixed number. v1.0 means the format is stable, the pipeline is boring, and enough people
have contributed that the project no longer depends on any one person. If that lands at 200 songs,
it lands at 200.

Ideas that belong here rather than earlier:

- **The continuation benchmark.** Formalise the AI experiment into a scored evaluation with a
  held-out set, published baselines, and a leaderboard. See the argument in
  [`docs/USE_CASES.md`](docs/USE_CASES.md#a-benchmark-not-just-a-dataset) — a benchmark that
  distinguishes *followed the rules* from *understood the idiom* is hard to build, and this
  repertoire supplies one.
- **Braille music and screen-reader output.** Symbolic notation can be made accessible; page scans
  cannot.
- **Cross-tradition schema.** Nazrulgeeti, Atulprasadi, Dwijendrageeti and Rajanikanta's songs all
  use akarmatrik notation. The schema was built for Rabindrasangeet but nothing in it is specific
  to Tagore. A sibling corpus would cost far less than this one did.

---

## Explicitly not planned

Saying no is part of a roadmap.

- **Audio recordings.** This is a notation corpus. Performance corpora exist (Saraga, CompMusic)
  and do that job better. The synthesized audio here exists to make the *data* checkable by ear,
  not to be listened to for pleasure.
- **Automatic OCR of swaralipi at scale.** Tempting, and the wrong trade. The failure mode of OCR
  is confident wrongness at volume, which is exactly what this project is set up to avoid. Assisted
  transcription with a human deciding — yes. Unattended bulk OCR — no.
- **Performance-practice annotations.** How a song is *sung* — ornament choices, tempo elasticity,
  gharana differences — is real and valuable and belongs in a different dataset with different
  provenance rules. Mixing it into the notation would blur the one line this corpus is careful
  about: what the page says versus what a singer does.
- **A web app.** The listening page is deliberately one static HTML file. Anything more becomes
  software to maintain, and the data is the point.

---

## Known open questions

Things we don't know, recorded so they aren't quietly forgotten:

1. **The `i`-form tokens** (22 units, 3 songs) — an undecoded source-notation variant.
2. **Section labels** — sthayi/antara/sanchari/abhog are inferred from double-bar structure, not
   stated by any witness. Sometimes that inference will be wrong.
3. **Edition drift** — Swarabitan volumes went through multiple editions. Where they disagree, the
   schema currently has no way to hold two readings at once. It should.
4. **Anacrusis vs. printed line breaks** — some lines end with pickup cells for the next cycle.
   We record them as printed, but "as printed" and "as counted" are not always the same thing, and
   the taal-arithmetic test tolerates a small number of off-cycle lines because of it.
5. **Whether the corpus is representative.** Ten songs were chosen for structural diversity, which
   is the right call for testing a schema and the wrong one for statistics. Any inference drawn
   from this corpus is an inference about these ten songs.

---

## How to claim something

Open an issue saying which item you're taking, or comment on the existing one. For verification
tasks, [`docs/VERIFICATION.md`](docs/VERIFICATION.md) has the exact commands and the volume for
every remaining song — you can start without asking anyone.

If you want to do something that isn't on this list, that's usually a better idea than the list.
Open a [discussion](../../discussions).
