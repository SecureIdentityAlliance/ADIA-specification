#!/usr/bin/env python3
"""
D-405 (part): HIDA is mandatory within an Interchange.

    python3 defects/apply_hida.py --dry-run
    python3 defects/apply_hida.py

Rationale. RK's D-404 answer produced this requirement in §7.4.1:

    "An Interchange MUST ensure that it issues no more than one Digital Address
     to the same natural person, determined by HIDA comparison under §7.4.2."

HIDA is the only mechanism the specification defines for that check, so the two
statements that describe HIDA as optional are inconsistent with it. This script
corrects them. It does NOT specify the HIDA construction -- algorithm, keying
and canonicalization remain open under D-405.

Also repairs a Google Docs link that survived the F-601 pass.
"""

import sys, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

EDITS = [
 ("§6.7.3 — HIDA is not implementation-specific",
  "HIDA usage is implementation-specific and should be set by ADI-Provider governance policies.",
  "Every Interchange MUST compute and retain a HIDA for each participant it enrolls, and MUST use it to satisfy the one-Digital-Address-per-person requirement of §7.4.1. Which PII attributes comprise the HIDA, and the retention period, are set by ADI-Provider governance policies."),

 ("§7.4.2 — HIDA usage is optional",
  " HIDA usage is optional.",
  "HIDA usage is REQUIRED. An Interchange cannot satisfy §7.4.1 without it. The choice of contributing PII attributes is set by governance policies; the requirement to perform the comparison is not optional."),

 ("§6.7.3 — construction scope is the Interchange, not the region",
  "HIDA construction, management and usage rules are defined within a region scope.",
  "HIDA construction, management and usage rules are set by governance policy and applied within the scope of a single Interchange."),

 ("§7.4.2 — stray Google Docs link",
  "See [Governance HIDA](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#heading=h.g7c9avwei6bl).",
  "See [Governance HIDA](#governance-hida)."),

 ("§8.5 flow — HIDA is not conditional",
  "DAA->>DAS: POST ~ix/enroll_user (FIDO public key, HIDA if required, forms)",
  "DAA->>DAS: POST ~ix/enroll_user (FIDO public key, HIDA, forms)"),
]


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()
    done, already, missing = [], [], []

    for label, find, repl in EDITS:
        if find in text:
            text = text.replace(find, repl, 1); done.append(label)
        elif repl.split(".")[0][:45] in text:
            already.append(label)
        else:
            missing.append(label)

    # the stray link may be wrapped differently; catch any remaining one in this area
    if "docs.google.com" in text:
        text = re.sub(r"\[([^\]]*Governance[^\]]*)\]\(https://docs\.google\.com[^)]*\)",
                      r"[\1](#governance-hida)", text)
        if "docs.google.com" not in text:
            done.append("§7.4.2 — stray Google Docs link (regex fallback)")

    for l in done:    print("  updated : %s" % l)
    for l in already: print("  already : %s" % l)
    for l in missing: print("  NOT FOUND, left alone : %s" % l)

    if "docs.google.com" in text:
        print("\n  NOTE: %d Google Docs link(s) still present -- run: make explain ID=F-601"
              % text.count("docs.google.com"))

    if dry:
        print("\n  --dry-run: nothing written"); return
    if not done:
        print("\n  nothing to change"); return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written -- now run: make explain ID=F-601 && make explain ID=F-603")


if __name__ == "__main__":
    main()
