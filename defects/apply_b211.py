#!/usr/bin/env python3
"""
B-211: who creates and signs a DIDdoc, and what get_did_doc returns.

    python3 defects/apply_b211.py --dry-run
    python3 defects/apply_b211.py

RK, 23 Sep: the Interchange creates the DIDdoc and keeps the enrolled entity's
public key. So the DIDdoc's signer is the enrolling authority -- the
Interchange for Issuers, Service Providers and Users; the AGD for Interchanges
and for itself. This is the DID Core notion of `controller`.

Three edits:
  clause 3.20   the definition names the signer and stops calling it "the issuer"
  clause 10.2   the response to get_did_doc is defined and its signer stated
  B.3.5         new: the did_doc response object, served as a JWS by the DAS

Safe to re-run.
"""

import sys, os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

IX     = "did:adi:9uGPcUMRTgmL_JmAqQ5L5w"     # Interchange 1
TARGET = "did:adi:CfTO4LOoS_6h92nYNHZBWQ"     # the DID B.3.4 asks for

E320 = [
 ("> Document signed using the private key of the issuer.",
  "> Document, bound to a DID, that carries the DID's verification methods and metadata. It is created and signed by the authority that enrolled the DID's subject — the Interchange for Credential Issuers, Service Providers and Users; the ADI Global Domain for Interchanges and for itself — which is the DIDdoc's `controller`."),
 ("> Note 1 to entry: A DIDdoc contains the associated DID, the public key of the DID, the verification method(s) and optionally other metadata",
  "> Note 1 to entry: A DIDdoc contains the associated DID, its controller, the verification method(s) carrying the subject's public keys, service endpoints, and optionally other metadata. The controller holds a copy of every public key it publishes in a DIDdoc."),
 ("> Note 3 to entry: A DIDdoc may be packaged as a JWT VC.",
  "> Note 3 to entry: A DIDdoc is served by the controller's Digital Address Service as the payload of a JWS signed by the controller; see clause 10.2 and B.3.5."),
]

E102 = [
 ("The Agent MUST return the DID_DOC",
  "The Agent MUST return the DIDdoc as the payload of a JWS signed by the DIDdoc's controller ([B.3.5](#did-doc)). The Agent MUST verify that signature against the controller's own DIDdoc before returning the result, and the Service Provider MUST NOT use a key from a DIDdoc whose controller signature has not been verified."),
]

B35 = '''<a id="did-doc"></a>
### B.3.5 did_doc

Response to `get_did_doc` (B.3.4). The Digital Address Service of the DID's controller returns the DIDdoc as the payload of a JWS whose `kid` identifies the controller's signing key. Shown decoded.

```json
{
  "header": {
    "alg": "ES256",
    "typ": "did+jwt",
    "kid": "%(ix)s#key-1"
  },
  "payload": {
    "iss": "%(ix)s",
    "iat": 1758585600,
    "exp": 1758672000,
    "didDocument": {
      "@context": ["https://www.w3.org/ns/did/v1"],
      "id": "%(t)s",
      "controller": "%(ix)s",
      "verificationMethod": [
        {
          "id": "%(t)s#key-1",
          "type": "JsonWebKey2020",
          "controller": "%(t)s",
          "publicKeyJwk": {
            "kty": "EC",
            "crv": "P-256",
            "x": "issuer_x_placeholder_public_key_value_00000000",
            "y": "issuer_y_placeholder_public_key_value_00000000"
          }
        }
      ],
      "assertionMethod": ["%(t)s#key-1"],
      "authentication": ["%(t)s#key-1"],
      "service": [
        {
          "id": "%(t)s#agent",
          "type": "ADIAgent",
          "serviceEndpoint": "https://issuer1.ix1.adi.example/agent"
        }
      ]
    },
    "didDocumentMetadata": {
      "created": "2026-01-15T10:00:00Z",
      "updated": "2026-01-15T10:00:00Z",
      "deactivated": false
    }
  },
  "signature": "…"
}
```

`exp` bounds how long a resolver MAY cache the document (clause 7.4.3.3). `didDocumentMetadata.deactivated` is `true` for a DID whose authority has been withdrawn (clause 6.6); resolvers MUST honour it.

''' % {"ix": IX, "t": TARGET}


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()
    done, skipped = [], []

    for a, b in E320 + E102:
        if a in text: text = text.replace(a, b, 1); done.append(b[:70])
        elif b[:60] in text: skipped.append("already: " + b[:50])
        else: skipped.append("NOT FOUND: " + a[:50])

    if '<a id="did-doc"></a>' in text:
        skipped.append("B.3.5 already present")
    else:
        m = re.search(r"### B\.3\.4 get_did_doc.*?```json\n.*?\n```\n", text, re.S)
        if m:
            text = text[:m.end()] + "\n" + B35 + text[m.end():]
            done.append("B.3.5 did_doc response added")
        else:
            skipped.append("B.3.4 not found; B.3.5 not added")

    for l in done:    print("  updated : %s" % l)
    for l in skipped: print("  skipped : %s" % l)

    for blk in re.findall(r"```json\n(.*?)\n```", text, re.S):
        try: json.loads(blk)
        except Exception as e: print("  ABORTED: JSON no longer parses: %s" % str(e)[:60]); sys.exit(1)

    if dry: print("\n  --dry-run: nothing written"); return
    if not done: print("\n  nothing to change"); return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written -- now run: make anchors && make notes")


if __name__ == "__main__":
    main()
