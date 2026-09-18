#!/usr/bin/env python3
"""
F-601 + F-603: replace Google Docs links with stable in-document anchors.

Run from the kit folder:   python3 defects/add_anchors.py
Safe to re-run: it never adds an anchor that is already there.
"""
import re, sys, os

SPEC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spec", "adia_v3.md")

# heading-text fragment  ->  anchor id   (fragments are matched case-insensitively, numbers ignored)
ANCHORS = {
    "Roles and Authorities":                 "roles-and-authorities",
    "8.7.3 HIDA":                            "governance-hida",
    "Verifiable Credential Issuance":        "vc-issuance",
    "Verifiable Credential Presentation":    "vc-presentation",
    "create_agd":                            "create-agd",
    "enroll_ix":                             "enroll-ix",
    "enroll_issuer":                         "enroll-issuer",
    "enroll_sp":                             "enroll-sp",
    "enroll_user":                           "enroll-user",
    "B.2.2 vc_offer":                        "vc-offer",
    "issue_vc_token":                        "issue-vc-token",
    "ADI-IX role VC":                        "adi-ix-role-vc",
    "ADI-ISSUER role VC":                    "adi-issuer-role-vc",
    "ADI-SP role VC":                        "adi-sp-role-vc",
    "Informative References":            "informative-references",
}

# current link target (exactly as written in the spec)  ->  stable target
TARGETS = {
    "#10-vc-presentation":           "#vc-presentation",
    "#6.3 roles and authorities":    "#roles-and-authorities",
    "#9.-vc-issuance-protocols":     "#vc-issuance",
    "#b.1.1-create_agd":             "#create-agd",
    "#b.1.3-enroll_ix":              "#enroll-ix",
    "#b.1.4-enroll_user":            "#enroll-user",
    "#b.1.5-enroll_sp":              "#enroll-sp",
    "#b.1.6-enroll_user":            "#enroll-user",
    "#b.2.2-vc_offer":               "#vc-offer",
    "#b.2.3-issue_vc_token":         "#issue-vc-token",
    "#b.3.3-adi-ix-role-vc":         "#adi-ix-role-vc",
    "#b.3.4-adi-issuer-role-vc":     "#adi-issuer-role-vc",
    "#b.3.5-adi-sp-role-vc":         "#adi-sp-role-vc",
    "#c.1 informative references":   "#informative-references",
}

text = open(SPEC, encoding="utf-8").read()
lines = text.split("\n")

# 1. anchors above headings
added = 0
for frag, aid in ANCHORS.items():
    tag = '<a id="%s"></a>' % aid
    if tag in text:
        continue
    hit = None
    for i, l in enumerate(lines):
        if re.match(r"^#{1,4} ", l) and frag.lower() in l.lower():
            hit = i; break
    if hit is None:
        print("  WARNING: no heading contains '%s' -- anchor %s not added" % (frag, aid)); continue
    lines.insert(hit, tag); added += 1
    text = "\n".join(lines)

# 1b. anchor every remaining heading
def _slug(h):
    h = re.sub(r"^(?:Appendix [A-Z][.:\u2013\u2014-]?|[A-Z]\.(?:\d+(?:\.\d+)*\.?)?|\d+(?:\.\d+)*\.?)\s*", "", h)
    h = re.sub(r"[*_`]", "", h)
    return re.sub(r"[^a-z0-9]+", "-", h.lower()).strip("-") or "section"

lines = text.split("\n")
existing = set(re.findall(r'<a id="([^"]+)"', text))
# first pass: which base names appear more than once? those all get parent-qualified
_counts = {}
for l in lines:
    m = re.match(r"^(#{1,4}) (.*)$", l)
    if m: _counts[_slug(m.group(2))] = _counts.get(_slug(m.group(2)), 0) + 1
shared = {k for k, v in _counts.items() if v > 1}
parents = {}                      # depth -> slug of most recent heading at that depth
out, auto = [], 0
i = 0
while i < len(lines):
    l = lines[i]
    m = re.match(r"^(#{1,4}) (.*)$", l)
    if m:
        depth, title = len(m.group(1)), m.group(2).strip()
        base = _slug(title)
        parents[depth] = base
        for d in list(parents):
            if d > depth: del parents[d]
        already = out and out[-1].startswith("<a id=")
        if not already:
            aid = base
            if base in shared or aid in existing:            # shared name -> qualify with parent
                par = parents.get(depth - 1)
                aid = ("%s-%s" % (par, base)) if par else base
            n = 2
            while aid in existing:                           # still taken -> numeric suffix, last resort
                aid = "%s-%d" % (base, n); n += 1
            out.append('<a id="%s"></a>' % aid)
            existing.add(aid); auto += 1
    out.append(l); i += 1
text = "\n".join(out)

# 2. rewrite links by exact target
rewritten = 0
for old, new in TARGETS.items():
    n = text.count("](%s)" % old)
    if n:
        text = text.replace("](%s)" % old, "](%s)" % new); rewritten += n
# also strip leftover <u> tags inside link labels
text = re.sub(r"\[<u>([^\]]*?)</u>\]", r"[\1]", text)

open(SPEC, "w", encoding="utf-8").write(text)
ids  = set(re.findall(r'<a id="([^"]+)"', text))
refs = set(re.findall(r"\]\(#([^)]+)\)", text))
left = sorted(refs - ids)
print("targeted anchors added: %d   all-heading anchors added: %d   links rewritten: %d   unresolved: %d" % (added, auto, rewritten, len(left)))
for r in left:
    print("  unresolved: #%s   (run: make explain ID=F-603)" % r)
