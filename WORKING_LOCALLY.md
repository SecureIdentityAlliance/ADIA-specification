# Working Locally — Setup and Daily Use

No GitHub account needed. Everything runs on your own machine.

Worth separating two things that sound alike: **git** is version history that
lives in a hidden folder on your computer — free, no account, works offline.
**GitHub** is a shared copy on the internet. You can have the first today and
add the second whenever the repository arrives. Nothing you do now gets thrown
away when that happens.

---

## 1. One-time setup

### What you need

- **Python 3** — Macs have it. Check by opening Terminal and typing
  `python3 --version`. If it errors, install from python.org.
- **git** — also on most Macs. Check with `git --version`. If it errors, macOS
  will offer to install it for you.

### Steps

Put the `local-kit` folder somewhere sensible — `~/Documents/adia-spec` is fine.
Then open Terminal and run:

```bash
cd ~/Documents/adia-spec
make setup
```

You should see:

```
Ready. Try: make status
```

That installed the safety net and started version history. You will not need
to run it again.

If `make setup` complains about `pyyaml`, run this once and try again:

```bash
python3 -m pip install pyyaml
```

---

## 2. What you now have

```
adia-spec/
├── spec/adia_v3.md          the specification
├── defects/
│   ├── defects.yaml         the tracker — the file that gets edited
│   ├── register.md          the report — writes itself
│   ├── adia_checks.py       the automatic checker
│   ├── render.py            builds the report
│   └── validate.py          catches typos
├── Makefile                 the commands below
└── github-later/            two files to use when the repo exists
```

---

## 3. The commands

Type `make help` any time to see this list.

| Command | What it does |
|---|---|
| `make status` | How many problems are left |
| `make check` | The full checker report |
| `make register` | Rebuild the report |
| `make validate` | Check the tracker file for typos |
| `make ci` | Has anything that used to pass started failing? |
| `make explain ID=E-501` | **Why** a check fails — shows the exact lines |
| `make relocate` | Refresh line numbers in the tracker after editing the spec |
| `make save m="what you did"` | Record today's work |

### A normal session

```bash
cd ~/Documents/adia-spec
```

Edit `defects/defects.yaml` in a text editor — BBEdit is ideal. Then:

```bash
make save m="Assign A-101 to RK"
```

That's it. The report rebuilds and the change is recorded, in one step.

---

## 4. The safety net

A check runs automatically every time you save. If the tracker file has a
problem, **nothing is saved** and you get a plain-English explanation. Real
examples:

```
PROBLEM: Line 25 contains a Tab character.
  YAML cannot use Tabs. Delete it and press the space bar instead.
```

```
PROBLEM: A-102 has an unrecognised status: 'fixed'
  Allowed: Open, Fixed, Verified, Rejected,
           Blocked(D4), Superseded(A-102)
  Capital letters matter — 'fixed' is not the same as 'Fixed'.
```

```
PROBLEM: Two entries share the ID E-509 (entries 79 and 80).
  You probably copied an entry instead of editing it.
  Delete the copy you added.
```

Fix what it describes and run `make save` again. A blocked save is not a
failure — it is the system doing its job before a mistake reaches the report.

---

## 5. Editing the spec itself

Same rhythm. Edit `spec/adia_v3.md`, then:

```bash
make status
```

Fixed defects change from `FAIL` to `ok` on their own — the checker reads the
document rather than being told. Then:

```bash
make save m="Fix A-102: id_doc carries the subject key"
```

Putting the defect ID in the message is worth the two seconds. The report's
Ref column fills itself in from those messages, so every finished item ends up
linked to the change that closed it.

**Before a run of spec edits, set your starting point:**

```bash
make ci
```

The first time, this records what currently passes. From then on it warns you
if something that used to work has broken — which is exactly the partial-fix
problem worth catching early.

---

## 6. Undoing things

Everything is recoverable.

See what you've changed since the last save:

```bash
git diff
```

Throw away today's unsaved changes to one file:

```bash
git checkout HEAD -- defects/defects.yaml
```

See the history:

```bash
git log --oneline
```

If you need to go further back than that, ask a developer. They can restore any
previous version in seconds, and the fact that you saved regularly is what
makes it easy.

---

## 7. The one real limitation

Without GitHub there is no shared copy, so **only one machine can hold the
real version at a time.** Two people editing their own copies will produce two
diverging files that have to be merged by hand — tedious and error-prone.

Until the repository exists, pick one of these:

- **One owner.** One person holds the files and makes all edits. Everyone else
  sends changes by email or chat for that person to enter. Simplest, and fine
  for a few weeks.
- **A shared folder** (Dropbox, Drive, iCloud) with a strict rule: say in chat
  when you start editing and when you stop. Never two people at once. Sync
  services do not merge text files — they keep one version and rename the other
  as a conflicted copy, which is easy to miss.

Do not try to keep two independent copies in step manually. That is the one
thing here that genuinely goes wrong.

---

## 8. When the repository arrives

Roughly ten minutes of a developer's time:

1. Copy the two files from `github-later/` into `.github/workflows/`
2. Connect the folder to the repository and upload it

All your history comes with it — every save, every message, every restorable
version. Nothing is lost and nothing needs redoing.

After that the checks run on GitHub automatically and the report rebuilds
itself there, so `make register` becomes optional. Everything else stays the
same.

---

## 9. Summary card

**Setup, once:** `make setup`

**Every session:**
```
cd ~/Documents/adia-spec
[edit defects/defects.yaml]
make save m="what you did"
```

**Useful:** `make status` · `make check` · `make help`

**If a save is blocked:** read the message, fix that one thing, save again.

**Two spaces at the start of a line. Never a Tab.**
