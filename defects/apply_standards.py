#!/usr/bin/env python3
"""
Adopt normal standards where the draft invented or left open something that
an established standard already settles. Plus three corrections that were
drafted but never landed.

    python3 defects/apply_standards.py --dry-run
    python3 defects/apply_standards.py

Adoptions:
  C-306  error model            RFC 9457 Problem Details for HTTP APIs
  C-307  versioning             a declared protocol version in metadata and every request
  D7     signature algorithms   RFC 8725 (JWT BCP) + RFC 7518: ES256 REQUIRED, EdDSA RECOMMENDED
  D10    vault discovery        a DID Core service entry in the User's DIDdoc
  A-117  vc_authorization_token RFC 7519 registered claims replace the undocumented ones

Corrections drafted earlier but not applied:
  B-205  two AAL3 sentences in 7.2.3 (ASSURANCE_MODEL §5, rows 1-2)
  B-204  clause 5.4 signs the credential before consent is obtained
  C-309  clause 8.2 has no prose flow description

Safe to re-run.
"""

import sys, os, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

EDITS = [
 # ---- B-205 ----
 ("B-205", "An ADI wallet authenticates the user with a NIST 800-63 Assurance Level AAL1, AAL2 & AAL3, and conveys that level in ADI-Network transactions.",
           "An ADI wallet authenticates the User at NIST SP 800-63 authentication assurance level 1 or 2 as determined by clause 7.2.4, and conveys the achieved `ial`, `aal` and `fal` values in ADI-Network transactions."),
 ("B-205", "using strong authenticators capable of AAL1, AAL2 or AAL3 assurance levels.",
           "using authenticators meeting the requirements of clause 7.2.4.3."),
 # ---- B-204 ----
 ("B-204", "2.  The Credential Issuer’s software assembles the Claims into a Credential and validates completeness against the Credential Schema. The package of Claims and Metadata is then signed using the Credential Issuer’s private key and becomes a VC.",
           "2.  The Credential Issuer’s software assembles the Claims into a Credential and validates completeness against the Credential Schema. The Credential is not yet signed; signing occurs only after the Holder has approved issuance (step 3 below)."),
 ("B-204", "3.  Upon receiving approval from the Holder, the Credential Issuer submits the VC to the Interchange",
           "3.  Upon receiving approval from the Holder, the Credential Issuer signs the package of Claims and Metadata with its private key — at which point it becomes a VC — and submits the VC to the Interchange"),
 # ---- A-117 ----
 ("A-117", '"vc_authorization_token": "eyJ',
           '"vc_authorization_token": "eyJ'),   # placeholder; real edit below replaces the whole block
]

C309_PROSE = '''The following request and response JSON objects are used during Interchange enrollment.

An Interchange applicant generates its signing key pair in a hardware security module and submits an enrollment request to the ADI Global Domain carrying its public key, key identifier, proposed Digital Address and enrollment form.

**IX_APPLICANT -\\> AGD: POST ~agd/enroll_ix**

The ADI Global Domain MUST vet the applicant against network governance policy before proceeding. On approval it assigns the Interchange a network-unique name (clause 7.4.1), creates the Interchange's DID and DIDdoc from the submitted public key, and signs the ADI-IX role VC recording the Interchange's entitlements.

**AGD -\\> AGD: Vet applicant; assign Interchange name; create DID and DIDdoc**

**AGD -\\> AGD: Sign ADI-IX role VC**

**AGD -\\> AGD_VAULT: Store ADI-IX role VC**

The ADI Global Domain adds the Interchange to the network directory, then returns the DID, DIDdoc, role VC and directory endpoints to the applicant, which provisions its Digital Address Service with them.

**AGD -\\> AGD: Add Interchange to network directory**

**AGD -\\> IX_APPLICANT: Return DID, DIDdoc, ADI-IX role VC, directory endpoints**

**IX_APPLICANT -\\> IX_DAS: Provision DAS with credential and AGD endpoints**
'''

