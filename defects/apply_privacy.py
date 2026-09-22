#!/usr/bin/env python3
"""
C-305: add a Privacy Considerations clause.

    python3 defects/apply_privacy.py --dry-run
    python3 defects/apply_privacy.py

Inserted as a new top-level clause immediately before the Editor's Notes, which
renumbers itself. Added to the normative list in clause 1.1.1.

The clause states the privacy properties the architecture actually provides,
including the ones it deliberately does not. The draft elsewhere says the
ecosystem "must facilitate and preserve personal privacy" and describes
"privacy preserving pairwise DIDs"; this clause is where those claims are made
precise, and in two places narrowed.
"""

import sys, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

CLAUSE = '''<a id="privacy-considerations"></a>
# {N}. Privacy Considerations

This clause is normative. It states the privacy properties the ADI Network provides to a User, the parties from whom the User's activity is and is not protected, and the requirements on participants that follow. Claims about privacy elsewhere in this document are to be read as qualified by this clause.

<a id="privacy-scope"></a>
## {N}.1 What the architecture protects, and from whom

The ADI Network is designed so that a Service Provider learns only what the User consents to disclose, and so that a Service Provider cannot, from the identifiers it receives, link one User's presentations to another Service Provider's. It is not designed to conceal the User's activity from the Interchange that serves them. The Interchange sees every presentation the User makes, knows the identity behind every Digital Address it issued, and holds the record that links the two. This is the accountability property from which the architecture takes its name, and it is stated here so that no reader infers a stronger property than the one provided.

<a id="privacy-linkability"></a>
## {N}.2 Subject identifiers and linkability across Service Providers

A credential whose `credentialSubject.id` is the User's primary DID carries a stable, globally unique identifier into every presentation of that credential. Two Service Providers receiving such presentations can trivially establish that they concern the same User, and one Service Provider can link a User's repeat visits. The transaction identifier mechanism of clause 7.4.4 addresses the identifier on the *presentation*; it does not address the identifier inside the *credential*. A transaction DID wrapping a credential that names the primary DID provides no unlinkability, and clause 7.4.4.3 prohibits representing it as such.

Unlinkability across Service Providers therefore requires that the credential itself not disclose a stable subject identifier. This version of this document does not fully specify a mechanism for that; the credential format decision recorded in the Editor's Notes determines whether it can be provided. Until it is, an Interchange MUST NOT describe presentations to Users or Service Providers as unlinkable.

<a id="privacy-interchange"></a>
## {N}.3 Visibility to the Interchange

An Interchange necessarily observes, for every User it serves: each presentation request received, the Service Provider that made it, the credential selected, the time, and the assurance asserted. It holds the User's vault signing key and authorises its use. It retains the enrolment record, including the PII from which the HIDA was computed.

An Interchange MUST limit its use of this information to the operation of the network, the enforcement of governance policy, and disclosure required by law under clause 6. It MUST NOT use transaction records to profile Users, and MUST NOT disclose them to Service Providers, Credential Issuers or other Interchanges except as this document or applicable law requires. The record retention and access requirements of clause {S}.9 apply.

<a id="privacy-cross-interchange"></a>
## {N}.4 Identity across Interchanges

A natural person may hold Digital Addresses issued by more than one Interchange. The uniqueness check of clause 7.4.1 is performed within a single Interchange, and Hashes of Subject ID Attributes are not compared across Interchanges (clause 7.4.2). The network therefore does not determine, and cannot determine, that two Digital Addresses issued by different Interchanges refer to the same person.

This is a privacy property: a person's activity at one Interchange is not linkable to their activity at another through any network mechanism. It is also a limitation: the network provides no global assurance of one-person-one-identity, and a Service Provider that assumes a Digital Address corresponds to a unique natural person network-wide is mistaken. Service Providers whose use case requires that assurance MUST obtain it by other means.

<a id="privacy-disclosure"></a>
## {N}.5 Selective disclosure and data minimisation

A Service Provider MUST request only the credential types and claims its purpose requires, and MUST state that purpose in a manner the User can see before consenting. A User Agent MUST present the User with the specific claims that will be disclosed, not merely the credential, and MUST NOT disclose claims the User has not approved.

Where the credential format permits selective disclosure, the User Agent MUST disclose only the claims the User selected. Where it does not, the whole credential is disclosed and the User Agent MUST make this apparent to the User before consent is given.

<a id="privacy-pii"></a>
## {N}.6 Personal information in enrolment records and the directory

The information an Interchange collects at enrolment is held for the purposes of vetting, uniqueness checking and accountability. It MUST NOT be published. The network directory MUST contain, for each entity, no more than its Digital Address, its DID, its role, and its service endpoints. An entity's legal name and contact details MAY be published for Providers, Credential Issuers and Service Providers, which are organisations; they MUST NOT be published for Users.

Where this document provides for personal information to be carried inside a credential or authority record, it MUST be limited to what the recipient requires for the purpose the record serves, and the record MUST state the party for whose access it is protected.

<a id="privacy-hida"></a>
## {N}.7 Hash of Subject ID Attributes

The HIDA is a keyed digest of personal attributes, computed and held by the enrolling Interchange for the sole purpose of detecting duplicate enrolment (clause 7.4.2). It is derived from PII and MUST be treated as PII. It MUST NOT leave the Interchange, MUST NOT be included in any credential, presentation or directory entry, and MUST NOT be used for any purpose other than the uniqueness check at enrolment. The Interchange key under which it is computed MUST be managed so that the HIDA cannot be recomputed by any other party.

<a id="privacy-biometrics"></a>
## {N}.8 Biometric information

Where the User's authenticator uses biometric verification, the biometric sample, any template derived from it, and any comparison score remain within the authenticator (clause 7.2.4.5). The only artefact that reaches any ADI Network participant is the `UV` flag in a WebAuthn assertion, indicating that verification succeeded. No participant MUST collect, store or process biometric information, and no ADI Network protocol message carries it.

<a id="privacy-audit"></a>
## {N}.9 Audit records and lawful access

The audit record of clause {S}.9 links transaction identifiers, Digital Addresses and Service Providers. It exists so that, under appropriate legal process, the identity behind a transaction can be established. Access to it MUST be limited to that purpose. An Interchange MUST maintain a record of each disclosure made from the audit record, including the legal basis, and SHOULD make aggregate statistics of such disclosures available to the governance body of the network.

<a id="privacy-retention"></a>
## {N}.10 Retention and erasure

Signed artefacts — credentials, presentations, authority records — cannot be altered after signing without invalidating the signature, and copies may be held by parties outside the Interchange's control. A User's right to erasure under applicable law is therefore satisfied by revocation and by deletion of the Interchange's own copies, not by alteration of issued artefacts. An Interchange MUST document its retention periods for enrolment records, audit records and vault keys, and MUST delete or irreversibly anonymise each category when its retention period ends or when a User withdraws from the network, whichever is earlier, save where law requires longer retention.

'''

