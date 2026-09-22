#!/usr/bin/env python3
"""
C-304: add a Security Considerations clause.

    python3 defects/apply_security.py --dry-run
    python3 defects/apply_security.py

Inserted as a new top-level clause immediately before the Editor's Notes, which
renumbers only the Editor's Notes (the generator now derives its own number).
Also adds the new clause to the normative list in clause 1.1.1, because several
of its requirements are stated nowhere else.

Written against the current draft. Where the draft has an open decision that
changes the analysis, the text says so rather than pretending otherwise.
"""

import sys, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

CLAUSE = '''<a id="security-considerations"></a>
# {N}. Security Considerations

This clause is normative. It records the threats the architecture is designed to resist, the parties it trusts and to what extent, and the requirements that follow. Where a requirement is stated in an earlier clause it is referenced, not repeated; where a requirement appears only here, it is binding on the conformance targets named.

<a id="security-trust-model"></a>
## {N}.1 Trust model

The ADI Network places trust in two parties and withholds it from the rest.

The **ADI Global Domain** is trusted as the root of the network. Its signing key is the trust anchor from which every other authority derives. Compromise of the AGD key compromises the network; there is no higher authority to recover from.

An **Interchange** is trusted to vet the entities it enrols, to hold Users' vault signing keys under the controls of clause 7.2.4.4, and to keep the audit record of clause {N}.9. An Interchange sees every transaction of every User it serves. This is inherent to the accountability property the architecture provides and is not a defect; it is, however, a concentration of trust that the controls in this clause exist to bound.

**Credential Issuers** are trusted only for the credential types they are entitled to issue, as recorded by the enrolling Interchange. **Service Providers** are not trusted: the architecture assumes a Service Provider may attempt to correlate presentations, replay them, or misrepresent the assurance it requires. **Users** are authenticated but not trusted with the vault signing key; the Digital Address Application is assumed to be under the User's control but is not assumed to be free of malware.

<a id="security-trust-anchor"></a>
## {N}.2 Trust anchor and root key

The AGD public key MUST be distributed to Interchanges and Service Providers out of band and MUST NOT be obtained solely from the network it anchors. A verifier that accepts an AGD key presented in-band by the party it is verifying has no root.

AGD key rotation MUST be performed by publishing the successor key signed by both the retiring key and the successor, for an overlap period of not less than 90 days during which verifiers MUST accept either. A verifier MUST reject any chain whose root key is not the configured trust anchor or its published successor.

There is no mechanism to recover from compromise of the AGD key other than re-establishing the network under a new anchor. Operators of an AGD SHOULD hold the key in a hardware security module validated to FIPS 140-3 Level 3 and SHOULD require multi-party authorisation for its use.

<a id="security-interchange"></a>
## {N}.3 The Interchange as a privileged party

Because an Interchange holds the User's vault signing key, a signature produced with that key does not, on its own, prove that the User authorised the signed content. The controls of clause 7.2.4.4 — a WebAuthn assertion bound to the hash of the exact payload, verified before the hardware security module will sign, and recorded in a hash-chained log — are what make such a signature attributable to the User rather than to the Interchange. An Interchange that does not implement those controls in full MUST NOT represent its Users' signatures as User-authorised, and a relying party MUST NOT treat them as such.

Compromise of an Interchange compromises every User, Issuer and Service Provider it enrolled, and every credential issued by those Issuers. The AGD MUST be able to revoke an Interchange's authority, and verifiers MUST check that revocation as part of the chain verification of clause 10.3.

Non-repudiation in this architecture is therefore a property of the Interchange's controls and records, not of the signature alone. Relying parties whose use case requires non-repudiation against the User without reliance on the Interchange are not served by the vault-assisted signing model, as clause 7.2.4.2 states.

<a id="security-replay"></a>
## {N}.4 Replay and substitution

A Verifiable Presentation MUST carry the `nonce` and `aud` values from the request that elicited it, and a Service Provider MUST reject a presentation whose values differ from those it issued or whose `exp` has passed. Without this, a presentation captured from one transaction can be replayed to the same or a different Service Provider.

A credential offer MUST bind the intended subject at the time the offer is created, and the Issuer MUST verify that the party redeeming the offer controls that subject's key before issuing. An offer whose subject is taken from the redeeming party allows anyone who intercepts the offer — including by reading a QR code — to obtain a credential in their own name. Offers MUST be single-use and MUST expire.

Correlation of a presentation request with the User's session across a redirect MUST use a `state` value that the Service Provider generates, stores, and compares on return.

<a id="security-crypto"></a>
## {N}.5 Cryptographic agility and algorithm confusion

Verifiers MUST select the signature algorithm from the token's `alg` header and MUST confirm that it is consistent with the type of the key retrieved from the signer's DIDDoc. A verifier MUST reject `alg: none` and MUST reject any attempt to verify with a symmetric algorithm a token whose signer is identified by an asymmetric key. These requirements are stated in clause 6.2 and are restated here because their omission is a well-known class of vulnerability in JWS implementations.

The set of signature algorithms permitted by this document is to be stated by the working group; until it is, implementers SHOULD support ES256 and SHOULD NOT produce new signatures with RSA PKCS#1 v1.5 (`RS256`).

<a id="security-enrolment"></a>
## {N}.6 Enrolment integrity

The AGD MUST enforce that Interchange names are unique within the network, as clause 7.4.1 requires. The uniqueness of every Digital Address in the network depends on this single check.

Only the enrolling Interchange MAY write a Member's entry in the network directory, and directory writes MUST be signed with the Interchange's DID key. A directory that accepts unauthenticated writes permits an attacker to register a Digital Address they do not control, or to redirect resolution of one they do not own.

The Hash of Subject ID Attributes (HIDA) is computed over a small, structured attribute space. An unkeyed digest over such a space is recoverable by exhaustive search. A HIDA MUST be computed under a key held by the enrolling Interchange, MUST NOT be disclosed outside that Interchange, and MUST NOT be compared across Interchanges, as clause 7.4.2 requires.

<a id="security-identifiers"></a>
## {N}.7 Identifier integrity

Digital Addresses are human-readable and therefore subject to confusable-character attacks. This version restricts the local part to ASCII (clause 7.4.1); implementations MUST NOT accept a Digital Address containing characters outside that set, and user interfaces SHOULD display Digital Addresses in a manner that makes substitution of similar-looking characters apparent.

NOTE — The syntax of the `did:adi` identifier is under revision. In the form used by the examples in Appendix B, the segments following the first solidus form a path rather than part of the identifier, so two entities differing only in those segments resolve to the same DID. Verifiers MUST NOT rely on path segments to distinguish entities until the syntax is settled.

<a id="security-transport"></a>
## {N}.8 Transport security

Connections between Digital Address Services MUST use mutual TLS. The client certificate MUST carry the connecting party's DID as a `uniformResourceIdentifier` subject alternative name, and the receiving party MUST confirm that the certificate's public key appears in the DIDDoc that DID resolves to. This binds the transport identity to the network identity; without it the two are independent trust hierarchies and a certificate issued to one party can front for another.

Network-layer controls, including IP address allowlisting, MUST NOT be used as, or counted towards, a User authentication factor (clause 7.2.4.3).

<a id="security-audit"></a>
## {N}.9 Audit record integrity

The accountability property of this architecture rests on the Interchange's record of what was signed, when, and on whose authority. That record MUST be append-only and MUST be hash-chained so that alteration or deletion of an entry is detectable. The head of the chain MUST be published to the AGD at least daily, so that an Interchange cannot rewrite its own history without the AGD's copy of the head diverging. Access to the record MUST be limited to what applicable law requires, as clause 6 provides.

<a id="security-session"></a>
## {N}.10 Session management

Assertion of an authentication assurance level is valid only for the reauthentication window of clause 7.2.4.3. An Interchange MUST NOT authorise a signing operation on the basis of an authentication event older than that window, and MUST require reauthentication after the period of inactivity stated there.

<a id="security-availability"></a>
## {N}.11 Availability dependencies

Verification of a presentation requires resolution of the signer's public key and authority, which in turn requires the Digital Address Service of the issuing Interchange to be reachable. A verifier with no network path to that Interchange cannot verify. Verifiers MAY cache resolved DIDDocs and authority records for the lifetime their signer declares, and SHOULD do so; they MUST NOT extend a cached record beyond its declared lifetime.

An attacker able to deny access to an Interchange's Digital Address Service can prevent verification of every credential issued under that Interchange. Interchange operators SHOULD provision the service for availability accordingly.

'''

