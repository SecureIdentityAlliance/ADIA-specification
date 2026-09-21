#!/usr/bin/env python3
"""
Adds the missing Verifiable Presentation object (A-127) and applies the
transaction-DID data model additions (D-406, one-time variant per RK).

    python3 defects/apply_vp.py --dry-run
    python3 defects/apply_vp.py

What it does:
  B.2.5   vc_request  -- add nonce, aud, exp, state, subject_scope_required
  B.2.12  vp          -- new section, the presentation object
  §10.1   prose       -- one sentence pointing at B.2.12

The credential inside a presentation is carried in `verifiableCredential`.
Its serialization follows the credential format decision (D6); the envelope
fields below do not depend on it.

Safe to re-run.
"""

import sys, os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

VC_REQUEST = '''{
  "sp_id": "sp1@interchange1",
  "aud": "did:adi:r1:ix1:a523335a-df3b-41cc-b371-88034beb1e5c",
  "nonce": "n-0S6_WzA2Mj",
  "state": "af0ifjsldkj",
  "exp": 1758240600,
  "min_ial": 2,
  "min_aal": 2,
  "min_fal": 1,
  "subject_scope_required": "any",
  "schemas_accepted": [
    "US_Passport",
    "US_Driver_License",
    "Univ_ID"
  ]
}'''

VP_SECTION = '''### B.2.12 vp

A Verifiable Presentation returned by a User Agent in response to a
`vc_request`. The envelope fields are independent of the credential format;
`verifiableCredential` carries the credential as serialized under the format
specified in §6.2.

`adia_subject_scope` is `primary` when the presentation is bound to the User's
primary DID, and `transaction` when it is bound to a single-use transaction DID
generated under §7.4.4. A Service Provider MUST NOT store a transaction-scoped
identifier as a persistent account key.

```json
{
  "iss": "did:adi:r1:ix1:txn:3b9c1e2a-7d41-4f8e-9a02-5c6d18b4e730",
  "aud": "did:adi:r1:ix1:a523335a-df3b-41cc-b371-88034beb1e5c",
  "nonce": "n-0S6_WzA2Mj",
  "state": "af0ifjsldkj",
  "iat": 1758240120,
  "exp": 1758240420,
  "adia_subject_scope": "transaction",
  "ial": 2,
  "aal": 2,
  "fal": 2,
  "verifiableCredential": [
    "eyJhbGciOiJFUzI1NiIsInR5cCI6InZjK3NkLWp3dCIsImtpZCI6ImtleS0xIn0..."
  ],
  "disclosures": [
    "WyJfMjZiYzRsVC1hYzZxMktJNmNCVyIsICJmYW1pbHlfbmFtZSIsICJEb2UiXQ"
  ],
  "proof": {
    "type": "JsonWebSignature2020",
    "created": "2026-09-19T00:02:00Z",
    "verificationMethod": "did:adi:r1:ix1:txn:3b9c1e2a-7d41-4f8e-9a02-5c6d18b4e730#key-1",
    "jws": "eyJhbGciOiJFUzI1NiJ9..."
  }
}
```

'''

PROSE = ("A Verifiable Presentation is defined in [B.2.12 vp](#vp). It is bound to the "
         "requesting Service Provider by `aud` and to the request by `nonce`, and carries the "
         "identity, authentication and federation assurance levels achieved.\n\n")


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()
    did = []

    # 1. vc_request
    m = re.search(r"(### B\.2\.5 vc_request\n+```json\n)(.*?)(\n```)", text, re.S)
    if not m:
        print("  WARNING: B.2.5 not found"); 
    elif "subject_scope_required" in m.group(2):
        print("  B.2.5 already updated, skipped")
    else:
        text = text[:m.start(2)] + VC_REQUEST + text[m.end(2):]
        did.append("B.2.5")

    # 2. B.2.12, inserted after B.2.11
    if "### B.2.12 vp" in text:
        print("  B.2.12 already present, skipped")
    else:
        m = re.search(r"^## B\.3 ", text, re.M)
        if not m:
            print("  WARNING: B.3 heading not found; B.2.12 not inserted")
        else:
            text = text[:m.start()] + VP_SECTION + text[m.start():]
            did.append("B.2.12")

    # 3. one sentence in the presentation section
    if "B.2.12 vp" in text and PROSE.strip()[:40] not in text:
        m = re.search(r"^## [\d.]+ Service Provider\s*\n+", text, re.M)
        if m:
            text = text[:m.end()] + PROSE + text[m.end():]
            did.append("§10.1 prose")

    print("  updated: %s" % (", ".join(did) or "nothing"))

    bad = []
    for b in re.findall(r"```json\n(.*?)\n```", text, re.S):
        try: json.loads(b)
        except Exception as e: bad.append(str(e)[:50])
    if bad:
        print("  ABORTED -- JSON would not parse: %s" % bad[0]); sys.exit(1)
    print("  all JSON examples parse")

    if dry:
        print("\n  --dry-run: nothing written"); return
    if not did:
        print("\n  nothing to change"); return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written -- now run: make anchors && make relocate")


if __name__ == "__main__":
    main()
