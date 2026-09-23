# Publishing to GitHub — Guide

For posting the v3.0 draft and its supporting material to the SIA organisation once editing is complete.

---

## 1. The decision: existing repo or new repo

You have a local git repository already. Every `make save` since setup is a commit with a message; the register, the Editor's Notes and the check results are all in that history. That history is worth keeping, and it is the main thing the decision affects.

| | New repository | Existing ADIA repository |
|---|---|---|
| Push the kit | One command; history intact | Two unrelated histories must be merged, or yours squashed |
| What a visitor sees | v3 draft and its tooling, nothing else | v2 published spec alongside v3 draft; status of each must be explained |
| Toolchain | Makefile, `defects/`, `spec/`, `figures/` at the root, where the scripts expect them | Must live in a subdirectory, and every script's relative path assumption breaks |
| CI | Workflows in `github-later/` work as written | Workflows need path adjustments |
| ITU Study Group | Self-contained; can be forked or transferred cleanly | Coupled to v2 history and SIA's other content |
| Continuity | Old repo README links to the new one | Everything in one place |

**Recommendation: new repository.** The kit is a coherent unit — spec, figures, register, checks, guides — and the scripts assume they sit at the repository root. Putting it in a subdirectory of the existing repo means either restructuring the kit or editing every script's path logic, two days before you want it stable. And the status distinction matters: v2 is a published specification, v3 is a draft under ITU contribution. Two repos make that unambiguous; one repo needs a README paragraph to explain it, and readers skip README paragraphs.

The existing repo is not abandoned. Its README gets a prominent link to the new one, and when v3 is approved the two can be reconciled — by then you'll know whether the ITU wants the canonical copy in their own space anyway.

If you choose the existing repo regardless, §8 covers it.

---

## 2. Before you push

Do these in order. Each takes under a minute.

**2.1 Final state.**
```bash
cd ~/Documents/adia-spec/local-kit
make tidy
make anchors
make notes
make status
make ci
make save m="Final edits before ITU contribution"
```

**2.2 Move the workflows into place.** They were staged in `github-later/` for exactly this moment.
```bash
mkdir -p .github/workflows
git mv github-later/register.yml .github/workflows/
git mv github-later/spec.yml .github/workflows/
rmdir github-later
```

**2.3 Add a README.** Visitors land on it. Keep it short — what this is, its status, where the outstanding work is, how to run the checks:
```bash
cat > README.md <<'EOF'
# Accountable Digital Identity Architecture — Specification v3.0 (draft)

Draft specification of the ADI Association, contributed to ITU-T in September 2026.
Work in progress: the outstanding items are listed in the Editor's Notes clause of the specification.

- **Specification:** [spec/adia_v3.md](spec/adia_v3.md)
- **Outstanding work:** [Editor's Notes](spec/adia_v3.md#editors-notes)
- **Defect register:** [defects/register.md](defects/register.md)
- **Previous version (v2.0):** see the ADIA repository

## Working on this document

See [WORKING_LOCALLY.md](WORKING_LOCALLY.md) for setup, [CHEAT_SHEET.md](CHEAT_SHEET.md) for the commands,
and [EDITING_DIAGRAMS.md](EDITING_DIAGRAMS.md) before touching a figure.

Automated checks run on every push. `make status` runs them locally.
EOF
```

**2.4 Ignore what shouldn't be tracked.**
```bash
cat > .gitignore <<'EOF'
.DS_Store
*.pdf
__pycache__/
EOF
```
Remove `*.pdf` from that list if you want a rendered PDF in the repo; otherwise generate it at release time.

**2.5 Decide visibility.** A public repository is visible to anyone; a private one only to people you invite. The Study Group will need access either way. Public is simpler for an ITU contribution — nobody has to be invited, and links in the contribution just work. If SIA policy requires private, you'll invite SG members in §6.

**2.6 Commit the housekeeping.**
```bash
git add -A
git commit -m "Prepare for publication: README, workflows, gitignore"
```

---

## 3. Authentication, once

GitHub no longer accepts a password for `git push`. The simplest route is GitHub's own command-line tool:

```bash
brew install gh
gh auth login
```

Choose **GitHub.com**, **HTTPS**, and **Login with a web browser**. It opens a browser page, you paste a code, done. This stores a token that `git` then uses automatically. You will not be asked again.

Confirm you can see the organisation:
```bash
gh org list
```

`SIA` should appear. If not, your account isn't a member with repository-creation rights — ask the org owner before going further.

---

## 4. Create the repository and push

One command creates the repo in the organisation, connects your local kit to it, and pushes everything including the full history:

```bash
cd ~/Documents/adia-spec/local-kit
gh repo create SIA/adia-specification-v3 --public --source=. --push \
  --description "ADI Association Specification v3.0 (draft, ITU-T contribution)"
```

Substitute `--private` if that's the decision from §2.5, and adjust the name if `adia-specification-v3` collides with something. Avoid a name with `v3` in it if this repo will carry later versions too — `adia-specification` with git tags per version ages better.

If that succeeds, the output ends with a URL. Open it.

**If `gh repo create` is refused** (no permission to create in the org), have the org owner create an empty repository and give you write access, then connect to it:
```bash
git remote add origin https://github.com/SIA/adia-specification-v3.git
git branch -M main
git push -u origin main
```

