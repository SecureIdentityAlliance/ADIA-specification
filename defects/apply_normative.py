#!/usr/bin/env python3
"""
C-302 / C-301: make the requirements normative.

    python3 defects/apply_normative.py --dry-run
    python3 defects/apply_normative.py

Three groups, in order of risk:

  1. Requirements sitting in clause 3 "NOTE to entry" blocks. Notes are
     informative by ISO convention, so these requirements currently have no
     force. Each becomes a descriptive note pointing at the normative clause,
     and the requirement is restated there with MUST.

  2. Lowercase must/should in clauses 6-10. Capitalised where they state a
     requirement; one is also wrong (a DIDDoc "must be" a key) and is corrected.

  3. Narrative "will" sentences in clauses 8-10 whose actor and obligation are
     unambiguous. Two are corrected as they are promoted: the SP Agent does not
     write the directory (D-412), and the Issuer does not take the subject from
     the redeeming token (A-122, contradicts clause 12.4).

Sentences describing role-VC issuance are deliberately NOT converted; they
would entrench a model the working group is about to reconsider (D13). The
Editor's Notes record that clauses 9 and 10 remain partly narrative.

Safe to re-run.
"""

import sys, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

# ── group 1: NOTE demotion + normative restatement ─────────────────────────
NOTES = [
 ("> NOTE 2 to entry: An ADI-Network must include at least one ADI-Region.",
  "> NOTE 2 to entry: An ADI-Network includes at least one ADI-Region; see clause 6.4."),
 ("> NOTE 2 to entry: ADI-Network Providers must implement at least one administrator role. This includes CI-Admin, IX-Admin, SP-Admin, and AGD-Admin.",
  "> NOTE 2 to entry: ADI-Network Providers implement at least one administrator role (CI-Admin, IX-Admin, SP-Admin or AGD-Admin); see clause 6.4."),
 ("> Note 2 to entry: An ADI-Network must include at least one ADI-Interchange.",
  "> Note 2 to entry: An ADI-Network includes at least one ADI-Interchange; see clause 6.4."),
 ("> Note 3 to entry: An ADI-Region must include at least one ADI-Interchange.",
  "> Note 3 to entry: An ADI-Region includes at least one ADI-Interchange; see clause 6.4."),
 ("> Note 2 to entry: A DID must be bound to one and only one DIDDoc.",
  "> Note 2 to entry: A DID is bound to exactly one DIDDoc; see clause 7.4.3."),
 ("> Note 3 to entry: Agents must have at least one endpoint in order to communicate.",
  "> Note 3 to entry: An Agent has at least one endpoint; see clause 7.2.2."),
]

RESTATE = {
 # anchor heading -> paragraph to insert immediately after the heading's first paragraph
 "## 6.4 ADI-Network Providers":
   "An ADI Network MUST include at least one Region and at least one Interchange, and every Region MUST include at least one Interchange. Every ADI Network Provider MUST implement at least one administrator role.",
 "### 7.2.2 Agents":
   "An Agent MUST expose at least one endpoint through which it can be reached.",
 "### 7.4.3 DID Addressing":
   "Every DID MUST resolve to exactly one DIDDoc, and a DIDDoc MUST be bound to exactly one DID.",
}

# ── group 2: lowercase keywords ────────────────────────────────────────────
KEYWORDS = [
 ("All participants in an ADI-Network must generate a PK Pair",
  "All participants in an ADI-Network MUST generate a PK Pair"),
 ("The agent must securely store the private key in a hardened data vault.",
  "The agent MUST store the private key in a hardware security module meeting the requirements of clause 7.2.4.4."),
 ("Logic to process rules should be automated",
  "Logic to process rules SHOULD be automated"),
 ("ADI-Network User VCs must contain minimum information as required by ADI-Network governance policies",
  "ADI-Network User VCs MUST contain the minimum information required by ADI-Network governance policies"),
 ("Implementations should provide admin",
  "Implementations SHOULD provide admin"),
 ("An AGD must be created, which contains the root signing",
  "An AGD MUST be created, which contains the root signing"),
 ("a DID for the AGD is created and the DIDDoc must be the public key of the AGD private key",
  "a DID for the AGD is created and its DIDDoc MUST contain the public key corresponding to the AGD root signing key"),
 ("The Interchange should have an enrollment form the issuer can fill out and submit.",
  "The Interchange SHOULD provide an enrollment form the issuer can fill out and submit."),
 ("When requesting a VC, the service provider must specify one or more schemas that are acceptable.",
  "When requesting a VC, the service provider MUST specify one or more schemas that are acceptable."),
]

