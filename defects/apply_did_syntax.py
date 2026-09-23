#!/usr/bin/env python3
"""
D-403: opaque DID syntax, decided 23 Sep 2026.

    python3 defects/apply_did_syntax.py --dry-run
    python3 defects/apply_did_syntax.py

The form:  did:adi:<id>   where <id> is base64url (RFC 4648 §5, no padding) of
at least 128 bits of entropy. No region, no Interchange, no readable label.
Resolution goes through the AGD network directory, which maps a DID to the
Interchange that serves its DIDdoc.

What this script does:
  1. Rewrites every did:adi string in the document to the new form, keeping
     each entity's identity stable (one UUID -> one opaque id, used everywhere
     that entity appears) and preserving #fragments.
  2. Rewrites clause 7.4.3 with the syntax, encoding and resolution rules.
  3. Corrects clause 7.4.4's stale cross-reference and its transaction-DID form.
  4. Replaces the path-segment NOTE in Security 12.7.

Figure 10 shows routing inside the DID and needs redrawing; that is filed,
not fixed here. Safe to re-run.
"""

import sys, os, re, uuid, base64

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")


def opaque(u):
    """base64url of the UUID's 16 bytes, no padding -> 22 chars"""
    return base64.urlsafe_b64encode(uuid.UUID(u).bytes).decode().rstrip("=")


# every entity that appears in the document, keyed by the UUID already used for it
ENTITIES = {
    "8c019421-2920-410c-acfe-77d5c87b187c": "AGD",
    "f6e18f71-4311-4e09-8bfc-9980a90e4be7": "Interchange 1",
    "3b576f82-3506-4663-8ca4-51d614aea318": "Issuer 1",
    "eedec811-0f26-4656-a6cd-59d5f0bf2c16": "Issuer (university)",
    "9d0e5f61-7c2a-4b83-a1f4-2e6b7c8d9e0f": "Service Provider 1",
    "a523335a-df3b-41cc-b371-88034beb1e5c": "Service Provider (verifier)",
    "45bde61c-7da0-4f85-aed4-39d2d7508e99": "User 2",
    "09f4cee0-b3a8-4bfe-a1f7-69d834764159": "resolved DID (B.3.4)",
    "3b9c1e2a-7d41-4f8e-9a02-5c6d18b4e730": "transaction DID",
    "71a39c8d-0500-45d0-88d0-9c08d3931cce": "AGD (old B.2.7 subject)",
}
# strings that are not UUIDs but name an entity above
ALIASES = {
    "user2":                          "45bde61c-7da0-4f85-aed4-39d2d7508e99",
    "ebfeb1f712ebc6f1c276e12ec21":    "45bde61c-7da0-4f85-aed4-39d2d7508e99",
    "issuser1":                       "eedec811-0f26-4656-a6cd-59d5f0bf2c16",
    "issuer_6":                       "eedec811-0f26-4656-a6cd-59d5f0bf2c16",
    "global":                         "8c019421-2920-410c-acfe-77d5c87b187c",
}

CLAUSE_743 = '''### 7.4.3 DID Addressing

Every DID MUST resolve to exactly one DIDdoc, and a DIDdoc MUST be bound to exactly one DID.

An ADI-Network DID identifies an entity. Its DIDdoc references the keys that entity uses to sign and to authenticate; keys MAY be rotated without changing the DID (clause 6.1.2).

**7.4.3.1 Syntax.** An ADI-Network DID conforms to [DID-CORE] and has the form

```
did:adi:<id>
```

where `<id>` is the base64url encoding, without padding ([RFC4648] §5), of an identifier carrying at least 128 bits of entropy. The identifier carries no region, Interchange, role or other structure; it is opaque. Implementations MUST NOT encode routing or organisational information in the identifier, and verifiers MUST NOT infer any such information from it.

NOTE — Standard Base64 ([RFC4648] §4) is not acceptable: its alphabet includes `/`, which begins a DID URL path, and `+` and `=`, which are not permitted in a method-specific identifier. Only the URL-safe alphabet, unpadded, produces a valid DID.

A conforming construction is the base64url encoding of the 16 octets of a version-4 UUID [RFC9562], which yields a 22-character identifier. Other constructions MAY be used provided the entropy requirement is met.

**7.4.3.2 Assignment.** An Interchange assigns DIDs to the entities it enrols and MUST ensure uniqueness among them. The ADI Global Domain assigns DIDs to Interchanges and its own. Because identifiers carry at least 128 bits of entropy and are generated independently, collision across Interchanges is not a practical concern and no coordination is required.

**7.4.3.3 Resolution.** Because the DID carries no routing information, a resolver locates the Interchange serving a DID through the network directory maintained by the ADI Global Domain, which maps every enrolled DID to its Interchange. The resolver then requests the DIDdoc from that Interchange's Digital Address Service (clause 10.2). Resolvers MAY cache directory entries and DIDdocs for the validity period their signer declares and MUST NOT rely on them beyond it. Availability of the directory and of the serving Interchange is therefore a dependency of every verification; see clause 12.11.

**7.4.3.4 Conformance to DID Core.** ADI-Network identifiers conform to the syntax of [DID-CORE]. ADI resolves a DID to a DIDdoc to obtain verification keys and, through the ADI-ROLE credential, authority. ADI does not use DID document service endpoints for agent messaging. The `did:adi` method is to be registered in the W3C DID Specification Registries.

![ADI-Network DID Addressing](figures/fig-10-adi-network-did-addressing.svg)

*Figure 10. ADI-Network DID Addressing*

'''

