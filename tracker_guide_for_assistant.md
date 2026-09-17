# Managing the ADIA Defect Tracker — A Beginner's Guide

This explains how to keep the defect tracker up to date. You do not need to
understand the specification itself, and you will not be editing it. Your job
is the bookkeeping: who is working on what, and what has been finished.

Everything here is safe. Nothing you do can damage the specification document,
and every change can be undone.

---

## 1. What the files are

There are five files. You will regularly edit **one** of them.

| File | What it is | Do you edit it? |
|---|---|---|
| `spec/adia_v3.md` | The specification itself | **No — never** |
| `defects/defects.yaml` | The tracker. One entry per problem | **Yes — this is your file** |
| `defects/register.md` | The readable report | No — it writes itself |
| `defects/adia_checks.py` | The automatic checker | **No** |
| `defects/render.py` | Builds the report | **No** |

A useful way to picture it: `defects.yaml` is the spreadsheet you type into,
and `register.md` is the printed report generated from it. You never edit the
report. You edit the spreadsheet and the report is rebuilt for you.

---

## 2. What an entry looks like

Open `defects/defects.yaml` and you will see a long list. Each problem looks
like this:

```yaml
- id: E-510
  severity: S3
  workstream: editorial
  location: L926
  defect: 'Figure 11 caption: "Creating **and** AGD"'
  fix: ''
  owner: null
  status: Open
  notes: null
  check: auto
```

**You may change exactly three lines:** `owner`, `status`, `notes`.

Leave every other line exactly as it is. In particular do not touch `defect:` —
it often contains quote marks and colons that have to stay in place.

The word `null` simply means "empty". You replace it with your text.

---

## 3. The rules

These five rules prevent essentially every problem.

1. **Only ever change `owner`, `status` or `notes`.**
2. **Never change the spacing at the start of a line.** Each of those lines
   begins with exactly two spaces. Keep them.
3. **Use the space bar, never the Tab key.** Tab characters break the file.
4. **Put your text in double quotes:** `owner: "RK"` rather than `owner: RK`.
   Both usually work, but quotes always work.
5. **Never delete an entry**, even a finished one. Finished items stay in the
   list with their status changed.

---

## 4. The status words

Only these six are allowed. Spelling and capitals matter.

| Word | What it means |
|---|---|
| `Open` | Nobody has fixed it yet |
| `Fixed` | Someone says they fixed it, but it has not been confirmed |
| `Verified` | Confirmed done |
| `Blocked(D4)` | Waiting on a decision. The number matches the decisions list |
| `Rejected` | The team decided not to fix it. Say why in `notes` |
| `Superseded(A-102)` | Merged into a different entry |

**Two of these are not yours to set.**

- Never type `Verified` yourself. Either the automatic checker sets it, or a
  second person confirms it. The person who did the work never marks their own
  work verified — that rule exists because a past "fix" was only half applied
  and nobody caught it.
- For any entry with `check: auto` at the bottom, the computer decides the
  status. If you type something there it will simply be overwritten. Leave
  those alone.

So in practice you set `Open`, `Fixed`, `Blocked(...)`, or `Rejected`, and only
on entries **without** `check: auto`.

---

## 5. How to make a change

### The easy way — in your web browser

No software needed.

1. Go to the repository on GitHub.
2. Click the `defects` folder, then `defects.yaml`.
3. Click the **pencil icon** at the top right.
4. Press `Ctrl-F` (`Cmd-F` on a Mac) and search for the ID, e.g. `E-510`.
5. Make your change.
6. Scroll to the bottom, type a short note in the description box such as
   `Assign E-510 to RK`, and click **Commit changes**.

That's it. Within about a minute the report rebuilds itself. You'll see a small
tick or cross next to your change on the repository's front page — a tick means
all is well.

### The local way — using the terminal

If you'd rather work on your own computer, four commands cover everything.

```bash
cd adia-spec          # move into the project folder
git pull              # get everyone else's latest changes
```

Now edit `defects/defects.yaml` in a plain text editor (BBEdit is ideal).

```bash
make register         # rebuild the report
```

You should see something like:

```
wrote defects/register.md  (3 of 105 verified)
```

Then save your work back:

```bash
git add -A
git commit -m "Assign E-510 to RK"
git push
```

**Always run `git pull` before you start.** It takes a second and avoids the
most common headache — two people editing the same file at once.

---

## 6. The jobs you'll actually do

### Assign someone to a problem

Find the entry, put their initials in `owner`:

```yaml
  owner: "RK"
```

### Record that someone finished something

Change `status` to `Fixed`:

```yaml
  owner: "RK"
  status: Fixed
```

Leave it at `Fixed`. Somebody else moves it to `Verified`.

### Add a note

```yaml
  notes: "RK waiting on the Tuesday call before starting"
```

If your note contains a double quote mark, use single quotes around the whole
thing instead:

```yaml
  notes: 'Discussed on the call — see Martin''s email'
```

### Check where things stand

In the browser: open `defects/register.md`. The table at the top gives the
totals.

In the terminal:

```bash
make check
```

The first two lines tell you what you need:

```
ADIA defect checks  --  spec/adia_v3.md
5 of 68 checks pass
```

### Produce a progress update

Open `defects/register.md` and read the summary table. It gives you verified
count, awaiting-verification count, blocked count, and open count, already
totalled. Copy those figures straight into your update.

---

## 7. When something goes wrong

### A red cross appears after you commit

The file has a typo. Click the red cross, then **Details**, and look for a line
starting with `Error`. It is almost always one of three things:

- A Tab character instead of spaces
- Changed spacing at the start of a line
- A status word misspelled, or wrong capitals (`fixed` instead of `Fixed`)

Go back and fix it the same way you made the change. Nothing is broken in the
meantime — the report simply keeps the previous version until the file reads
cleanly again.

### "Two entries share an ID"

You copied an entry instead of editing it. Delete the copy you added.

### The terminal says `make: command not found`

You're not in the right folder. Run `cd adia-spec` first.

### `git push` is rejected

Somebody else changed the file while you were working. Run:

```bash
git pull
```

then `git push` again. If it mentions a conflict, stop and ask a developer —
takes them a minute, and it is not worth learning for this.

### You want to undo something

Nothing is ever lost. Any developer can restore any previous version in
seconds. Just say what you changed and roughly when.

---

## 8. What to pass to a developer

Don't attempt these — they are not beginner tasks and getting them wrong is
genuinely awkward to unpick:

- Any edit to `spec/adia_v3.md`
- Any edit to `adia_checks.py` or `render.py`
- Anything described as a "merge conflict"
- Setting an entry to `Verified`
- An entry showing `Blocked` where the decision has now been made — the
  developer needs to confirm the work can actually start

---

## 9. One-page summary

**You edit:** `defects/defects.yaml`
**You change:** `owner`, `status`, `notes` — nothing else
**You never type:** `Verified`
**You never touch:** entries marked `check: auto`

**Browser:** pencil icon → edit → Commit changes
**Terminal:** `git pull` → edit → `make register` → `git add -A` → `git commit -m "..."` → `git push`

**Status words:** `Open` · `Fixed` · `Blocked(D4)` · `Rejected`

**Two spaces at the start of a line. Never a Tab.**