# ── group 3: narrative -> normative, unambiguous cases only ───────────────
NARRATIVE = [
 ("The Interchange will vet the Issuer information and execute a contract to join ADI.",
  "The Interchange MUST vet the Issuer information and execute a contract to join ADI before enrolling the Issuer."),
 ("The Interchange will perform due diligence, information validation and contract execution per ADI-Network governance rules.",
  "The Interchange MUST perform due diligence, information validation and contract execution per ADI-Network governance rules before enrolling the Service Provider."),
 ("The Interchange will also create an Agent for the Service Provider.",
  "The Interchange MUST create an Agent for the Service Provider."),
 ("The SP Agent will list the Service Provider in the AGD Service Provider Directory.",
  "The Interchange MUST list the Service Provider in the AGD Service Provider Directory; only the enrolling Interchange writes a Member's directory entry."),
 ("The Interchange will vet the service provider information and execute a contract to join ADI.",
  "The Interchange MUST vet the service provider information and execute a contract to join ADI before enrolling the Service Provider."),
 ("In this case the Interchange will perform vetting and issuing procedures to meet Network governance requirements or use a partnered network Issuer to perform vetting procedures.",
  "In this case the Interchange MUST perform vetting to meet Network governance requirements, either itself or through a partnered network Issuer."),
 ("The interchange will vet the user identity and issue an ADI-Network User VC to the user.",
  "The interchange MUST vet the user identity before issuing an ADI-Network User VC to the user."),
 ("If required, the INTERCHANGE will validate the identity with a selected Credential Issuer.",
  "If required, the INTERCHANGE MUST validate the identity with a selected Credential Issuer before proceeding."),
 ("The user agent  sends the signed issuance_token back to the issuer agent, who will then sign,  Issue and store the VC in a secure VC Vault.",
  "The user agent sends the signed issuance_token back to the issuer agent. The issuer agent MUST verify the token before signing, issuing and storing the VC in a secure VC Vault."),
 ("The USER_AGENT will request consent and authorization from the User.",
  "The USER_AGENT MUST obtain consent and authorization from the User before proceeding."),
 ("Using the user DID from the issue_vc token for the VC subject, a VC is generated and signed with DID private key.",
  "The issuer agent MUST verify that the issue_vc token was signed by the key of the subject bound to the offer when it was created (clause 12.4), and MUST use that subject, not a value taken from the token, as the VC subject. A VC is then generated and signed with the Issuer's DID private key."),
 ("The USER_AGENT will ask the user to select one or more VCs from their wallet (if there is more than one) to use for this request.",
  "The USER_AGENT MUST present the acceptable VCs from the User's wallet and ask the User to select one or more to use for this request."),
 ("The USER_AGENT will then ask the user for consent to present this VC to the service provider, using Strong Auth.  The USER_AGENT will then take the VC to create and sign a VP with the users\u2019 private key to demonstrate user consent.",
  "The USER_AGENT MUST obtain the User's consent to present the selected VC to the service provider, using strong authentication, and MUST then create and sign a VP with the User's private key to demonstrate that consent."),
 ("The Agent will return the  DID_DOC",
  "The Agent MUST return the DID_DOC"),
]


def apply(text, pairs, label, done, skipped):
    for a, b in pairs:
        if a in text:
            text = text.replace(a, b, 1); done.append("%s: %s" % (label, b[:70]))
        elif b in text:
            skipped.append("%s already: %s" % (label, b[:50]))
        else:
            skipped.append("%s NOT FOUND: %s" % (label, a[:60]))
    return text


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()
    done, skipped = [], []

    text = apply(text, NOTES, "note", done, skipped)

    for heading, para in RESTATE.items():
        if para[:60] in text:
            skipped.append("restate already present under %s" % heading[:24]); continue
        m = re.search(r"^%s[^\n]*\n\n(?:<a[^\n]*\n)?([^\n]+)\n" % re.escape(heading), text, re.M)
        if not m:
            skipped.append("heading not found: %s" % heading); continue
        text = text[:m.end()] + "\n" + para + "\n" + text[m.end():]
        done.append("restate under %s" % heading[:30])

    text = apply(text, KEYWORDS, "keyword", done, skipped)
    text = apply(text, NARRATIVE, "narrative", done, skipped)

    for l in done:    print("  updated : %s" % l)
    for l in skipped: print("  skipped : %s" % l)
    print("\n  %d edits. Role-VC issuance sentences deliberately left as narrative (D13)." % len(done))

    if dry: print("\n  --dry-run: nothing written"); return
    if not done: print("\n  nothing to change"); return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written -- now run: make notes")


if __name__ == "__main__":
    main()