# ---- new clauses ----
ERR_CLAUSE = '''
<a id="error-responses"></a>
## 6.8 Error responses

Every ADI-Network endpoint that rejects a request MUST return an error response conforming to [RFC9457], *Problem Details for HTTP APIs*, with media type `application/problem+json`. The `type` member MUST be a URI in the `https://adiassociation.org/problems/` namespace, from the registry in Appendix C.1; `title` and `status` MUST be present; `detail` SHOULD explain the failure without disclosing information a caller is not entitled to; and `instance` SHOULD carry the request identifier so the failure can be correlated with the Interchange audit record (clause 12.9).

```json
{
  "type": "https://adiassociation.org/problems/not-entitled",
  "title": "Issuer not entitled to issue this credential type",
  "status": 403,
  "detail": "The Issuer's ADI-ISSUER role credential does not list UniversityDegreeCredential.",
  "instance": "urn:adi:request:7560e840-0e79-4d21-9f71-974864681044"
}
```

A response with `status` 429 or 503 MUST carry a `Retry-After` header. Clients MUST NOT retry a 4xx response other than 429 without changing the request.
'''

VER_CLAUSE = '''
<a id="protocol-version"></a>
## 6.9 Protocol version

Every participant's metadata (B.3.1) MUST declare `"adia_versions_supported"`, an array of the protocol versions it implements, and every ADI-Network request MUST carry `"adia_version"` naming the version under which it is made. A participant receiving a request for a version it does not support MUST reject it with the `unsupported-version` problem type (clause 6.8) and MUST list its supported versions in `detail`.

Versions are of the form `MAJOR.MINOR`. A change of MINOR adds optional capability and MUST remain interoperable with earlier MINOR versions of the same MAJOR; a change of MAJOR MAY break interoperability. This document defines version `3.0`.
'''

ALG_CLAUSE = '''
<a id="signature-algorithms"></a>
### 6.1.3 Signature algorithms

The following JSON Web Signature algorithms [RFC7518] are permitted. Implementations MUST follow the JSON Web Token Best Current Practices [RFC8725].

| Algorithm | Status | Key |
|---|---|---|
| `ES256` | REQUIRED — every conforming implementation MUST be able to produce and verify it | EC P-256 |
| `EdDSA` (Ed25519) | RECOMMENDED | OKP Ed25519 |
| `RS256`, `PS256` | NOT RECOMMENDED for new signatures; a verifier MAY accept them until 1 January 2028 | RSA, 3072 bits or more |
| any `HS*` | MUST NOT be used | — |
| `none` | MUST NOT be used | — |

A verifier MUST reject a signature whose algorithm is not in this table, and MUST apply the key-type check of clause 6.2 so that a token cannot select an algorithm inconsistent with the key it is verified against. The `kid` requirement of clause 6.1.1 applies to every algorithm.
'''

VAULT_TEXT = ("A credential is stored either in the Issuer's vault or in the User's. The location of the User's vault is published as a "
              "`service` entry of type `ADIVault` in the User's DIDdoc (B.3.5), and a USER_AGENT MUST consult that entry first; "
              "the Issuer's vault, published in the Issuer's metadata as `credential_vault_endpoint`, is the fallback where the "
              "User has none.")

AUTH_TOKEN = '''{
  "header": {
    "alg": "ES256",
    "typ": "JWT",
    "kid": "did:adi:7t7IEQ8mRlamzVnV8L8sFg#key-1"
  },
  "payload": {
    "iss": "did:adi:7t7IEQ8mRlamzVnV8L8sFg",
    "sub": "did:adi:7t7IEQ8mRlamzVnV8L8sFg",
    "aud": "https://vault.ix1.adi.example",
    "iat": 1758240100,
    "exp": 1758240400,
    "jti": "c9d2f1a4-3b7e-4f60-9a1d-2e5c8b7f6a30",
    "nonce": "n-0S6_WzA2Mj",
    "vc_id": "https://university.example/credentials/3732",
    "purpose": "present"
  },
  "signature": "…"
}'''