NORMATIVE_OLD_RE = r"Clauses 6, 7, 8, 9, 10 and (\d+) and Appendix B are normative\."


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()

    if '<a id="privacy-considerations"></a>' in text:
        print("  Privacy Considerations already present"); return

    m = re.search(r"^# (\d+)\. Editor's Notes", text, re.M)
    if not m:
        print("  Editor's Notes clause not found; run make notes first"); sys.exit(1)
    n = int(m.group(1))
    sm = re.search(r"^# (\d+)\. Security Considerations", text, re.M)
    s_num = sm.group(1) if sm else "12"
    clause = CLAUSE.replace("{N}", str(n)).replace("{S}", s_num)

    start = text.find("<!-- EDITORS-NOTES-START")
    text = text[:start] + clause + "\n" + text[start:]
    print("  inserted clause %d Privacy Considerations before the Editor's Notes" % n)

    mm = re.search(NORMATIVE_OLD_RE, text)
    if mm:
        text = text.replace(mm.group(0), "Clauses 6, 7, 8, 9, 10, %s and %d and Appendix B are normative." % (mm.group(1), n), 1)
        print("  clause 1.1.1 updated to list clause %d as normative" % n)
    else:
        print("  NOTE: clause 1.1.1 normative sentence not found -- add clause %d by hand" % n)

    if dry:
        print("\n  --dry-run: nothing written"); return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written -- now run: make notes && make anchors")


if __name__ == "__main__":
    main()
