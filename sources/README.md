# sources/

**This directory is intentionally almost empty.**

Every song in this corpus was encoded from a witness page served by the
[SNLTR Rabindra Rachanabali digital edition](https://rabindra-rachanabali.nltr.org/) of
*Swarabitan*. Those pages are **not redistributed here**, for two reasons:

1. **Rights.** Tagore's compositions have been in the Indian public domain since 2002, and the
   musical facts we extracted — pitches, durations, taal structure, lyrics — are not anyone's
   property. But the archive asserts copyright over *its own digitization*, and re-hosting its
   HTML would be claiming something that isn't ours to give away.
2. **Consistency.** [CONTRIBUTING.md](../CONTRIBUTING.md) asks contributors not to paste scans,
   fonts, or large verbatim extracts of any archive into this repo. A rule the maintainers exempt
   themselves from is not a rule.

What is preserved instead is stronger than a copy: **every song records exactly where it came
from.** Each file in `data/songs/` carries a `provenance` block with the witness archive, the
precise URL, the retrieval date, the taal as that source stated it, any secondary witnesses and
whether they agreed, and the encoding method.

## Reproducing the dataset from scratch

```bash
python tools/fetch_sources.py     # downloads the witness pages into sources/raw/ (git-ignored)
python tools/build_dataset.py     # sources/raw/*.html -> data/songs/*.json
python -m pytest tests/ -v        # verify what you rebuilt
```

`sources/raw/` is listed in `.gitignore`, so fetched pages stay on your machine.

If a URL has moved — the archive encodes Bengali song titles in its query strings, which are
fragile — the canonical URL for each song is in its provenance block, and the archive's own index
is at `https://rabindra-rachanabali.nltr.org/`. Please open an issue if you find a dead witness so
we can record the change rather than quietly lose the trail.

## On the decoding

The witness serves notation in a custom font encoding, not readable text. How that token language
was decoded — and the three independent lines of evidence that confirm the decoding — is
documented in [`docs/DECODING.md`](../docs/DECODING.md). That document, not this directory, is
where the real audit trail lives.
