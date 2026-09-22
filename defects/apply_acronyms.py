#!/usr/bin/env python3
"""
D-414: add the acronym table that §4 promises but does not contain.

    python3 defects/apply_acronyms.py --dry-run
    python3 defects/apply_acronyms.py

Inserts the table as §4.1 and renumbers the two existing subsections to §4.2
and §4.3. Nothing in the document cites §4.1 or §4.2 by number, and the anchors
are derived from heading text rather than numbers, so nothing breaks.

Also repairs one surviving "Authoritative Global Domain" missed by the rename.

Safe to re-run.
"""

import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

TABLE = '''<a id="acronyms"></a>
## 4.1 Acronyms

| Acronym | Expansion | Defined in |
|---|---|---|
| AAL | Authentication Assurance Level — the strength of an authentication event, per NIST SP 800-63B | §7.2.4 |
| ADI | Accountable Digital Identity | §1 |
| ADIA | Accountable Digital Identity Association | §1 |
| AGD | ADI Global Domain — the root authority of an ADI Network | §3.15, §6.4.1 |
| CI | Credential Issuer (ADI-CI) | §3.4, §6.5.1 |
| DA | Digital Address — an entity identifier of the form `local@interchange` | §3.21, §7.4.1 |
| DAA | Digital Address Application — the application on the User's device that performs strong authentication | §7.2.3.2 |
| DAS | Digital Address Service — the component within an AGD or Interchange that creates and maintains Digital Addresses | §7.2.1 |
| DID | Decentralized Identifier | §3.19, §7.4.3 |
| DIDDoc | DID Document — the document bound to a DID, containing its verification keys and metadata | §3.20 |
| FAL | Federation Assurance Level — the strength of an assertion conveying an authentication event to a relying party, per NIST SP 800-63C | §7.2.4 |
| HIDA | Hash of (Subject) ID Attributes — a digest of PII used to establish that an applicant is not already enrolled | §3.24, §6.7.3, §7.4.2 |
| IAL | Identity Assurance Level — the rigour of identity proofing, per NIST SP 800-63A | §7.2.4 |
| IX | Interchange (ADI-IX) | §3.6, §6.4.2 |
| KYC | Know Your Customer — regulated identity verification performed by financial institutions | §11.1 |
| PII | Personally Identifiable Information | §6.7.3 |
| SP | Service Provider (ADI-SP) — in this document, equivalent to the Relying Party and Verifier roles | §3.12, §6.5.2 |
| VC | Verifiable Credential | §3.25, §6.2 |
| VP | Verifiable Presentation | §10.1 |

'''

EDITS = [
 ("renumber 4.1 -> 4.2", "## 4.1 ADI-Role VCs", "## 4.2 ADI-Role VCs"),
 ("renumber 4.2 -> 4.3", "## 4.2 Identifiers", "## 4.3 Identifiers"),
 ("stray old AGD expansion", "Authoritative Global Domain", "ADI Global Domain"),
]


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()
    done, already, missing = [], [], []

    if "<a id=\"acronyms\"></a>" in text:
        already.append("acronym table")
    else:
        # renumber first, so the anchors above each heading are untouched
        for label, find, repl in EDITS[:2]:
            if find in text:
                text = text.replace(find, repl, 1); done.append(label)
            elif repl in text:
                already.append(label)
            else:
                missing.append(label)
        # insert above the anchor belonging to the first subsection
        marker = '<a id="adi-role-vcs"></a>'
        if marker in text:
            at = text.index(marker)
            text = text[:at] + TABLE + text[at:]
            done.append("acronym table as §4.1")
        else:
            missing.append("acronym table (insertion point not found)")

    label, find, repl = EDITS[2]
    n = text.count(find)
    if n:
        text = text.replace(find, repl); done.append("%s (x%d)" % (label, n))

    for l in done:    print("  updated : %s" % l)
    for l in already: print("  already : %s" % l)
    for l in missing: print("  NOT FOUND, left alone : %s" % l)

    if dry:
        print("\n  --dry-run: nothing written"); return
    if not done:
        print("\n  nothing to change"); return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written -- now run: make anchors && make explain ID=F-607")


if __name__ == "__main__":
    main()