EDITS_744 = [
 ("Construct a transaction DID in the form specified in §9.5.3, whose method-specific identifier is a UUIDv4 and which is marked as transaction-scoped by the `txn` segment. For example: `did:adi:r1:ix1:txn:3b9c1e2a-...`.",
  "Construct a transaction DID in the form specified in clause 7.4.3, from a freshly generated identifier. The DID itself carries no marker of its scope; the DIDdoc published for it under item 4 records that it is transaction-scoped."),
]

EDIT_127 = (
 "NOTE — The syntax of the `did:adi` identifier is under revision. In the form used by the examples in Appendix B, the segments following the first solidus form a path rather than part of the identifier, so two entities differing only in those segments resolve to the same DID. Verifiers MUST NOT rely on path segments to distinguish entities until the syntax is settled.",
 "The `did:adi` identifier is opaque and base64url-encoded (clause 7.4.3.1). An implementation that emits standard Base64 produces identifiers containing `/`, which DID Core treats as the start of a path, so two distinct entities can resolve to one DID. Verifiers MUST reject a `did:adi` identifier containing any character outside the base64url alphabet.",
)


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()
    mapping = {u: opaque(u) for u in ENTITIES}
    done = []

    # 1. rewrite every DID
    unknown = set()
    def sub(m):
        body = m.group(1)
        frag = m.group(2) or ""
        first = re.split(r"[/:]", body)[0]           # UUID or alias is always the first segment
        # colon form may put the uuid last: did:adi:r1:ix1:<uuid>
        parts = re.split(r"[/:]", body)
        cand = None
        for p in parts:
            if p in mapping: cand = p; break
            if p in ALIASES: cand = ALIASES[p]; break
        if cand is None:
            unknown.add(body); return m.group(0)
        return "did:adi:%s%s" % (mapping[cand], frag)
    new, n = re.subn(r"did:adi:([A-Za-z0-9_./:{}-]*?[A-Za-z0-9_}])(#[A-Za-z0-9_-]+)?(?=[\"'\s)\],.]|$)", sub, text)
    text = new; done.append("DID strings rewritten: %d" % n)
    if unknown: print("  WARNING unmapped forms left alone: %s" % sorted(unknown))

    # 2. clause 7.4.3
    m = re.search(r"### 7\.4\.3 DID Addressing\n.*?(?=\n<a id=\"transaction-dids\"></a>|\n### 7\.4\.4 )", text, re.S)
    if m and "7.4.3.1 Syntax" not in text:
        text = text[:m.start()] + CLAUSE_743.rstrip("\n") + "\n" + text[m.end():]
        done.append("clause 7.4.3 rewritten")
    elif "7.4.3.1 Syntax" in text:
        done.append("clause 7.4.3 already rewritten")
    else:
        print("  WARNING 7.4.3 not found")

    # 3. clause 7.4.4
    for a, b in EDITS_744:
        if a in text: text = text.replace(a, b, 1); done.append("7.4.4 transaction DID form corrected")
        elif b in text: done.append("7.4.4 already corrected")
        else: print("  WARNING 7.4.4 sentence not found")

    # 4. security 12.7
    a, b = EDIT_127
    if a in text: text = text.replace(a, b, 1); done.append("12.7 NOTE replaced")
    elif b in text: done.append("12.7 already replaced")

    for d in done: print("  " + d)
    forms = sorted(set(re.findall(r"did:adi:[A-Za-z0-9_-]+", text)))
    bad = [f for f in forms if not re.fullmatch(r"did:adi:[A-Za-z0-9_-]{22}", f)]
    print("\n  distinct DIDs now: %d   non-conforming: %s" % (len(forms), bad or "none"))

    import json
    blocks = re.findall(r"```json\n(.*?)\n```", text, re.S)
    for i, blk in enumerate(blocks):
        try: json.loads(blk)
        except Exception as e: print("  ABORTED: JSON block %d no longer parses: %s" % (i, str(e)[:50])); sys.exit(1)
    print("  all %d JSON examples parse" % len(blocks))

    if dry: print("\n  --dry-run: nothing written"); return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written -- now run: make anchors && make notes")


if __name__ == "__main__":
    main()
