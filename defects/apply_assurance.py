#!/usr/bin/env python3
"""
Apply the ASSURANCE_MODEL.md data model changes to Appendix B.

    python3 defects/apply_assurance.py --dry-run
    python3 defects/apply_assurance.py

Scope, deliberately narrow:
  B.2.7 / B.2.8 / B.2.9   authorized_max_assurance_level -> max_ial / max_aal / max_fal
  B.2.10                  authorized_max_assurance_level -> min_ial / min_aal / min_fal
  B.2.5  vc_request       add min_ial / min_aal / min_fal

It does NOT touch authorized_to_issue. Those values are wrong (A-105, A-106,
A-107) but they are blocked on decision D4, and mixing the two makes an
unreviewable commit.

Edits are made textually so the surrounding formatting, comments and key order
are preserved. Re-running is safe: blocks already converted are skipped.
"""

import sys, os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

# ceilings for parties that issue; floors for parties that verify
PROVIDER = '"max_ial": 3,\n        "max_aal": 2,\n        "max_fal": 2'
VERIFIER  = '"min_ial": 2,\n        "min_aal": 2,\n        "min_fal": 1'
TARGETS = {"B.2.7": PROVIDER, "B.2.8": PROVIDER, "B.2.9": PROVIDER, "B.2.10": VERIFIER}

REQUEST_FIELDS = '''  "min_ial": 2,
  "min_aal": 2,
  "min_fal": 1,
'''

def blocks(text):
    """yield (name, start, end) for each fenced json block under a B.x.y heading"""
    names = [(m.group(1), m.end()) for m in re.finditer(r"^#{2,3} (B\.\d+\.\d+)", text, re.M)]
    for name, pos in names:
        m = re.search(r"```json\n(.*?)\n```", text[pos:], re.S)
        if m:
            yield name, pos + m.start(1), pos + m.end(1)

def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()
    changed, skipped, missing = [], [], []

    # role VCs: swap the assurance field, keep indentation
    for name, a, b in list(blocks(text)):
        if name not in TARGETS:
            continue
        body = text[a:b]
        if "max_ial" in body or "min_ial" in body:
            skipped.append(name); continue
        m = re.search(r'([ \t]*)"authorized_max_assurance_level"\s*:\s*\[[^\]]*\]', body)
        if not m:
            missing.append(name); continue
        indent = m.group(1)
        repl = TARGETS[name].replace("\n        ", "\n" + indent)
        new = body[:m.start()] + indent + repl + body[m.end():]
        text = text[:a] + new + text[b:]
        changed.append(name)

    # vc_request: add the floors after the audience/nonce block
    for name, a, b in list(blocks(text)):
        if name != "B.2.5":
            continue
        body = text[a:b]
        if "min_ial" in body:
            skipped.append(name); break
        m = re.search(r'([ \t]*)"schemas_accepted"', body)
        if not m:
            missing.append(name); break
        ins = REQUEST_FIELDS.replace("\n  ", "\n" + m.group(1)).rstrip() + "\n" + m.group(1)
        new = body[:m.start()] + m.group(1) + ins.lstrip() + body[m.start(2) if m.lastindex and m.lastindex > 1 else m.start():][len(m.group(1)):]
        # simpler: insert the three lines immediately before the matched line
        new = body[:m.start()] + m.group(1) + REQUEST_FIELDS.strip().replace("\n  ", "\n" + m.group(1)) + "\n" + body[m.start():]
        text = text[:a] + new + text[b:]
        changed.append(name)
        break

    print("  updated: %s" % (", ".join(changed) or "none"))
    if skipped: print("  already converted, skipped: %s" % ", ".join(skipped))
    if missing: print("  field not found, left alone: %s" % ", ".join(missing))

    # validate every block still parses before writing
    bad = []
    for name, a, b in blocks(text):
        try: json.loads(text[a:b])
        except Exception as e: bad.append("%s (%s)" % (name, str(e)[:40]))
    if bad:
        print("\n  ABORTED -- these would no longer parse: %s" % ", ".join(bad))
        sys.exit(1)
    print("  all JSON examples still parse")

    if dry:
        print("\n  --dry-run: nothing written"); return
    if not changed:
        print("\n  nothing to change"); return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written")

if __name__ == "__main__":
    main()