NORMATIVE_OLD = "Clauses 6, 7, 8, 9 and 10 and Appendix B are normative."
NORMATIVE_NEW = "Clauses 6, 7, 8, 9, 10 and {N} and Appendix B are normative."


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()

    if '<a id="security-considerations"></a>' in text:
        print("  Security Considerations already present"); return

    # the new clause takes the Editor's Notes' number; the notes generator renumbers itself
    m = re.search(r"^# (\d+)\. Editor's Notes", text, re.M)
    if not m:
        print("  Editor's Notes clause not found; run make notes first"); sys.exit(1)
    n = int(m.group(1))
    clause = CLAUSE.replace("{N}", str(n))

    start = text.find("<!-- EDITORS-NOTES-START")
    text = text[:start] + clause + "\n" + text[start:]
    print("  inserted clause %d Security Considerations before the Editor's Notes" % n)

    if NORMATIVE_OLD in text:
        text = text.replace(NORMATIVE_OLD, NORMATIVE_NEW.replace("{N}", str(n)), 1)
        print("  clause 1.1.1 updated to list clause %d as normative" % n)
    else:
        print("  NOTE: clause 1.1.1 sentence not found -- add clause %d to the normative list by hand" % n)

    if dry:
        print("\n  --dry-run: nothing written"); return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written -- now run: make notes && make anchors")


if __name__ == "__main__":
    main()