---

## 5. Verify it landed correctly

Open the repository in a browser and check five things. Each is a known failure mode of this specific kit.

1. **`spec/adia_v3.md` renders**, and the table of headings on the right (GitHub's outline) shows clause numbers 1–14 and Appendices A–B.
2. **Figures display.** Scroll to Figure 4 — the pyramid should be visible. If you see a broken-image icon, the `spec/figures/` folder didn't upload; check `git status` locally for untracked SVGs.
3. **Mermaid renders.** Scroll to Figure 15 (Enrolling a User). You should see a sequence diagram, not a code block. If it's a code block, the fence is ` ```mermaid ` with a typo.
4. **Anchors work.** Click the "Editor's Notes" link in the README. It should scroll to clause 14.
5. **Actions ran.** Click the **Actions** tab. Two workflows should have run on your push. Green means the checks and the register are consistent; red means click in and read — most likely `pyyaml` install or a permission issue (§7).

---

## 6. Make it accessible

**Public repo:** nothing to do. Send the URL.

**Private repo:** Settings → Collaborators and teams → Add people. Invite Study Group members by GitHub username, **Read** access. Anyone who will edit needs **Write**.

**Protect `main`** either way: Settings → Branches → Add rule → branch name `main` → tick *Require a pull request before merging*. This stops anyone — including you — pushing directly. Edits go through pull requests, which is where the Actions checks earn their keep.

---

## 7. Enable the workflows to write back

The `register.yml` workflow regenerates `register.md` and the Editor's Notes on every push and commits the result. For that it needs permission to push:

Settings → Actions → General → **Workflow permissions** → select *Read and write permissions* → Save.

Without this the workflow runs, produces the updated files, and fails at the commit step with a permissions error. It's the most common red cross on day one.

---

## 8. If you choose the existing ADIA repo instead

The kit must go in a subdirectory — `v3/`, say. The Python scripts locate the spec relative to `defects/`, so as long as `v3/spec/` and `v3/defects/` sit beside each other they keep working unchanged. Two things do break and need editing before the push: the Makefile's `SPEC := spec/adia_v3.md` becomes `SPEC := v3/spec/adia_v3.md`, and every path in the two workflow files gains the `v3/` prefix.

The push is the hard part: your local history is unrelated to the existing repo's. The clean approach is a subtree:

```bash
cd /path/to/existing-adia-repo
git subtree add --prefix=v3 ~/Documents/adia-spec/local-kit main
git push
```

That imports the kit under `v3/` with its history preserved. It's a legitimate technique but it is not beginner territory, and if it goes wrong the recovery is not obvious. A developer should drive it. This is the strongest practical argument for §1's recommendation.

---

## 9. Tag what was contributed

Once the version you submitted to the ITU is on GitHub, mark it so it can always be found regardless of later edits:

```bash
git tag -a itu-contribution-2026-09 -m "Version contributed to ITU-T, September 2026"
git push origin itu-contribution-2026-09
```

Then on GitHub: **Releases → Draft a new release → choose that tag**. Attach a rendered PDF if you have one. The release page gives the Study Group a permanent URL to the exact text they received, and the contribution document can cite it.

---

## 10. Working after publication

Nothing changes locally. The loop is the same, plus one command:

```bash
make save m="…"
git push
```

`git push` sends your saves to GitHub. The Actions run, the register and notes regenerate there, and the checks confirm nothing regressed.

If `main` is protected (§6), `git push` to it is refused and you work on a branch:

```bash
git checkout -b fix/E-527
# ... make save as usual ...
git push -u origin fix/E-527
gh pr create --fill
```

The pull request shows the diff, the Actions results, and lets a second person approve — which is also how `Fixed` items become `Verified` under the register's rules.

---

## 11. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Permission denied` on push | Not authenticated | `gh auth login` again; confirm `gh auth status` |
| `remote: Repository not found` | Wrong name or no access | `gh repo view SIA/<name>` to confirm it exists and you can see it |
| `Updates were rejected` | Someone else pushed first | `git pull --rebase` then `git push` |
| `refusing to merge unrelated histories` | Pushing the kit into a repo that already has commits | You're on the §8 path; use the subtree method |
| Red cross on Actions, "Permission denied" in the commit step | §7 not done | Settings → Actions → Read and write |
| Red cross, `No module named yaml` | pip step failed | Re-run the job; if persistent, the runner image changed — tell a developer |
| Figures show as broken images | SVGs not committed | `git status` — add and commit `spec/figures/*.svg` |
| Mermaid shows as a code block | Fence typo | Check the line reads exactly ` ```mermaid ` |

---

## 12. Sequence, end to end

```bash
cd ~/Documents/adia-spec/local-kit
make tidy && make anchors && make notes && make ci
make save m="Final edits before ITU contribution"
mkdir -p .github/workflows && git mv github-later/*.yml .github/workflows/ && rmdir github-later
# write README.md and .gitignore per §2
git add -A && git commit -m "Prepare for publication"
gh auth login                                            # once
gh repo create SIA/adia-specification-v3 --public --source=. --push
# verify per §5; set permissions per §7; protect main per §6
git tag -a itu-contribution-2026-09 -m "Contributed to ITU-T" && git push --tags
```

Roughly twenty minutes, most of it reading the verification checklist.
