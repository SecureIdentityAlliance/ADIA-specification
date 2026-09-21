#!/usr/bin/env python3
"""
D-404 / D-405: apply the Digital Address uniqueness model confirmed by RK.

    python3 defects/apply_da_uniqueness.py --dry-run
    python3 defects/apply_da_uniqueness.py

The model:
  * Interchange names are assigned by the AGD and are network-unique.
  * An Interchange ensures no two Digital Addresses it issues share a local part.
    Network-wide uniqueness of the Digital Address follows automatically.
  * An Interchange ensures it issues at most one Digital Address per natural
    person, determined by HIDA. This is scoped to one Interchange.
  * A person MAY hold Digital Addresses at several Interchanges, and the network
    does not determine that they refer to the same person.

Edits are exact-string replacements, so anything already reworded is reported
rather than silently missed. Safe to re-run.
"""

import sys, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

EDITS = [
 # (label, find, replace)
 ("§3.11 ADI-Region — scope of uniqueness",
  "> Virtual or physical scope or boundaries for the uniqueness of a Digital Address.",
  "> Virtual or physical grouping of Interchanges for governance and routing purposes.\n>\n> Note: A Region is not the scope of Digital Address uniqueness. Digital Addresses are unique within an Interchange, and network-unique by construction; see §7.4.1."),

 ("§3.11 Note 2 — entity uniqueness scope",
  "> Note 2 to entry: Entities within an ADI-Region are unique when they do not have matching HIDAs.",
  "> Note 2 to entry: An Interchange determines that two enrollment applicants are the same entity when their HIDAs match. This comparison is performed within a single Interchange and is not performed across Interchanges."),

 ("§3.21 Note 2 — DA uniqueness scope",
  "> Note 2 to entry: A DA must be unique within an ADI-Region.",
  "> Note 2 to entry: A Digital Address is unique within the Interchange that issued it. Because Interchange names are network-unique, every Digital Address is unique within the ADI Network."),

 ("§3.24 Note 1 — HIDA purpose",
  "> Note 1 to entry: The HIDA is a key driver for performing lookup operations to ensure that no two entities have the same DA within an ADI-Region. HIDAs are used to ensure uniqueness among entities that are applying for a DID and/or DA.",
  "> Note 1 to entry: An Interchange uses the HIDA to determine whether an enrollment applicant already holds a Digital Address issued by that Interchange, so that it issues at most one Digital Address per natural person. HIDAs are not compared across Interchanges."),

 ("§7.2.1 DAS — HIDA enforcement",
  "The DAS records the public keys of Digital Addresses & DIDs, maintains Network Directories and may enforce HIDA uniqueness.",
  "The DAS records the public keys of Digital Addresses and DIDs, maintains Network Directories, and enforces Digital Address and HIDA uniqueness within its own Interchange."),

 ("§7.4.1 Digital Address — definition and uniqueness",
  "A **Digital Address i**s an identifier that is unique in an ADI-Network.   It has the form of username@interchange_name.  For example, alice@interchange_1.",
  "A **Digital Address** is an identifier of the form `local@interchange`, where `local` is 1 to 64 characters from ALPHA, DIGIT, \".\", \"_\" and \"-\", and `interchange` is an Interchange name assigned by the AGD. For example, `alice@interchange_1`. Comparison is case-insensitive and Digital Addresses are stored in lowercase. In this version `local` is restricted to ASCII.\n\nInterchange names are assigned by the AGD at enrollment and MUST be unique within the ADI Network. The AGD MUST reject an enrollment request naming an Interchange name already in use.\n\nAn Interchange MUST ensure that no two Digital Addresses it issues share the same `local` part. Because Interchange names are network-unique, every Digital Address is therefore unique within the ADI Network.\n\nAn Interchange MUST ensure that it issues no more than one Digital Address to the same natural person, determined by HIDA comparison under §7.4.2. This requirement is scoped to a single Interchange. A natural person MAY hold Digital Addresses issued by more than one Interchange, and the ADI Network does not determine whether Digital Addresses issued by different Interchanges refer to the same person."),

 ("§7.4.2 HIDA — enforcement scope",
  "Participant uniqueness can be globally or regionally enforced by creating a participant HIDA (Hashed ID Attributes) from required PII data.   The hashed PII data will produce a digital fingerprint that can be used to check for pre-existence of an identity to ensure uniqueness.",
  "Participant uniqueness is enforced by the enrolling Interchange by creating a participant HIDA (Hashed ID Attributes) from required PII data. The HIDA produces a digital fingerprint that the Interchange compares against the HIDAs of its own participants, to determine whether an applicant already holds a Digital Address issued by that Interchange.\n\nHIDAs MUST NOT be compared across Interchanges. A participant's HIDA is computed using a key held by the enrolling Interchange and is not disclosed to other Interchanges or to the AGD."),

 ("§8.5 enrollment — HIDA check scope",
  "- The User HIDA is verified for uniqueness, and an ADI-Network User VC is issued to the user for participation in the ADI ecosystem.",
  "- The User HIDA is compared against the HIDAs held by the enrolling Interchange to confirm the applicant does not already hold a Digital Address there, and an ADI-Network User VC is issued to the user for participation in the ADI ecosystem."),

 ("§7.4.1 implementation option — region suffix",
  "*Implementation option:  user, issuer, service provider and interchange digital addresses may contain a suffix containing ADI region.  For example, [issuer1@ix3.region](mailto:issuer1@ix3.region)1  or the interchange id can be globally unique.*",
  "*Implementation option: an Interchange name may itself be structured, for example `ix3.region1`, provided the whole name is unique within the ADI Network. Structure within the Interchange name has no protocol meaning.*"),
]


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()
    done, already, missing = [], [], []

    for label, find, repl in EDITS:
        if repl.split("\n")[0][:50] in text and find not in text:
            already.append(label); continue
        if find not in text:
            missing.append(label); continue
        text = text.replace(find, repl, 1)
        done.append(label)

    for l in done:    print("  updated : %s" % l)
    for l in already: print("  already : %s" % l)
    for l in missing: print("  NOT FOUND, left alone : %s" % l)

    if dry:
        print("\n  --dry-run: nothing written"); return
    if not done:
        print("\n  nothing to change"); return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written -- now run: make tidy && make relocate")


if __name__ == "__main__":
    main()
