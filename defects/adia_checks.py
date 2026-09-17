#!/usr/bin/env python3
"""
ADIA specification defect checks.

Each entry in CHECKS is keyed by a defect ID from the register and returns
True when the defect is resolved in the spec file under test.

    python3 adia_checks.py spec.md            # human-readable report
    python3 adia_checks.py spec.md --ci       # exit 1 if any check regresses
    python3 adia_checks.py spec.md --status   # ID,STATUS pairs for the register

A check answers only "is this specific assertion true of the document now".
It never claims a defect was understood, discussed, or correctly fixed --
that judgement stays with a reviewer, which is why the register distinguishes
Fixed (author's claim) from Verified (this harness agrees).
"""

import sys, os, re, json, collections

# ───────────────────────── document model ─────────────────────────

class Spec:
    def __init__(self, path):
        self.path = path
        self.text = open(path, encoding="utf-8").read()
        self.blocks = re.findall(r"```json\n(.*?)\n```", self.text, re.S)
        self.names  = re.findall(r"^#{2,3} (B\.\d+\.\d+)", self.text, re.M)
        self.J = {}
        self.unparsed = []
        for n, b in zip(self.names, self.blocks):
            try:
                self.J[n] = json.loads(b)
            except Exception:
                self.unparsed.append(n)
        # prose only: examples excluded, so wording checks aren't fooled by payloads
        self.prose = re.sub(r"```json.*?```", "", self.text, flags=re.S)

    def find(self, name, key):
        """First value for `key` anywhere inside example `name`."""
        def walk(o):
            if isinstance(o, dict):
                if key in o:
                    return o[key]
                for v in o.values():
                    r = walk(v)
                    if r is not None:
                        return r
            elif isinstance(o, list):
                for i in o:
                    r = walk(i)
                    if r is not None:
                        return r
            return None
        return walk(self.J.get(name, {}))

    def id_doc_id(self, name):
        d = self.find(name, "id_doc")
        return d.get("id") if isinstance(d, dict) else None

    def dids(self):
        return set(re.findall(r"did:adi:[A-Za-z0-9_\-{}/.]*", self.text))

    def headings(self):
        return [(i + 1, l) for i, l in enumerate(self.text.split("\n"))
                if re.match(r"^#{1,4} ", l)]


UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
UUIDISH = re.compile(r"\b[0-9a-zA-Z]{6,10}-[0-9a-zA-Z]{3,5}-[0-9a-zA-Z]{3,5}-"
                     r"[0-9a-zA-Z]{3,5}-[0-9a-zA-Z]{10,14}\b")

ROLE_VCS = ("B.2.7", "B.2.8", "B.2.9", "B.2.10", "B.2.11")

# ───────────────────────── checks ─────────────────────────
# Every lambda takes a Spec and returns True when the defect is resolved.

