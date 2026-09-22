#!/usr/bin/env python3
"""
B-202 and B-207: correct the flow-description message lines.

    python3 defects/apply_flow_fixes.py --dry-run
    python3 defects/apply_flow_fixes.py

Narrow by design. The bold message lines in the Flow Description sections are
step markers inside the narrative, not a redundant list duplicating the Mermaid
diagram, so they are corrected rather than deleted.

Of the five USER_AGENT -> USER_AGENT lines, only two are defects:

    "Vet user and issue ADI-Network User VC"   the subject's own agent cannot
    "Sign and create ADI-Network User VC"      issue the subject's role VC (B-202)

The other three are legitimate self-calls: selecting an address, being notified
of issuance, and creating and signing a VP -- all things the User Agent does
alone.

B-207 replaces the biometric round trip with WebAuthn user verification, per
§7.2.4.5: biometric comparison happens inside the authenticator and reaches the
network only as UV=1.
"""

import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

EDITS = [
 # ---- B-202: the Interchange issues the User's role credential ----
 ("B-202  vetting and issuance actor",
  "**USER_AGENT -\\> USER_AGENT :  Vet user and issue ADI-Network User VC **",
  "**INTERCHANGE -\\> USER_AGENT:  Vet user and issue ADI-Network User VC**"),

 ("B-202  signing actor",
  "**USER_AGENT -\\> USER_AGENT:  Sign and create ADI-Network User VC**",
  "**INTERCHANGE -\\> INTERCHANGE:  Sign and create ADI-Network User VC**"),

 # ---- B-207: user verification is UV=1 inside an assertion ----
 ("B-207  biometric request",
  "**USER_AGENT -\\> USER:  Request Biometric approval**",
  "**USER_AGENT -\\> DAA:  Request WebAuthn assertion, challenge = SHA-256(VP payload), UV required**"),

 ("B-207  biometric response",
  "**USER -\\> USER_AGENT: Biometric approval given**",
  "**DAA -\\> USER_AGENT: WebAuthn assertion (UV=1)**"),
]

# prose that introduces the two corrected steps, so narrative and marker agree
PROSE = [
 ("B-202  narrative already correct — no change needed",
  "The interchange will vet the user identity and issue an ADI-Network User VC to the user.",
  "The interchange will vet the user identity and issue an ADI-Network User VC to the user."),
]


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()
    done, already, missing = [], [], []

    for label, find, repl in EDITS:
        if find in text:
            text = text.replace(find, repl, 1); done.append(label)
        elif repl in text:
            already.append(label)
        else:
            missing.append(label)

    for l in done:    print("  updated : %s" % l)
    for l in already: print("  already : %s" % l)
    for l in missing: print("  NOT FOUND, left alone : %s" % l)

    left = text.count("USER_AGENT -\\> USER_AGENT")
    print("\n  remaining USER_AGENT self-calls: %d  (expected 3, all legitimate)" % left)

    if dry:
        print("\n  --dry-run: nothing written"); return
    if not done:
        print("\n  nothing to change"); return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written")


if __name__ == "__main__":
    main()
