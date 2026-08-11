<!-- Thank you for contributing. Delete any section that doesn't apply. -->

## What does this change?

<!-- One or two sentences. -->

## Type

- [ ] Notation correction (data changes)
- [ ] New song
- [ ] Tooling / code
- [ ] Schema change (needs a version bump — see CONTRIBUTING.md §4)
- [ ] Documentation

## If this touches `data/`

**Source for the change** (required — Swarabitan volume/page, or the archive and retrieval date):

<!-- e.g. Swarabitan vol. 32 p.14, Visva-Bharati 1963 ed. -->

- [ ] I updated the song's `provenance` block (and `confidence`, if the certainty changed)
- [ ] `python -m pytest tests/ -v` passes
- [ ] `python tools/validate.py` reports no PROBLEMs
- [ ] If the melody changed, I regenerated `data/text/`, `derived/`, and `audio/`
      (`python tools/render_text.py && python tools/to_midi.py && python tools/to_musicxml.py && python tools/synth.py`)

## Credit

- [ ] Credit me by name in the provenance block (uncheck to stay anonymous)

Name to use, if different from your GitHub handle: <!-- optional -->
