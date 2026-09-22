#!/usr/bin/env python3
"""
B-201: replace the signature verification description in §6.2.

    python3 defects/apply_b201.py --dry-run
    python3 defects/apply_b201.py

The existing paragraph contains three errors:

  1. "combining the metadata and claims sections to create a SHA256 hash"
     The JWS signing input is BASE64URL(protected header) || "." ||
     BASE64URL(payload) -- a concatenation of two base64url strings, not a
     combination of decoded sections. The digest is selected by the "alg"
     header parameter and is not fixed at SHA-256.

  2. "the signature is valid if the public key encryption of the hash matches
     the signature of the proof"
     This describes textbook RSA verification in reverse, and does not apply
     at all to ECDSA, which is the algorithm this specification's own issuer
     metadata advertises (ES256). ECDSA verification is not an encrypt-and-
     compare operation.

  3. "the specified encryption algorithm"
     "alg" identifies a signature algorithm, not an encryption algorithm, and
     it appears in the JOSE header rather than in credential metadata.

The replacement states the procedure by normative reference to RFC 7515 rather
than describing the primitive, and adds the header requirements that hold
regardless of which algorithms the working group selects under A-126.

Safe to re-run.
"""

import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

OLD = ("The verifier can check the signature by combining the metadata and claims sections to create a "
       "SHA256 hash. Using the public key from the issuers ADI DIDDoc, the signature is valid if the "
       "public key encryption of the hash matches the signature of the proof, using the specified "
       "encryption algorithm in the metadata.")

NEW = """Signatures on ADI Verifiable Credentials, presentations and protocol requests are JSON Web Signatures [RFC7515].

A verifier MUST validate a signature using the procedure in [RFC7515] §5.2. In outline: reconstruct the signing input as `BASE64URL(UTF8(protected header))`, a full stop, and `BASE64URL(payload)`; select the signature algorithm named by the `alg` header parameter; locate the verification key identified by the `kid` header parameter in the signer's DIDDoc; and verify the signature over the signing input according to that algorithm.

The following apply to every signature verification:

- A verifier MUST reject a token whose `alg` value is `none`, and MUST reject any `alg` value not permitted by this specification.
- A verifier MUST select the verification algorithm from the `alg` header parameter, and MUST confirm that it matches the key type of the key retrieved. A verifier MUST NOT allow a token to select a symmetric algorithm where an asymmetric key is expected.
- A verifier MUST reject a token whose `kid` does not resolve to a verification method in the signer's current DIDDoc.
- Where a key appears both in a role credential and in a resolved DIDDoc, the DIDDoc is authoritative. A mismatch MUST be treated as a verification failure."""


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()

    if NEW.split("\n")[0] in text:
        print("  already applied")
        return
    if OLD not in text:
        print("  NOT FOUND -- the paragraph has been reworded.")
        print("  Locate it with: make explain ID=B-201")
        return

    text = text.replace(OLD, NEW, 1)
    print("  updated : §6.2 signature verification paragraph")
    print("  note    : the permitted `alg` values are still open (A-126 / decision D7)")

    if dry:
        print("\n  --dry-run: nothing written"); return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written")


if __name__ == "__main__":
    main()
