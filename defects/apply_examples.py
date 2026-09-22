#!/usr/bin/env python3
"""
Workstream A items independent of the role-VC decision: A-111, A-113, A-114,
A-116, A-118. (A-115 needs an author's judgement, not a script; see below.)

    python3 defects/apply_examples.py --dry-run
    python3 defects/apply_examples.py

Every edit is to an example that survives the DID Document proposal, and every
DID written here uses the form the surrounding examples already use, so nothing
pre-judges the syntax decision (D-403). When that decision lands, all DIDs are
rewritten together.

A-111  B.2.4: the issuer of a UniversityDegreeCredential is an Interchange DID.
       Give it an Issuer DID, in the same shape B.2.9 uses for an Issuer.
A-113  B.2.2 and B.2.3 share a malformed UUID (nine hex digits, a non-hex 'n').
       Distinct valid UUIDs for each.
A-114  B.1.3 and B.1.4 share a request_id. Distinct.
A-116  B.2.2 subject is the placeholder {subject_did}. Use the same User DID
       B.2.3 uses, so the offer and the token that redeems it name one subject.
A-118  B.3.1 is branded example.com with a mismatched authorization server.
       One consistent host under the reserved .example TLD.

A-115  B.1.5 carries sample values substituted during the JSON repair (a name,
       an address, an email, a phone number). They are plausible and consistent
       but were not authored. Someone who knows what the example is meant to
       show should confirm or replace them. Not scriptable.

Validates every JSON block before writing. Safe to re-run.
"""

import sys, os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

EDITS = [
 # (id, example, find, replace)
 ("A-111", "B.2.4",
  '"issuer": "did:adi:eedec811-0f26-4656-a6cd-59d5f0bf2c16/region_1/ix_3"',
  '"issuer": "did:adi:eedec811-0f26-4656-a6cd-59d5f0bf2c16/region_1/ix_3/issuer_1"'),

 ("A-113", "B.2.2",
  '"id": "7560e8400-e79n-21d4-f719-748646810442"',
  '"id": "7560e840-0e79-4d21-9f71-974864681044"'),
 ("A-113", "B.2.3",
  '"id": "7560e8400-e79n-21d4-f719-748646810442"',
  '"id": "7560e840-0e79-4d21-9f71-974864681044"'),

 ("A-113", "B.2.7",
  '"request_id": "aa2f772-0c23-4d11-99b6-c7fdc932ca26"',
  '"request_id": "aa2f7720-0c23-4d11-99b6-c7fdc932ca26"'),

 ("A-114", "B.1.4",
  '"request_id": "bb20b6aa-2063-45f5-ab20-9f2b4f1224ec"',
  '"request_id": "c4d1e7f2-8a3b-4c5d-9e6f-1a2b3c4d5e6f"'),

 ("A-116", "B.2.2",
  '"subject": "did:adi:{subject_did}"',
  '"subject": "did:adi:user2/r_1/ix_1"'),

 ("A-118", "B.3.1", "https://credential-issuer.example.com", "https://issuer1.ix1.adi.example"),
 ("A-118", "B.3.1", "https://users.adi.com",                  "https://users.ix1.adi.example"),
 ("A-118", "B.3.1", "https://vault.example.com",              "https://vault.ix1.adi.example"),
 ("A-118", "B.3.1", "https://university.example.edu",         "https://university.example"),
]

# B.2.2 and B.2.3 are an offer and the token that redeems it; the same id ties them
# together deliberately. A-113 replaces the malformed value in both with one valid value.


def blocks(text):
    """(name, start, end) of the first json block under each B.x.y heading"""
    names = [(m.group(1), m.end()) for m in re.finditer(r"^#{2,3} (B\.\d+\.\d+)", text, re.M)]
    for i, (name, pos) in enumerate(names):
        limit = names[i + 1][1] if i + 1 < len(names) else len(text)
        m = re.search(r"```json\n(.*?)\n```", text[pos:limit], re.S)
        if m:
            yield name, pos + m.start(1), pos + m.end(1)


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()
    done, skipped = [], []

    for did, ex, find, repl in EDITS:
        hit = None
        for name, a, b in blocks(text):
            if name == ex: hit = (a, b); break
        if not hit:
            skipped.append("%s: example %s not found" % (did, ex)); continue
        a, b = hit
        body = text[a:b]
        if find not in body:
            if repl in body: skipped.append("%s %s: already applied" % (did, ex))
            else:            skipped.append("%s %s: text not found -- left alone" % (did, ex))
            continue
        text = text[:a] + body.replace(find, repl) + text[b:]
        done.append("%s %s: %s" % (did, ex, repl[:60]))

    for l in done:    print("  updated : %s" % l)
    for l in skipped: print("  skipped : %s" % l)

    bad = []
    for name, a, b in blocks(text):
        try: json.loads(text[a:b])
        except Exception as e: bad.append(name)
    if bad:
        print("\n  ABORTED -- JSON would not parse: %s" % ", ".join(bad)); sys.exit(1)
    print("  all JSON examples parse")
    print("\n  A-115 (B.1.5 sample values) needs an author's eye, not a script.")

    if dry: print("\n  --dry-run: nothing written"); return
    if not done: print("\n  nothing to change"); return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written")


if __name__ == "__main__":
    main()