CHECKS = {

# ---- Workstream A: data model and examples ----
"A-101": lambda s: s.find("B.1.2", "role") == s.find("B.2.8", "role"),
"A-102": lambda s: all(s.find(n, "subject") == s.id_doc_id(n)
                       for n in ("B.2.9", "B.2.10", "B.2.11")),
"A-103": lambda s: s.find("B.2.7", "issuer") == s.find("B.2.7", "subject"),
"A-104": lambda s: s.find("B.2.7", "subject") == s.id_doc_id("B.2.7"),
"A-105": lambda s: any("IX" in x.upper() or "INTERCHANGE" in x.upper()
                       for x in (s.find("B.2.7", "authorized_to_issue") or [])),
"A-106": lambda s: len(s.find("B.2.8", "authorized_to_issue") or []) >= 3,
"A-109": lambda s: "issuer" not in str(s.find("B.2.11", "subject")).lower(),
"A-110": lambda s: _msid(s.find("B.2.9", "subject")) != _msid(s.find("B.2.10", "subject")),
"A-112": lambda s: '"type": "JWT"' not in s.text and s.text.count('"kid"') >= 8,
"A-113": lambda s: all(UUID.match(u) for u in UUIDISH.findall(s.text)),
"A-114": lambda s: s.find("B.1.3", "request_id") != s.find("B.1.4", "request_id"),
"A-116": lambda s: "{" not in str(s.find("B.2.2", "subject") or ""),
"A-118": lambda s: "credential-issuer.example.com" not in s.text,
"A-119": lambda s: "batch_credential_endpoint" not in s.text
                   and "deferred_credential_endpoint" not in s.text,
"A-122": lambda s: "tx_code" in s.text and "expires_in" in s.text,
"A-123": lambda s: all(k in json.dumps(s.J.get("B.2.5", {})) for k in ("nonce", "aud")),
"A-124": lambda s: "ns/credentials/v2" in s.text
                   and "2018/credentials/v1" not in s.text
                   and "credentialStatus" in s.text,
"A-126": lambda s: not (("RS256" in s.text) and ("ES256" in s.text)),

# ---- Workstream B: cryptography and protocol ----
"B-201": lambda s: "public key encryption of the hash" not in s.text,
"B-202": lambda s: "USER_AGENT -\\> USER_AGENT" not in s.text,
"B-207": lambda s: "Biometric approval" not in s.text,
"B-209": lambda s: "credentialStatus" in s.text and "revoc" in s.prose.lower(),
"B-213": lambda s: s.text.count('"kid"') >= 8,
"B-216": lambda s: ("vc_authorization_request" not in s.text
                    or "B.2." in _section_of(s, "vc_authorization_request")),
"B-218": lambda s: not ("~issuer/issue_vc\n" in s.text and "~issuer/issue_vc_token" in s.text),
"B-219": lambda s: "~ard/" not in s.text,

# ---- Workstream C: normative structure ----
"C-301": lambda s: _upper_kw(s) > _lower_kw(s),
"C-303": lambda s: re.search(r"^#{1,3}.*Conformance", s.prose, re.M | re.I) is not None,
"C-304": lambda s: re.search(r"^#{1,3}.*Security Considerations", s.prose, re.M | re.I) is not None,
"C-305": lambda s: re.search(r"^#{1,3}.*Privacy Considerations", s.prose, re.M | re.I) is not None,
"C-310": lambda s: "To be completed" not in s.text,

# ---- Workstream D: architecture and terminology ----
"D-401": lambda s: len(re.findall(r"\bard_\w+", s.text)) == 0,
"D-402": lambda s: ("IAL" in s.text and "FAL" in s.text
                    and "800-63-3" not in s.text),
"D-403": lambda s: _did_forms_consistent(s),
"D-407": lambda s: "ADI NETWORK VC" not in s.text,
"D-409": lambda s: not ("Digital Address Application (DAA)" in s.text
                        and "Device Application Agent (DAA)" in s.text),
"D-410": lambda s: "Domain Authorities (AGs)" not in s.text,

# ---- Workstream E: editorial ----
"E-501": lambda s: all(re.match(r"^#{1,4} (?:\d+(?:\.\d+)*\.?|[A-C]\.(?:\d+(?:\.\d+)*\.?)?)\s", l)
                       for _, l in s.headings()),
"E-502": lambda s: all(len(l.lstrip("# ")) <= 80 for _, l in s.headings()),
"E-504": lambda s: "# 6 Accountable" not in s.text,
"E-505": lambda s: "B.1. Schemas" not in s.text,
"E-507": lambda s: not re.search(r"^6\.\s+Issuers may initiate", s.text, re.M),
"E-508": lambda s: "(AD-NU)" not in s.text,
"E-509": lambda s: "[Role}-Agent" not in s.text.replace("\\", ""),
"E-510": lambda s: "Creating and AGD" not in s.text,
"E-511": lambda s: "issuer by are" not in s.text,
"E-512": lambda s: "one more Verifiable Credentials" not in s.text,
"E-513": lambda s: "HIDA usage is implementation and" not in s.text,
"E-514": lambda s: "vetting of the service provider" not in s.text,
"E-515": lambda s: "returns the VC to the SP agent" not in s.text,
"E-516": lambda s: "used during Issuer enrollment" not in s.text,
"E-517": lambda s: "provisions an CI_AGENT" not in s.text,
"E-518": lambda s: "Interchange send a" not in s.text,
"E-519": lambda s: "POST return" not in s.text,
"E-522": lambda s: not re.search(r"calls the get\\?_\s*$", s.text, re.M),
"E-523": lambda s: "W3C XXX" not in s.text,
"E-524": lambda s: "figure 7.3" not in s.text and "figure 4.4.3" not in s.text,
"E-525": lambda s: not re.search(r"\u00a7\s*2\.2\.1", s.text),
"E-526": lambda s: not re.search(r"See[^\n]{0,15}3\.3[^\n]{0,25}Roles", s.text),

# ---- Workstream F: references, links, hygiene ----
"F-601": lambda s: "docs.google.com/document" not in s.text,
"F-602": lambda s: "media/image" not in s.text,
"F-603": lambda s: s.text.count('<a id="') >= 20,
"F-604": lambda s: "\u00a0" not in s.text and "\u202f" not in s.text,
"F-605": lambda s: all(l == l.rstrip() for l in s.text.split("\n")),

# ---- standing invariants: these must never regress ----
"INV-json":     lambda s: len(s.unparsed) == 0,
"INV-fences":   lambda s: s.text.count("```") % 2 == 0,
"INV-gremlins": lambda s: _no_gremlins_in_fences(s),
"INV-encoding": lambda s: "\r" not in s.text and s.text.endswith("\n"),
}