def blocks(text):
    names = [(m.group(1), m.end()) for m in re.finditer(r"^#{2,3} (B\.\d+\.\d+)", text, re.M)]
    for i, (name, pos) in enumerate(names):
        lim = names[i + 1][1] if i + 1 < len(names) else len(text)
        m = re.search(r"```json\n(.*?)\n```", text[pos:lim], re.S)
        if m: yield name, pos + m.start(1), pos + m.end(1)


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()
    done, skipped = [], []

    for tag, a, b in EDITS:
        if a == b: continue
        if a in text: text = text.replace(a, b, 1); done.append("%s %s" % (tag, b[:60]))
        elif b[:50] in text: skipped.append("%s already" % tag)
        else: skipped.append("%s NOT FOUND: %s" % (tag, a[:50]))

    # C-309 prose into 8.2
    old = "The following request and response JSON objects are used during Interchange enrollment.\n"
    i = text.find("## 8.2 Enrolling an Interchange")
    if i != -1 and "IX_APPLICANT -\\> AGD" not in text:
        j = text.find(old, i)
        if j != -1 and j - i < 400:
            text = text[:j] + C309_PROSE + text[j + len(old):]; done.append("C-309 8.2 flow description added")
        else: skipped.append("C-309 anchor sentence not found under 8.2")
    elif "IX_APPLICANT -\\> AGD" in text: skipped.append("C-309 already")

    # 6.1.3 algorithms, 6.8 errors, 6.9 version — inserted before 6.2, 6.3 heading region, and before 7 respectively
    def insert_before(text, heading_regex, clause, marker, label):
        if marker in text: skipped.append(label + " already"); return text
        m = re.search(r"\n(<a id=\"[^\"]*\"></a>\n)?" + heading_regex, text)
        if not m: skipped.append(label + ": insertion point not found"); return text
        done.append(label + " added"); return text[:m.start()] + "\n" + clause + text[m.start():]
    text = insert_before(text, r"## 6\.2 ", ALG_CLAUSE, '<a id="signature-algorithms"></a>', "D7 6.1.3 Signature algorithms")
    text = insert_before(text, r"# 7\. ",   ERR_CLAUSE, '<a id="error-responses"></a>',      "C-306 6.8 Error responses")
    text = insert_before(text, r"# 7\. ",   VER_CLAUSE, '<a id="protocol-version"></a>',     "C-307 6.9 Protocol version")

    # D10 vault discovery sentence into 9.2.3 where the vault choice is described
    if "service` entry of type `ADIVault`" not in text:
        m = re.search(r"[^\n]*(issuer vault or user vault|user vault or issuer vault|VC Vault)[^\n]*\n", text[text.find("### 9.2.3"):])
        if m:
            pos = text.find("### 9.2.3") + m.end()
            text = text[:pos] + "\n" + VAULT_TEXT + "\n" + text[pos:]; done.append("D10 vault discovery sentence added in 9.2.3")
        else: skipped.append("D10: vault sentence anchor not found")
    else: skipped.append("D10 already")

    # A-117: replace the B.2.6 example
    for name, a, b in list(blocks(text)):
        if name == "B.2.6":
            if '"purpose": "present"' in text[a:b]: skipped.append("A-117 already"); break
            text = text[:a] + AUTH_TOKEN + text[b:]; done.append("A-117 B.2.6 rebuilt with RFC 7519 claims"); break

    # metadata: adia_versions_supported into B.3.1
    for name, a, b in list(blocks(text)):
        if name == "B.3.1":
            d = json.loads(text[a:b])
            if "adia_versions_supported" not in d:
                d = {"adia_versions_supported": ["3.0"], **d}
                text = text[:a] + json.dumps(d, indent=2, ensure_ascii=False) + text[b:]; done.append("C-307 B.3.1 adia_versions_supported")
            break

    # register the two new normative references
    if "[RFC9457]" not in text[text.find("# Appendix A"):]:
        ins = ('**[RFC8725]**\nSheffer, Y., Hardt, D., and M. Jones, "JSON Web Token Best Current Practices", BCP 225, RFC 8725, DOI 10.17487/RFC8725, February 2020, <https://www.rfc-editor.org/info/rfc8725>.\n\n'
               '**[RFC9457]**\nNottingham, M., Wilde, E., and S. Dalal, "Problem Details for HTTP APIs", RFC 9457, DOI 10.17487/RFC9457, July 2023, <https://www.rfc-editor.org/info/rfc9457>.\n\n'
               '**[RFC7518]**\nJones, M., "JSON Web Algorithms (JWA)", RFC 7518, DOI 10.17487/RFC7518, May 2015, <https://www.rfc-editor.org/info/rfc7518>.\n\n')
        k = text.find("**[RFC9562]**")
        if k != -1: text = text[:k] + ins + text[k:]; done.append("Appendix A: RFC 7518, 8725, 9457 added")

    for l in done:    print("  updated : %s" % l)
    for l in skipped: print("  skipped : %s" % l)
    for nm, a, b in blocks(text):
        try: json.loads(text[a:b])
        except Exception as e: print("  ABORTED: %s no longer parses: %s" % (nm, str(e)[:50])); sys.exit(1)

    if dry: print("\n  --dry-run: nothing written"); return
    if not done: print("\n  nothing to change"); return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written -- now run: make anchors && make notes")


if __name__ == "__main__":
    main()
