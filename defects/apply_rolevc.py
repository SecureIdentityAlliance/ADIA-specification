#!/usr/bin/env python3
"""
Role-credential example fixes, unblocked by RK's decision of 22 Sep to retain
role VCs issued by the onboarding Interchange.

    python3 defects/apply_rolevc.py --dry-run
    python3 defects/apply_rolevc.py

A-102  B.2.9 / B.2.10 / B.2.11: id_doc carries the Interchange's key, not the
       subject's. A DIDdoc holds the key of its own DID. Set id_doc.id = subject
       and give each its own key material (placeholder JWK values, distinct).
A-103  B.2.7: a self-signed root must have issuer == subject.
A-105  B.2.7: the AGD's entitlement must include the Interchange credential,
       or the network cannot be bootstrapped.
A-106  B.2.8: the Interchange's entitlement must include Issuer, SP and User.
A-109  B.2.11: the User's subject DID is an Issuer path.
A-112  B.2.7-B.2.11: "type" -> "typ", add "kid" (the five remaining).

Type strings use the values already in the examples' own "type" fields; the
registry decision (D4) may rename them later. DID forms use the shape the
surrounding examples already use; D-403 rewrites all DIDs together.

Every block is re-parsed before writing. Safe to re-run.
"""

import sys, os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

AGD  = "did:adi:8c019421-2920-410c-acfe-77d5c87b187c"
IX   = "did:adi:f6e18f71-4311-4e09-8bfc-9980a90e4be7/region_1/ix_1"
ISS  = "did:adi:3b576f82-3506-4663-8ca4-51d614aea318/region_1/ix_1/issuer_1"
SP   = "did:adi:9d0e5f61-7c2a-4b83-a1f4-2e6b7c8d9e0f/region_1/ix_1/sp_1"
USER = "did:adi:45bde61c-7da0-4f85-aed4-39d2d7508e99/region_1/ix_1"

# distinct placeholder JWKs so no two entities share a key
def jwk(tag):
    return {"kty": "EC", "crv": "P-256",
            "x": "%s_x_placeholder_public_key_value_00000000" % tag,
            "y": "%s_y_placeholder_public_key_value_00000000" % tag}


def blocks(text):
    names = [(m.group(1), m.end()) for m in re.finditer(r"^#{2,3} (B\.\d+\.\d+)", text, re.M)]
    for i, (name, pos) in enumerate(names):
        limit = names[i + 1][1] if i + 1 < len(names) else len(text)
        m = re.search(r"```json\n(.*?)\n```", text[pos:limit], re.S)
        if m:
            yield name, pos + m.start(1), pos + m.end(1)


def find(o, k):
    if isinstance(o, dict):
        if k in o: return o
        for v in o.values():
            r = find(v, k)
            if r is not None: return r
    elif isinstance(o, list):
        for i in o:
            r = find(i, k)
            if r is not None: return r
    return None


def fix(name, d, log):
    """mutate the parsed example in place; append human-readable notes to log"""
    h = find(d, "alg")
    if h is not None and "type" in h:
        h["typ"] = h.pop("type"); log.append("%s: type -> typ" % name)
    signer = {"B.2.7": AGD, "B.2.8": AGD, "B.2.9": IX, "B.2.10": IX, "B.2.11": IX}[name]
    if h is not None and "kid" not in h:
        h["kid"] = signer + "#key-1"; log.append("%s: kid added" % name)

    subj = {"B.2.7": AGD, "B.2.8": IX, "B.2.9": ISS, "B.2.10": SP, "B.2.11": USER}[name]
    tag  = {"B.2.7": "agd", "B.2.8": "ix", "B.2.9": "issuer", "B.2.10": "sp", "B.2.11": "user"}[name]

    p = find(d, "issuer")
    if p is not None:
        if p.get("issuer") != signer: p["issuer"] = signer; log.append("%s: issuer -> %s" % (name, tag if name == "B.2.7" else "signer"))
    s = find(d, "subject")
    if s is not None and s.get("subject") != subj:
        s["subject"] = subj; log.append("%s: subject corrected" % name)

    idd = find(d, "id_doc")
    if idd is not None and isinstance(idd.get("id_doc"), dict):
        doc = idd["id_doc"]
        if doc.get("id") != subj:
            doc["id"] = subj; log.append("%s: id_doc.id = subject" % name)
        pk = find(doc, "public_key")
        if pk is not None and pk["public_key"] != jwk(tag):
            pk["public_key"] = jwk(tag); log.append("%s: id_doc key is the subject's" % name)

    r = find(d, "authorized_to_issue")
    if r is not None:
        want = {"B.2.7": ["ADI-IX-VC"],
                "B.2.8": ["ADI-ISSUER-VC", "ADI-SP-VC", "ADI-User-VC"],
                "B.2.9": [], "B.2.10": [], "B.2.11": []}[name]
        if r["authorized_to_issue"] != want:
            r["authorized_to_issue"] = want; log.append("%s: authorized_to_issue = %s" % (name, want))


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()
    log = []
    edits = []
    for name, a, b in blocks(text):
        if name not in ("B.2.7", "B.2.8", "B.2.9", "B.2.10", "B.2.11"): continue
        raw = text[a:b]
        d = json.loads(raw)
        before = json.dumps(d, sort_keys=True)
        fix(name, d, log)
        if json.dumps(d, sort_keys=True) != before:
            edits.append((a, b, json.dumps(d, indent=2, ensure_ascii=False)))

    for a, b, new in sorted(edits, reverse=True):
        text = text[:a] + new + text[b:]

    for l in log: print("  " + l)
    print("\n  %d example blocks rewritten" % len(edits))

    bad = [n for n, a, b in blocks(text) if not _ok(text[a:b])]
    if bad: print("\n  ABORTED -- would not parse: %s" % bad); sys.exit(1)

    if dry: print("\n  --dry-run: nothing written"); return
    if not edits: print("\n  nothing to change"); return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written -- now run: make save")


def _ok(s):
    try: json.loads(s); return True
    except Exception: return False


if __name__ == "__main__":
    main()
