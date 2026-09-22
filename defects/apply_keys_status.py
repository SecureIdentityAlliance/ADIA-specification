#!/usr/bin/env python3
"""
The parts of B-209, B-213 and B-216 that do not depend on the role-VC decision.

    python3 defects/apply_keys_status.py --dry-run
    python3 defects/apply_keys_status.py

B-216  vc_authorization_request is undefined. The prose in clause 10.1.3 uses
       that name for what the message line and Appendix B call vc_request.
       One-word fix.

B-213  No key identifiers and no rotation procedure. Adds clause 6.1.1 (key
       identifiers) and 6.1.2 (key rotation). Model-independent, because clause
       6.2 already makes the DIDDoc authoritative for keys under either model.
       Also corrects "type" -> "typ" and adds "kid" in the three JWT examples
       that are not role VCs (B.1.1, B.1.2, B.2.3). The role-VC examples are
       left alone because the DIDDoc proposal deletes them.

B-209  No credential status or revocation. Adds clause 6.2.1 (credential
       status), written so that either credential format (D6) can satisfy it,
       and adds to clause 6.6 the requirement that authority be revocable --
       without naming the mechanism, which is exactly what the role-VC decision
       determines.

Safe to re-run.
"""

import sys, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

# ---------------------------------------------------------------- B-216
B216 = [
 ("The SP_AGENT creates a vc_authorization_request and constructs a URI",
  "The SP_AGENT creates a vc_request ([B.2.5](#vcrequest)) and constructs a URI"),
]

# ---------------------------------------------------------------- B-213
KEYS_CLAUSE = '''
<a id="key-identifiers"></a>
### 6.1.1 Key identifiers

Every JSON Web Signature produced by an ADI Network participant MUST carry a `kid` header parameter identifying the signing key. The value MUST be a DID URL of the form `<DID>#<fragment>`, where `<DID>` is the signer's DID and `<fragment>` identifies a verification method in the DIDDoc that DID resolves to. A verifier MUST reject a signature whose `kid` does not resolve to a verification method in the signer's current DIDDoc, as clause 6.2 requires.

The `typ` header parameter, where present, identifies the token type per [RFC7515]. Implementations MUST NOT use a header parameter named `type` for this purpose.

<a id="key-rotation"></a>
### 6.1.2 Key rotation

A participant rotates a signing key by having its DIDDoc republished with the new key added to `verificationMethod` and the retired key retained, marked with a `revoked` property carrying the timestamp from which it is no longer to be used for new signatures. The retired key MUST remain in the DIDDoc for as long as any signature made with it may need to be verified, and in no case less than the longest validity period of any credential signed with it.

A verifier presented with a signature whose `kid` identifies a retired key MUST verify it only if the signature was made before the key's `revoked` timestamp, as established by the signed object's own `iat` or equivalent. A verifier MUST reject a signature made with a retired key after its `revoked` timestamp.

Rotation of the ADI Global Domain root key follows clause 12.2. Rotation of an Interchange's key MUST be notified to the ADI Global Domain, which MUST update the network directory before the retired key's `revoked` timestamp takes effect.
'''

HEADER_FIX = [
 ("B.1.1", '"alg": "RS256",\n    "type": "JWT"',
           '"alg": "RS256",\n    "typ": "JWT",\n    "kid": "did:adi:global:agd:8c019421-2920-410c-acfe-77d5c87b187c#key-1"'),
 ("B.1.2", '"alg": "RS256",\n    "type": "JWT"',
           '"alg": "RS256",\n    "typ": "JWT",\n    "kid": "did:adi:r1:ix1:f6e18f71-4311-4e09-8bfc-9980a90e4be7#key-1"'),
 ("B.2.3", '"alg": "RS256",\n    "type": "JWT"',
           '"alg": "RS256",\n    "typ": "JWT",\n    "kid": "did:adi:r1:ix1:45bde61c-7da0-4f85-aed4-39d2d7508e99#key-1"'),
]