# ───────────────────────── helpers ─────────────────────────

def _msid(did):
    """Method-specific id: everything before the first path separator."""
    if not did:
        return None
    return str(did).split("did:adi:")[-1].split("/")[0]

def _upper_kw(s):
    return len(re.findall(r"\b(MUST|SHALL|SHOULD|MAY|REQUIRED|RECOMMENDED)\b", s.prose))

def _lower_kw(s):
    return len(re.findall(r"\b(must|shall|should)\b", s.prose))

def _section_of(s, token):
    i = s.text.find(token)
    if i < 0:
        return ""
    heads = re.findall(r"^#{2,3} (\S+)", s.text[:i], re.M)
    return heads[-1] if heads else ""

def _did_forms_consistent(s):
    """One region/interchange spelling convention, no placeholders, no empty segments."""
    forms = s.dids()
    if any("{" in d or d.rstrip().endswith("/") for d in forms):
        return False
    segs = collections.Counter()
    for d in forms:
        for seg in str(d).split("did:adi:")[-1].split("/")[1:]:
            segs[re.sub(r"[0-9]+$", "", seg).rstrip("_")] += 1
    return len(segs) <= 2

def _no_gremlins_in_fences(s):
    """Curly quotes are fine in prose and fatal inside JSON."""
    inside, bad = False, 0
    for line in s.text.split("\n"):
        if line.startswith("```"):
            inside = not inside
            continue
        if inside and any(c in line for c in "\u00a0\u2018\u2019\u201c\u201d"):
            bad += 1
    return bad == 0

# ───────────────────────── runner ─────────────────────────

def run(path):
    s = Spec(path)
    out = {}
    for cid, fn in CHECKS.items():
        try:
            out[cid] = "PASS" if fn(s) else "FAIL"
        except Exception as e:
            out[cid] = "ERROR: %s" % str(e)[:60]
    return s, out

BASELINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "baseline.json")

def _load_baseline():
    if not os.path.exists(BASELINE):
        return None
    try:
        return json.load(open(BASELINE))
    except Exception:
        return None

def _save_baseline(res):
    json.dump({k: v for k, v in res.items()}, open(BASELINE, "w"), indent=1, sort_keys=True)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    path = sys.argv[1]
    flags = sys.argv[2:]
    s, res = run(path)

    if "--status" in flags:
        for cid, r in res.items():
            print("%s,%s" % (cid, "Verified" if r == "PASS" else "Open"))
        return

    order = ("INV", "A-", "B-", "C-", "D-", "E-", "F-")
    npass = sum(1 for r in res.values() if r == "PASS")
    print("ADIA defect checks  --  %s" % path)
    print("%d of %d checks pass\n" % (npass, len(res)))
    for pre in order:
        rows = [(c, r) for c, r in res.items() if c.startswith(pre)]
        if not rows:
            continue
        print("  %s" % ("standing invariants" if pre == "INV" else "workstream " + pre[0]))
        for cid, r in sorted(rows):
            mark = "ok  " if r == "PASS" else "FAIL"
            print("    %-4s %-10s %s" % (mark, cid, "" if r in ("PASS", "FAIL") else r))
        print()
    if s.unparsed:
        print("  examples that do not parse as JSON: %s" % ", ".join(s.unparsed))
    if "--ci" in flags:
        base = _load_baseline()
        if base is None:
            _save_baseline(res)
            print("  baseline written: %d checks recorded as passing" % npass)
            return
        regressed = sorted(c for c in base if base[c] == "PASS" and res.get(c) != "PASS")
        gained    = sorted(c for c in res if res[c] == "PASS" and base.get(c) != "PASS")
        if gained:
            print("  newly passing: %s" % ", ".join(gained))
            _save_baseline(res)
        if regressed:
            print("\n  REGRESSION -- these passed on the baseline and now fail:")
            for c in regressed:
                print("    %s" % c)
            sys.exit(1)
        print("  no regressions")

if __name__ == "__main__":
    main()
