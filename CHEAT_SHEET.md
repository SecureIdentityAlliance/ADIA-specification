# ADIA Kit — Command Cheat-Sheet

Everything runs from the kit folder. If a command says "No rule to make target" or "No such file", you are in the wrong folder:

```bash
cd ~/Documents/adia-spec/local-kit
```

Commands are grouped by how often you use them. `make help` prints the list at any time.

---

## Every session

| Command | What it does | When |
|---|---|---|
| `make status` | Prints the headline: *N of M checks pass* | Start and end of a session, or after any edit, to see whether the count moved |
| `make save m="…"` | Validates the tracker, regenerates the Editor's Notes and the register, then records everything in local history with your message | **End of every session, and after every meaningful change.** Put the defect ID in the message: `make save m="Fix E-518: subject-verb agreement"` |

`make save` is the one that matters. It runs the safety net — a broken tracker file is caught and nothing is saved — and because it regenerates the Editor's Notes first, that clause can never be stale in a saved version.

---

## When something fails

| Command | What it does | When |
|---|---|---|
| `make explain ID=E-501` | Shows **why** a check fails, with line numbers and the offending text | The moment `make status` or `make ci` reports a failure you don't understand. Always try this before asking |
| `make check` | The full checker report, every check, pass or fail | When you want the whole picture rather than the headline |
| `make ci` | Reports only **regressions** — checks that passed before and now fail | Before a save, after a big edit, or when you suspect a fix broke something else. The first run records the baseline; later runs compare against it |
| `make validate` | Checks `defects.yaml` for typos: tabs, misspelled statuses, duplicate IDs | After hand-editing the tracker, before `make save`. `make save` runs it anyway, but running it alone gives a faster answer |

---

## After editing the spec

Run these in this order after a session of spec edits. Each is safe to run more than once.

| Command | What it does | When |
|---|---|---|
| `make anchors` | Adds a stable `<a id>` anchor above any heading that lacks one | After adding or renaming a heading. F-607 fails until you do |
| `make relocate` | Refreshes every line reference in the tracker from its anchor phrase | After edits that add or remove lines — the numbers drift otherwise. Reports anchors it can no longer find, which usually means you fixed that item |
| `make tidy` | Removes invisible characters (non-breaking spaces, zero-width characters) and trailing whitespace. Leaves curly quotes and dashes alone | After pasting anything from Word, Google Docs, Outlook or Slack. Those characters break search silently |
| `make notes` | Regenerates the Editor's Notes clause from the tracker | Whenever you want to see the current outstanding list in the document. `make save` does this automatically |
| `make register` | Rebuilds `defects/register.md`, the readable report | When you want to read progress rather than the raw tracker. `make save` does this automatically |

---

## One-time conversions

These implement a specific defect fix. Each is idempotent: run it twice and the second run reports "already applied". All the ones below have been run at least once; they're listed so you know what they were.

| Command | Closes | What it did |
|---|---|---|
| `make figures` | F-602 | Replaced `media/imageN.png` with named SVGs (Figures 1–10) and Mermaid (11–20) |
| `make assurance` | A-108, D-402 | Replaced `authorized_max_assurance_level` with `ial`/`aal`/`fal` fields in Appendix B |

---

## Scripts without a `make` target

Newer fixes arrived as scripts rather than make targets, to avoid a Makefile that needs re-downloading for every change. Run them directly. **Always `--dry-run` first** — it prints what would change and writes nothing.

```bash
python3 defects/<script>.py --dry-run
python3 defects/<script>.py
```

| Script | Closes | What it does |
|---|---|---|
| `apply_flow_fixes.py` | B-202, B-207 | Corrects the four defective message lines in the flow descriptions |
| `apply_hida.py` | D-405 (part) | HIDA becomes REQUIRED within an Interchange |
| `apply_da_uniqueness.py` | D-404 | Digital Address uniqueness model per RK; nine edits |
| `apply_acronyms.py` | D-414 | Adds the acronym table as clause 4.1 |
| `apply_b201.py` | B-201, B-212 | Replaces the incorrect signature-verification paragraph |
| `apply_vp.py` | A-127, A-123 | Adds the B.2.12 `vp` object; adds nonce/aud/state to `vc_request` |
| `apply_conformance.py` | C-303 | Adds clause 1.1 Conformance |
| `apply_security.py` | C-304 | Adds Security Considerations |
| `apply_privacy.py` | C-305 | Adds Privacy Considerations |

After any of these: `make anchors`, then `make save m="…"`.

---

## Setup and recovery

| Command | What it does | When |
|---|---|---|
| `make setup` | Installs the pre-commit safety net and starts local history | Once, when the kit is first unpacked. Harmless to re-run |
| `make help` | Lists every target with a one-line description | Whenever you forget one |
| `git log --oneline` | Shows the history of saves | To see what was done when |
| `git diff` | Shows unsaved changes | Before a save, to check what you're about to record |
| `git checkout HEAD -- spec/adia_v3.md` | Throws away unsaved changes to that one file | When an edit went wrong and you want the last saved version back |

---

## Installing an update from Claude

Tools arrive as `adia-tools.zip`. It contains scripts, the Makefile and the guides — **never** your spec or your tracker, so it is always safe to unpack over the kit.

```bash
unzip -o "$(ls -t ~/Downloads/adia-tools*.zip | head -1)" -d ~/Documents/adia-spec/local-kit
```

That picks the newest zip in Downloads whatever it's called. Then `ls defects/` to confirm the file you expected actually arrived.

Individual scripts arrive as `.py` files. Move them into `defects/`:

```bash
mv ~/Downloads/apply_something.py ~/Documents/adia-spec/local-kit/defects/
```

Register changes to `defects.yaml` arrive as a snippet to paste into the terminal, never as a replacement file — the tracker is yours and carries your hand edits.

---

## The rules that prevent most problems

1. **Read-only commands are always safe:** `status`, `check`, `explain`, `validate`, `help`, `git log`, `git diff`, anything with `--dry-run`. Run them freely.
2. **Writing commands get a dry-run first** where one exists.
3. **`make save` after every real change.** It's the undo button for everything else.
4. **Never edit `register.md` or the Editor's Notes by hand.** Both regenerate; edits are lost on the next save. Edit `defects.yaml` and the spec instead.
5. **Never type `Verified` into the tracker,** and never type any status on an item marked `check: auto`. The checker owns those.
6. **Anchors sit above their headings.** When inserting a section, insert above the anchor of the section that follows, not between it and its heading.

---

## A typical day

```bash
cd ~/Documents/adia-spec/local-kit
make status                                  # where am I
make explain ID=E-518                        # what exactly is wrong
# ... edit spec/adia_v3.md in BBEdit ...
make tidy                                    # if anything was pasted in
make anchors                                 # if any heading was added
make status                                  # did the count move
make ci                                      # did I break anything that used to pass
make save m="Fix E-518, E-519: flow description grammar"
```