# ---------------------------------------------------------------- B-209
STATUS_CLAUSE = '''
<a id="credential-status"></a>
### 6.2.1 Credential status

Every Verifiable Credential issued in the ADI Network MUST carry a status reference from which a verifier can determine whether the credential has been revoked or suspended since issuance. The reference identifies a status resource published by the Issuer and the position of this credential within it.

An Issuer MUST publish a status resource for every credential type it issues, MUST sign it, and MUST refresh it so that its validity period never exceeds 24 hours. A verifier MUST retrieve the status resource, MUST verify its signature against the Issuer's DIDDoc, and MUST reject a credential whose status is revoked or suspended. A verifier MAY cache a status resource for its stated validity period and MUST NOT rely on it beyond that.

The form of the status reference and resource depends on the credential format:

- for credentials serialised as SD-JWT VC, the `status` claim referencing a Token Status List;
- for credentials serialised under the W3C Verifiable Credentials Data Model, the `credentialStatus` property referencing a Bitstring Status List.

Revocation of a credential does not alter the credential; copies already held remain syntactically valid and are distinguished from live credentials only by the status check. This is why the check is mandatory.
'''

REVOCATION_6_6 = (
 "Each ADI-ROLE is issued and signed by an ADI-Authority.  Role VCs designate which role VCs the holder has authority to issue and sign.",
 "Each ADI-ROLE is issued and signed by an ADI-Authority.  Role VCs designate which role VCs the holder has authority to issue and sign.\n\n"
 "An authority that granted an entity its role MUST be able to withdraw it, and a verifier MUST determine, as part of chain verification, "
 "that no authority in the chain has been withdrawn. Withdrawal of an Interchange's authority invalidates every entity it enrolled. "
 "The mechanism by which withdrawal is recorded and discovered is specified with the authority record it applies to."
)


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()
    done, skipped = [], []

    # B-216
    for a, b in B216:
        if a in text: text = text.replace(a, b, 1); done.append("B-216 prose: vc_authorization_request -> vc_request")
        elif b in text: skipped.append("B-216 already applied")
        else: skipped.append("B-216 phrase not found")

    # B-213 clauses
    if '<a id="key-identifiers"></a>' in text:
        skipped.append("6.1.1 / 6.1.2 already present")
    else:
        m = re.search(r'\n(<a id="[^"]*"></a>\n)?## 6\.2 ', text)
        if m:
            text = text[:m.start()] + "\n" + KEYS_CLAUSE + text[m.start():]
            done.append("6.1.1 Key identifiers and 6.1.2 Key rotation inserted")
        else:
            skipped.append("6.2 heading not found; key clauses not inserted")

    # B-213 headers in surviving examples
    for name, old, new in HEADER_FIX:
        sec = re.search(r"### %s .*?```json\n(.*?)\n```" % re.escape(name), text, re.S)
        if not sec: skipped.append("%s not found" % name); continue
        body = sec.group(1)
        if '"typ": "JWT"' in body: skipped.append("%s header already fixed" % name); continue
        if old not in body: skipped.append("%s header shape differs; left alone" % name); continue
        text = text[:sec.start(1)] + body.replace(old, new, 1) + text[sec.end(1):]
        done.append("%s header: typ + kid" % name)

    # B-209 clause
    if '<a id="credential-status"></a>' in text:
        skipped.append("6.2.1 already present")
    else:
        m = re.search(r'\n(<a id="[^"]*"></a>\n)?## 6\.3 ', text)
        if m:
            text = text[:m.start()] + "\n" + STATUS_CLAUSE + text[m.start():]
            done.append("6.2.1 Credential status inserted")
        else:
            skipped.append("6.3 heading not found; status clause not inserted")

    # B-209 authority revocation requirement in 6.6
    a, b = REVOCATION_6_6
    if "MUST be able to withdraw it" in text: skipped.append("6.6 revocation sentence already present")
    elif a in text: text = text.replace(a, b, 1); done.append("6.6: authority withdrawal requirement (mechanism deferred)")
    else: skipped.append("6.6 anchor sentence not found")

    for l in done:    print("  updated : %s" % l)
    for l in skipped: print("  skipped : %s" % l)

    import json
    bad = [n for n, blk in zip(re.findall(r"^#{2,3} (B\.\d+\.\d+)", text, re.M),
                               re.findall(r"```json\n(.*?)\n```", text, re.S))
           if not _ok(json, blk)]
    if bad:
        print("\n  ABORTED -- JSON would not parse: %s" % ", ".join(bad)); sys.exit(1)

    if dry: print("\n  --dry-run: nothing written"); return
    if not done: print("\n  nothing to change"); return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written -- now run: make anchors && make notes")


def _ok(json, blk):
    try: json.loads(blk); return True
    except Exception: return False


if __name__ == "__main__":
    main()
