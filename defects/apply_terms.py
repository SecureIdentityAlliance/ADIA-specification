#!/usr/bin/env python3
"""
E-529: normalise capitalisation of three terms.

    python3 defects/apply_terms.py --dry-run
    python3 defects/apply_terms.py

Canonical forms:
    ADI-Network      (not "ADI Network", "ADI network")
    DIDdoc           (not "DIDDoc", "DID Document")
    USER_AGENT       (not "User Agent", "user agent", "User-Agent", "user_agent")

Kept as-is, deliberately:
    "Cloud User Agent"   the component's proper name (clause 7.2.3.1 heading,
                         Mermaid participant labels). USER_AGENT is the actor
                         token in flow text; both refer to the same component.
    "DID Document"       only inside Appendix A reference titles.
    DID_DOC              an object name in message lines.
    ~user_agent/         endpoint paths.

Never touched: code fences, anchor lines, link targets, the Editor's Notes
clause, Appendix A. Safe to re-run.
"""

import sys, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

RULES = [
 # (pattern, replacement, label)
 (r"\bADI Networks\b",                    "ADI-Networks", "ADI Networks -> ADI-Networks"),
 (r"\bADI [Nn]etwork\b",                  "ADI-Network",  "ADI Network -> ADI-Network"),
 (r"\bDIDDocs\b",                          "DIDdocs",      "DIDDocs -> DIDdocs"),
 (r"\bDIDDoc\b",                           "DIDdoc",       "DIDDoc -> DIDdoc"),
 (r"\bDID Documents\b",                    "DIDdocs",      "DID Documents -> DIDdocs"),
 (r"\bDID Document\b",                     "DIDdoc",       "DID Document -> DIDdoc"),
 (r"(?<!Cloud )\bUser Agents\b",           "USER_AGENTs",  "User Agents -> USER_AGENTs"),
 (r"(?<!Cloud )\bUser[ -]Agent\b",         "USER_AGENT",   "User Agent / User-Agent -> USER_AGENT"),
 (r"\buser[ -]agent\b",                    "USER_AGENT",   "user agent / user-agent -> USER_AGENT"),
 (r"(?<![~/\w])user_agent\b",              "USER_AGENT",   "user_agent -> USER_AGENT (not in paths)"),
]


def protect(line):
    """Return (line, restore) with link targets and endpoint paths masked."""
    tokens = []
    def mask(m):
        tokens.append(m.group(0)); return "\x00%d\x00" % (len(tokens) - 1)
    line = re.sub(r"\]\([^)]*\)", mask, line)        # link targets
    line = re.sub(r"~[a-z_]+/[A-Za-z_/{}.-]*", mask, line)  # endpoint paths
    def restore(l):
        for i, tok in enumerate(tokens):
            l = l.replace("\x00%d\x00" % i, tok)
        return l
    return line, restore


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()
    lines = text.split("\n")
    from collections import Counter
    counts = Counter()

    fence = False; in_notes = False; in_appx_a = False
    out = []
    for l in lines:
        if l.startswith("```"): fence = not fence; out.append(l); continue
        if "<!-- EDITORS-NOTES-START" in l: in_notes = True
        if "<!-- EDITORS-NOTES-END" in l:   in_notes = False; out.append(l); continue
        if re.match(r"^# Appendix A", l):    in_appx_a = True
        if re.match(r"^# Appendix B", l):    in_appx_a = False
        if fence or in_notes or in_appx_a or l.startswith("<a id="):
            out.append(l); continue

        work, restore = protect(l)
        for pat, rep, label in RULES:
            work, n = re.subn(pat, rep, work)
            if n: counts[label] += n
        out.append(restore(work))

    new = "\n".join(out)
    total = sum(counts.values())
    for label, n in counts.most_common():
        print("  %4d  %s" % (n, label))
    print("\n  %d replacements" % total)

    if dry: print("\n  --dry-run: nothing written"); return
    if not total: print("\n  nothing to change"); return
    open(SPEC, "w", encoding="utf-8").write(new)
    print("\n  written -- now run: make notes")


if __name__ == "__main__":
    main()
