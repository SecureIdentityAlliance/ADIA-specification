#!/usr/bin/env python3
"""
A-124 and A-126: within-document corrections to the examples.

    python3 defects/apply_alg_vcdm.py --dry-run
    python3 defects/apply_alg_vcdm.py

A-124  B.2.4 is written to VCDM 1.1 while Appendix A cites VCDM 2.0 and clause
       6.2.1 requires a status reference. Bring it to 2.0: v2 context, `id`,
       validFrom/validUntil, credentialStatus, a populated proof. This is a
       within-format fix; D6 (JSON-LD vs SD-JWT VC) remains open.

A-126  Eight headers say RS256. The document already specifies ES256 in three
       places: clause 6.2's example, B.3.1 metadata, and Security 12.5. Align
       the headers, and replace the two RSA JWKs with EC P-256 so key type
       matches algorithm. D7 remains open on the full mandatory set.

Every block is re-parsed before writing. Safe to re-run.
"""

import sys, os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")


def blocks(text):
    names = [(m.group(1), m.end()) for m in re.finditer(r"^#{2,3} (B\.\d+\.\d+)", text, re.M)]
    for i, (name, pos) in enumerate(names):
        lim = names[i + 1][1] if i + 1 < len(names) else len(text)
        m = re.search(r"```json\n(.*?)\n```", text[pos:lim], re.S)
        if m: yield name, pos + m.start(1), pos + m.end(1)


def ec(tag):
    return {"kty": "EC", "crv": "P-256",
            "x": "%s_x_placeholder_public_key_value_00000000" % tag,
            "y": "%s_y_placeholder_public_key_value_00000000" % tag}


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()
    done = []

    # A-124
    for name, a, b in list(blocks(text)):
        if name != "B.2.4": continue
        d = json.loads(text[a:b])
        if "ns/credentials/v2" in text[a:b]:
            done.append("A-124 already applied"); break
        new = {
          "@context": ["https://www.w3.org/ns/credentials/v2"],
          "id": "https://university.example/credentials/3732",
          "type": d.get("type", ["VerifiableCredential", "UniversityDegreeCredential"]),
          "issuer": d["issuer"],
          "validFrom": "2026-01-01T19:23:24Z",
          "validUntil": "2027-01-01T19:23:24Z",
          "credentialSubject": d["credentialSubject"],
          "credentialStatus": {
            "id": "https://university.example/status/degrees#9021",
            "type": "BitstringStatusListEntry",
            "statusPurpose": "revocation",
            "statusListIndex": "9021",
            "statusListCredential": "https://university.example/status/degrees"},
          "proof": {
            "type": "DataIntegrityProof",
            "cryptosuite": "ecdsa-rdfc-2019",
            "created": "2026-01-01T19:23:24Z",
            "verificationMethod": d["issuer"] + "#key-1",
            "proofPurpose": "assertionMethod",
            "proofValue": "z58DAdFfa9SkqZMVPxAQp...placeholder"}}
        text = text[:a] + json.dumps(new, indent=2, ensure_ascii=False) + text[b:]
        done.append("A-124: B.2.4 -> VCDM 2.0 with credentialStatus and proof")
        break

    # A-126 headers
    n = text.count('"alg": "RS256"')
    if n:
        text = text.replace('"alg": "RS256"', '"alg": "ES256"'); done.append("A-126: %d headers RS256 -> ES256" % n)
    else:
        done.append("A-126: headers already ES256")

    # A-126 keys
    for name, tag in [("B.1.1", "agd"), ("B.1.2", "ix")]:
        for nm, a, b in list(blocks(text)):
            if nm != name: continue
            d = json.loads(text[a:b])
            def swap(o):
                if isinstance(o, dict):
                    if o.get("kty") == "RSA": o.clear(); o.update(ec(tag)); return True
                    return any(swap(v) for v in o.values())
                if isinstance(o, list): return any(swap(v) for v in o)
                return False
            if swap(d):
                text = text[:a] + json.dumps(d, indent=2, ensure_ascii=False) + text[b:]
                done.append("A-126: %s RSA JWK -> EC P-256" % name)

    for l in done: print("  " + l)
    bad = [nm for nm, a, b in blocks(text) if not _ok(text[a:b])]
    if bad: print("\n  ABORTED -- would not parse: %s" % bad); sys.exit(1)
    print("  all JSON examples parse")

    if dry: print("\n  --dry-run: nothing written"); return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written")


def _ok(s):
    try: json.loads(s); return True
    except Exception: return False


if __name__ == "__main__":
    main()
