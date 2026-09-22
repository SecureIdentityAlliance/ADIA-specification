#!/usr/bin/env python3
"""
C-303: add a Conformance clause.

    python3 defects/apply_conformance.py --dry-run
    python3 defects/apply_conformance.py

Inserted as clause 1.1, at the end of the Introduction, so nothing is
renumbered two days before submission. Also corrects the sentence in clause 1
that declares all text normative, which the conformance clause contradicts.

The clause names clauses 6 to 10 and Appendix B as normative. Clauses 8, 9 and
10 currently contain no BCP 14 key words (C-302), so inserting this clause
raises the priority of that item: the conformance clause asserts requirements
that the protocol clauses do not yet express in normative form.
"""

import sys, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

OLD_NORMATIVE = "All text is normative unless otherwise labeled."
NEW_NORMATIVE = "The normative and informative parts of this document are identified in clause 1.1."

CLAUSE = '''<a id="conformance"></a>
## 1.1 Conformance

### 1.1.1 Normative and informative content

Clauses 6, 7, 8, 9 and 10 and Appendix B are normative. Clauses 1 to 5, clause 11, clause 12 and Appendix A are informative, except that the references listed as normative in Appendix A are themselves normative.

Within a normative clause, requirements are expressed using the key words defined in [RFC2119] and [RFC8174]. Text that does not use those key words, including notes, examples, figures and the "NOTE to entry" text accompanying definitions, is informative and does not affect conformance.

### 1.1.2 Conformance targets

This document defines requirements for five conformance targets. An implementation claims conformance as one or more of them.

| Target | Role in the ADI Network | Principal normative clauses |
|---|---|---|
| **ADI Global Domain (AGD)** | Root authority; enrols Interchanges; publishes the network directory and trust anchor | 6.4.1, 6.6, 6.7, 7.3.1, 8.1, 8.2 |
| **Interchange** | Enrols Credential Issuers, Service Providers and Users; operates the Digital Address Service and Cloud User Agents | 6.4.2, 6.6, 6.7, 7.2, 7.3.2, 7.4, 8.3, 8.4, 8.5 |
| **Credential Issuer** | Proofs claims and issues Verifiable Credentials to Users | 6.5.1, 6.7, 9 |
| **Service Provider** | Requests and verifies Verifiable Presentations | 6.5.2, 10 |
| **Digital Address Application** | The User's device application; performs strong authentication and authorises signing | 7.2.3.2, 7.2.4 |

The Cloud User Agent is a component of the Interchange and is not a separate conformance target.

### 1.1.3 Conditions of conformance

An implementation conforms as a given target if all of the following hold:

1. It satisfies every requirement expressed with MUST, MUST NOT, REQUIRED, SHALL or SHALL NOT that is addressed to that target in the normative clauses.
2. It produces, on every interface it exposes, messages that validate against the schemas in Appendix B, and it accepts every message defined there for that target.
3. Where the target signs, it uses only signature algorithms permitted by this document, and where it verifies, it applies the verification procedure of clause 6.2 and, for presentations, the procedure of clause 10.3.
4. Where the target issues credentials, it publishes credential status as required by this document.
5. Where the target authenticates Users, it meets the authenticator and assurance requirements of clause 7.2.4 for every assurance level it asserts, and asserts no level it does not meet.

Requirements expressed with SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED and MAY describe preferred or permitted behaviour and do not affect conformance.

### 1.1.4 Extensions

An implementation MAY support features not defined in this document, provided that no such feature contradicts a requirement of this document, and that the implementation continues to conform when the feature is not exercised. Extensions to the data model MUST use property names outside the vocabulary of Appendix B.

### 1.1.5 Conformance claims

A conformance claim MUST state the target or targets for which conformance is claimed and the version of this document against which it is made. A claim MUST NOT be made for a target where any requirement of clause 1.1.3 is unmet.

'''


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()
    done = []

    if '<a id="conformance"></a>' in text:
        print("  conformance clause already present")
    else:
        m = re.search(r'\n(<a id="[^"]*"></a>\n)?# 2\. ', text)
        if not m:
            print("  clause 2 heading not found; nothing inserted"); sys.exit(1)
        text = text[:m.start()] + "\n\n" + CLAUSE + text[m.start():]
        done.append("clause 1.1 Conformance inserted before clause 2")

    if OLD_NORMATIVE in text:
        text = text.replace(OLD_NORMATIVE, NEW_NORMATIVE, 1)
        done.append('clause 1: "all text is normative" replaced with a pointer to 1.1')
    elif NEW_NORMATIVE in text:
        pass
    else:
        print("  NOTE: the 'all text is normative' sentence was not found -- check clause 1 by hand")

    for l in done: print("  " + l)
    print("\n  Reminder: clauses 8-10 contain no BCP 14 key words yet (C-302). "
          "This clause asserts they are normative.")

    if dry:
        print("\n  --dry-run: nothing written"); return
    if not done:
        print("\n  nothing to change"); return
    text = re.sub(r"\n{3,}", "\n\n", text)
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written -- now run: make anchors && make notes")


if __name__ == "__main__":
    main()
