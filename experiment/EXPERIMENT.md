# Claude continues Tagore: a blind composition experiment

**Question.** If a frontier language model absorbs the symbolic grammar of nine Rabindrasangeet — their taal cycles, note-sets, cadence idioms, lyric-melisma habits — can it continue a tenth song *in-grammar*? And where it fails, what does the failure teach us about what makes Tagore Tagore?

## Method

- **Model**: Claude Fable 5 (Anthropic), one shot, no retries, no cherry-picking.
- **Given**: the full sargam-text of the other nine songs in this corpus; the sthayi (first 4 lines) of পুরানো সেই দিনের কথা *only*; the Bengali lyrics of the antara it had to set (আয় আর একটিবার আয় রে সখা…); the notation format spec; the constraint set (ektaal 12-matra lines, the song's melodic world, taal-aware stress, a cadence that re-enters the sthayi).
- **Withheld**: everything of the song beyond line 4 — the model never saw Tagore's antara.
- **Blindness protocol**: the generation ran in an isolated agent context whose only permitted action was reading the prompt packet; the packet contains no ground truth. (Limitation, stated plainly: the model may know this famous song from pretraining. But the melody's swaralipi has never been machine-readable, the task demands cell-exact notation in a bespoke format defined only in this repo, and the output diverges from the real antara in its central gesture — which is evidence against recall and, as it happens, the most interesting result.)
- **Evaluation**: mechanical checks (`tools/`): line/matra arithmetic, note-set membership, format parse; then musicological comparison against Tagore's actual antara.
- **Artifacts**: `blind_prompt.txt` (the exact prompt), `claude_antara_raw.txt` (the exact output), `claude_antara.json` (parsed), audio A/B.

## Result: the grammar test — passed clean

| Check | Result |
|---|---|
| 4 lines × 12 matras, vibhags [3,3,3,3] | ✅ exact |
| Note-set within the song's idiom (S R G P D + octaves; N, as ornament) | ✅ zero violations — stayed inside the song's pentatonic frame, komal/kori-free |
| Lyric setting: syllable-per-matra with melismas at line-ends | ✅ parses cell-for-cell |
| Cadence prepares return to sthayi | ✅ settles G–R → S with an (N,) grace — the sthayi's own lower-neighbour figure, mirrored |

The continuation is not word-salad with notes. It is a syntactically flawless antara.

## Result: the style test — a revealing divergence

Where the machine and the poet part ways is the *register strategy*:

- **Claude's antara** does what a thousand Hindustani antaras do: it **leaps up**. "আয়" lands on tara Sa (S'), the section lives in the upper register, peaks at R' on "সুখের", then descends to cadence. This is the pan-Indian convention — sthayi low, antara high — and the model, having absorbed idiom from nine songs (several of which do exactly this), applied it with confidence.
- **Tagore's antara** refuses the convention. "আয় আর একটিবার" re-enters on **P–G**, in the same middle register as the sthayi, staying close to the Scots source-tune's compass; the one climb to S' is saved for "প্রাণের মাঝে আয়" — the emotional center of the couplet, *come into my heart* — and it is approached stepwise, not by leap.

So the model composed a *correct* antara; Tagore composed a *particular* one. The machine learned the grammar; the poem's own logic — where in the words the music should rise — is exactly the residue the grammar doesn't capture. Ten songs of signal were enough for syntax. Style, in the sense that matters, lives somewhere deeper in the data — or beyond it.

That, in one experiment, is both the promise and the honest limit of computing over this tradition — and the best argument for building the larger corpus: you cannot even *ask* this question without the symbolic data.

## Listen

- `purano_real_sthayi_antara.mp3` — sthayi + Tagore's antara (synthesized from notation)
- `purano_claude_continuation.mp3` — same sthayi + Claude's antara
- `claude_antara_only.mp3` — the AI section isolated

Both renditions use the identical synthesizer, tonic (Sa = C♯4) and laya, so the only difference you hear is the composition.

## Reproduce

```bash
# the prompt packet is deterministic from the corpus:
python3 - <<'PY'
# see repo history: experiment packet = 9 full songs + sthayi-only + task spec
PY
# validation of any candidate continuation:
python3 -c "import sys; sys.path.insert(0,'tools'); from parse_text import parse_lines; \
  print(parse_lines(open('experiment/claude_antara_raw.txt').read()))"
```
