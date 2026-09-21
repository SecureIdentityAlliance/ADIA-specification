# ADIA v3.0 — Fix Guide for Workstreams A–D

For the engineers working the register. Organised by **root cause**, not by ID, because most of these 70 items are a dozen underlying problems. Each cluster lists the IDs it closes and what "done" means to the checker.

Part 1 gives a **recommended default for each of the twelve open decisions**. Nothing in Parts 2–5 that says *Blocked* can start until the TWG accepts or amends these. A default the group can push against is faster than a blank page.

---

## Part 1 — The twelve decisions, with recommended defaults

| # | Decision | Recommended default | Why |
|---|---|---|---|
| **D1** | ARD prefix | **Drop the prefix.** `ard_da_user_name` → `da_user_name`, `ard_public_key` → `public_key`, `ard_key_id` → `key_id`, `ard_information` → `information`, `ard_enrollment_form` → `enrollment_form`. `~ard/enroll_ix` → `~agd/enroll_ix`. | The fields describe the applicant, not a role. A neutral name is correct for all five enrollment types and never needs renaming again. Restoring ARD as a role adds a tier the architecture no longer has. |
| **D2** | `did:adi` syntax | **Colons, not slashes.** `did:adi:<region>:<ix>:<uuid>` — e.g. `did:adi:r1:ix3:09f4cee0-b3a8-4bfe-a1f7-69d834764159`. Region and IX labels are lowercase `[a-z0-9-]`, 1–32 chars. | DID Core permits `:` inside the method-specific-id but treats `/` as a path separator, so the current form makes every Issuer and SP under one IX the *same DID*. Colons keep the routing information the spec clearly wants while staying a real DID. |
| **D3** | Digital Address | **ABNF:** `da = local "@" ix-name` · `local = 1*64(ALPHA / DIGIT / "." / "_" / "-")` · `ix-name = label *("." label)`. Compare case-insensitively, store lowercase, ASCII-only in 3.0. Reserve `admin`, `agd`, `ix`, `root`, `system`. | IX names are network-unique, so a DA is network-unique by construction — that dissolves the §3.21 (region) vs §6.5.1 (network) conflict rather than picking a side. Defer IDN to 3.1 with a stated rationale (homograph risk). |
| **D4** | Role-VC type registry | Five type strings: `ADI-AGD-VC` `ADI-IX-VC` `ADI-ISSUER-VC` `ADI-SP-VC` `ADI-USER-VC`. Five role tokens: `AGD` `IX` `ISSUER` `SP` `USER`. Delete `ADI NETWORK VC`. One table in §4; every other mention references it. | Currently five competing schemes. Uppercase-hyphenated matches the majority of existing `type` fields, so it is the smallest diff. |
| **D5** | OpenID4VCI | **Profile it.** Pin to a specific published version, adopt its Credential Offer and metadata shapes verbatim, add ADIA extensions under an `adia_` prefix, and publish a one-page delta table. Use `/.well-known/openid-credential-issuer`. | Existing wallet libraries then work unmodified. Every deviation in the current examples is a deviation from something implementers already have code for. |
| **D6** | VC format | **SD-JWT VC** (IETF OAuth WG). | The spec promises selective disclosure (§5.4, §9.1) and the flows can't deliver it with whole-VC transport. SD-JWT VC has `cnf` holder binding built in, uses the JWS framing §6.2 already describes, and pairs with Token Status List for revocation. Closes A-124, A-125, B-215 at once. |
| **D7** | Signature algorithms | **MTI:** `ES256` required, `EdDSA` (Ed25519) recommended. `RS256` not permitted for new signatures; verifiers MAY accept for 12 months. `kid` REQUIRED in every JOSE header. `alg: none` and all `HS*` MUST be rejected. | The metadata already says ES256; the examples say RS256. Pick the one the metadata already advertises. |
| **D8** | Assurance | Three distinct integer fields per NIST SP 800-63 Rev. 4: `ial`, `aal`, `fal`, each 1–3. Role VCs for AGD/IX/Issuer carry ceilings `max_ial`, `max_aal`. SP role VC carries floors `min_ial`, `min_aal`. Delete `authorized_max_assurance_level`. | The document conflates identity proofing (IAL) with authentication strength (AAL). An Issuer's ceiling and an SP's floor are different kinds of number. |
| **D9** | HIDA | **Optional per region; when used, keyed and canonicalised.** `HIDA = HMAC-SHA-256(K_region, canon(given_name) ‖ 0x1F ‖ canon(family_name) ‖ 0x1F ‖ dob_ISO8601 ‖ 0x1F ‖ national_id)`. `canon` = NFKC → casefold → strip whitespace and punctuation → transliterate to ASCII. Scope uniqueness to the region; drop cross-region matching. | An unsalted digest over {name, DOB, ID number} is enumerable offline. Without canonicalisation the same person hashes differently at different Interchanges, so global uniqueness silently fails anyway. A region-held key makes the registry useless to anyone without it. |
| **D10** | Vault discovery | Add a `service` entry to the **user's DIDdoc**: `{"id": "#vault", "type": "ADIVault", "serviceEndpoint": "https://…"}`. Issuer's vault stays in issuer metadata. User agent rule: own DIDdoc service first, issuer metadata as fallback. | One singular `credential_vault_endpoint` in issuer metadata cannot express a per-user choice. The DIDdoc is the one place every party can already resolve. |
| **D11** | Sole control of the vault key | See Part 3, B-206 for the full design. Summary: HSM-resident non-exportable key (FIPS 140-3 L3 recommended, L2 minimum); each signing operation requires a fresh WebAuthn assertion whose `challenge` is the SHA-256 of the exact payload to be signed, with `UV=1`; DAS verifies before the HSM signs; every operation appended to a hash-chained log. Claim **AAL2**, not AAL3. | This is what eIDAS remote-QSCD actually requires. Without it the accountability property is asserted, not constructed. AAL3 needs a hardware authenticator with verifier-impersonation resistance — a server-held key released after remote auth is not that, however well-guarded. |
| **D12** | Pairwise DIDs | **Withdraw from 3.0.** Delete the claim in §3.19 and §7.4.3; add a paragraph to Privacy Considerations stating that 3.0 credentials carry a stable subject identifier, that Interchanges see all transactions, and that pairwise identifiers are planned for a later revision. | No flow uses one and no example shows one. A privacy property the protocol doesn't implement is worse than an honest limitation. Doing it properly means per-verifier `cnf` keys in SD-JWT VC, which is real design work for 3.1. |

Once the TWG has accepted these (or substituted its own), Parts 2–5 are unblocked in full.

---

## Part 2 — Workstream A: data model and examples

### A-cluster 1 — One correct role VC, then copy it five times
**Closes:** A-101, A-102, A-103, A-104, A-105, A-106, A-107, A-109, A-110, A-112, A-113, A-126, plus D-407 once D4 is accepted.

Every role VC in B.2.7–B.2.11 has the same shape and most of the defects are the same three mistakes repeated. Fix the template once. Here is **B.2.8 (Interchange) corrected**, decoded form:

```json
{
  "header": {
    "alg": "ES256",
    "typ": "vc+sd-jwt",
    "kid": "did:adi:global:agd:8c019421-2920-410c-acfe-77d5c87b187c#key-1"
  },
  "payload": {
    "vct": "ADI-IX-VC",
    "iss": "did:adi:global:agd:8c019421-2920-410c-acfe-77d5c87b187c",
    "sub": "did:adi:r1:ix1:f6e18f71-4311-4e09-8bfc-9980a90e4be7",
    "iat": 1755648000,
    "exp": 1818806400,
    "status": {
      "status_list": { "idx": 412, "uri": "https://agd.adi.example/status/ix" }
    },
    "cnf": {
      "jwk": { "kty": "EC", "crv": "P-256", "x": "…", "y": "…", "kid": "key-1" }
    },
    "role": "IX",
    "digital_address": "interchange_admin@ix1",
    "id_doc": {
      "id": "did:adi:r1:ix1:f6e18f71-4311-4e09-8bfc-9980a90e4be7",
      "verificationMethod": [{
        "id": "#key-1", "type": "JsonWebKey2020",
        "controller": "did:adi:r1:ix1:f6e18f71-4311-4e09-8bfc-9980a90e4be7",
        "publicKeyJwk": { "kty": "EC", "crv": "P-256", "x": "…", "y": "…" }
      }],
      "service": [{ "id": "#das", "type": "ADIDAS", "serviceEndpoint": "https://ix1.r1.adi.example/das" }]
    },
    "information": {
      "legal_name": "Example Interchange Ltd",
      "legal_address": "…",
      "contact": { "email": "ops@ix1.example", "phone": "+1-…" }
    },
    "rights": {
      "authorized_to_issue": ["ADI-ISSUER-VC", "ADI-SP-VC", "ADI-USER-VC"],
      "max_ial": 3,
      "max_aal": 2
    }
  },
  "signature": "…"
}
```

The three invariants that were broken, stated once:

1. **`id_doc.id` MUST equal `sub`.** The DIDdoc carries the subject's key, never the issuer's. (A-102, A-104)
2. **`cnf.jwk` MUST equal `id_doc.verificationMethod[0].publicKeyJwk`.** The holder-binding key and the DIDdoc key are the same key. (new — required by D6)
3. **`rights.authorized_to_issue` MUST list every type this role enrols.** AGD: `["ADI-IX-VC"]`. IX: Issuer + SP + User. Issuer and SP: `[]` — they issue *subject* credentials, governed by `authorized_schemas`, not ADI role credentials. (A-105, A-106, A-107)

Then per example:

| Example | Change |
|---|---|
| B.2.7 AGD | `iss` = `sub` (self-signed). `kid` points into its own DIDdoc. `authorized_to_issue: ["ADI-IX-VC"]`. Fix `request_id` `aa2f772-…` → valid UUID. |
| B.2.8 IX | As above. `role: "IX"` — also change B.1.2's `role: "INTERCHANGE"` → `"IX"` so request and credential agree (A-101). |
| B.2.9 Issuer | `sub` gets its own UUID (currently shares `3b576f82…` with B.2.10 — A-110). `id_doc.id = sub`. `authorized_to_issue: []`; add `authorized_schemas: ["UniversityDegreeCredential"]`. DA → `issuer_admin@ix1`. |
| B.2.10 SP | Own UUID. `id_doc.id = sub`. Replace `authorized_max_assurance_level: []` with `min_ial: 2, min_aal: 2` (A-108, needs D8). DA → `sp_admin@ix1`. |
| B.2.11 User | `sub` is currently an *Issuer* path — replace with a User DID (A-109). `id_doc.id = sub`. DA `user2@ix1`, no all-caps placeholders. Drop the copy-pasted `email@issuer_1.com`. |
| B.2.2 / B.2.3 | UUID `7560e8400-e79n-…` → valid (A-113). |
| All 8 JWTs | `"type"` → `"typ"`; add `kid` (A-112). |

**Done when:** `adia_checks.py` A-101 through A-114 and A-126 pass. (A-107, A-108 need checks written — add them when you touch the file.)

### A-cluster 2 — The credential offer
**Closes:** A-116, A-119, A-121, A-122. Needs D5.

Replace B.2.2 with the OpenID4VCI shape exactly:

```json
{
  "credential_issuer": "https://issuer1.ix1.r1.adi.example",
  "credential_configuration_ids": ["UniversityDegreeCredential"],
  "grants": {
    "urn:ietf:params:oauth:grant-type:pre-authorized_code": {
      "pre-authorized_code": "adhjhdjajkdkhjhAJHK",
      "tx_code": { "input_mode": "numeric", "length": 6, "description": "Code shown at the registrar desk" }
    }
  },
  "adia_subject": "did:adi:r1:ix1:45bde61c-7da0-4f85-aed4-39d2d7508e99",
  "adia_offer_expires": 1755651600
}
```

Normative text for §9.2.3, replacing the sentence at "Using the user DID from the issue_vc token":

> The Issuer MUST bind `adia_subject` when the offer is created. On redemption the Issuer MUST verify that the `issue_vc_token` is signed by the key bound to `adia_subject`, and MUST reject the redemption otherwise. The subject of the issued credential MUST be `adia_subject`, never a value taken from the redeeming party. Offers MUST be single-use and MUST expire no later than `adia_offer_expires`, which SHOULD be within 10 minutes of creation.

Drop `batch_credential_endpoint` and `deferred_credential_endpoint` from B.3.1 (A-119); replace `example.com` throughout with `adi.example` (A-118).

### A-cluster 3 — The presentation request
**Closes:** A-123, B-217.

```json
{
  "aud": "did:adi:r1:ix1:sp-uuid",
  "nonce": "n-0S6_WzA2Mj",
  "state": "af0ifjsldkj",
  "exp": 1755648600,
  "schemas_accepted": ["US_Passport", "US_Driver_License"],
  "min_ial": 2,
  "min_aal": 2,
  "response_uri": "https://sp1.example/adia/present"
}
```

The VP the user agent returns MUST echo `nonce` and `aud`; the SP MUST reject any VP where either differs from what it issued, or where `exp` has passed. `state` correlates the redirect back to the SP's session (B-217).

### A-cluster 4 — The subject credential
**Closes:** A-124, A-125, B-209 (the data side). Needs D6.

Replace B.2.4 with an SD-JWT VC. Decoded payload:

```json
{
  "vct": "UniversityDegreeCredential",
  "iss": "did:adi:r1:ix3:eedec811-0f26-4656-a6cd-59d5f0bf2c16",
  "sub": "did:adi:r2:ix1:ebfeb1f7-12eb-4c6f-9c27-6e12ec21a4f3",
  "iat": 1755648000,
  "exp": 1818806400,
  "status": { "status_list": { "idx": 9021, "uri": "https://issuer1.example/status/degrees" } },
  "cnf": { "jwk": { "kty": "EC", "crv": "P-256", "x": "…", "y": "…" } },
  "_sd": ["<digest of degree.type>", "<digest of degree.name>", "<digest of graduation_date>"],
  "_sd_alg": "sha-256"
}
```

with the disclosures shown separately. §6.2's sentence "This document will be using JWT VC formatting in examples" becomes true (A-125). A-124's `vc_id` disappears — `jti` if an identifier is needed.

### A-cluster 5 — Everything else in A
| ID | Fix |
|---|---|
| A-115 | Review the B.1.5 placeholder values I substituted; replace with authored ones |
| A-117 | B.2.6: delete `deviceID`, `fingerPrint`, `environmentID`, `isLoginAuthorized`, `custom:userId`. Keep `iss`/`sub`/`aud`/`iat`/`exp`/`nonce` + the ADIA fields. `iss` must be a URI — `https://HOME@DAS1` is not one |
| A-120 | Add the `ADIVault` service entry to the user DIDdoc per D10; drop `credential_vault_endpoint` from B.3.1 or mark it as the *issuer* vault |
| A-114 | B.1.3 / B.1.4 get distinct `request_id`s |

---

## Part 3 — Workstream B: cryptography and protocol

### B-201 — Replace the verification paragraph in §6.2
Delete from "The verifier can check the signature by combining…" to "…signature of the proof." Replace with:

> Signatures on ADI credentials, presentations and requests are JSON Web Signatures [RFC 7515]. A verifier MUST validate a signature using the procedure in RFC 7515 §5.2: reconstruct the signing input as `BASE64URL(UTF8(protected header)) || '.' || BASE64URL(payload)`, select the algorithm from the `alg` header parameter, locate the key identified by `kid` in the signer's DIDdoc, and verify according to that algorithm. Verifiers MUST reject `alg` values not in §D7 and MUST reject any token whose `kid` does not resolve to a key in the signer's current DIDdoc.

### B-202, B-203 — Fix the user enrollment sequence in §8.5
The User Agent cannot issue the User's own role credential. Corrected message list (replace from `DAA -> USER_AGENT` through `Sign and create ADI Network User VC`):

```
USER        -> DAA           : Start enrollment
DAA         -> DAA           : Generate key pair; store private key in device keystore (FIDO)
DAA         -> IX_DAS        : POST ~ix/enroll_user  { public_key, hida?, enrollment_form }
IX_DAS      -> IX_DAS        : Check DA uniqueness; verify HIDA if region policy requires
IX_DAS      -> CI_AGENT      : Request identity proofing            (alt: only if IX outsources proofing)
CI_AGENT    -> IX_DAS        : Proofing result { ial }
IX_DAS      -> IX_DAS        : Provision cloud User Agent; create vault key in HSM (see B-206)
IX_DAS      -> IX_DAS        : Create DID and DIDdoc (binding both keys)
IX_DAS      -> IX_DAS        : Sign ADI-USER-VC with IX private key
IX_DAS      -> USER_AGENT    : Store ADI-USER-VC in user vault
IX_DAS      -> AGD           : Register DID in directory
IX_DAS      -> DAA           : Return DA, DID, ADI-USER-VC
```

Key generation now precedes DID creation (B-203). The Interchange signs the role credential (B-202). Redraw Figure 15 to match.

### B-204 — Reorder §5.4
Move the signing step out of "Proofing of Claims" and into "Issuing a Verifiable Credential" as the step **after** Holder approval:

1. Proofing — CI verifies claims. Output: verified claims, unsigned.
2. Offer — CI offers to issue.
3. Consent — Holder authenticates and approves.
4. **Sign and issue** — CI signs. This is the first moment a VC exists.
5. Store.

### B-206, B-207, B-208 — Sole control of the vault key (the D11 design)
New subsection §9.3.3.1 "Authorising a signing operation". Normative text:

> 1. The User's vault signing key MUST be generated inside and never leave a hardware security module meeting FIPS 140-3 Level 2 or higher; Level 3 is RECOMMENDED. The key MUST be marked non-exportable.
> 2. To authorise a signing operation on payload *P*, the Cloud User Agent MUST issue a WebAuthn authentication ceremony to the User's Device Application Agent with `challenge = SHA-256(P)` and `userVerification = "required"`.
> 3. The DAS MUST verify the returned assertion per WebAuthn §7.2 against the credential registered at enrollment, MUST confirm the `UV` flag is set, MUST confirm `clientDataJSON.challenge` equals `SHA-256(P)`, and MUST confirm the signature counter has increased.
> 4. Only after step 3 succeeds MAY the DAS request the HSM to sign *P*. The HSM MUST refuse signing requests not accompanied by a DAS attestation of a successful step 3.
> 5. The DAS MUST append a record `{timestamp, sub, SHA-256(P), assertion_hash, prev_hash}` to a hash-chained log for every signing operation, successful or refused. The log head MUST be published to the AGD daily.
> 6. Biometric matching occurs entirely within the authenticator. No biometric data, template or match score is transmitted. The protocol carries only the WebAuthn assertion.

Step 2 is what replaces "Request Biometric approval" in §10.1.3 (B-207). Step 1 is the floor for "hardened data vault" (B-208). Steps 2–4 are the binding B-206 asked for.

**B-205:** with this design, claim AAL2 in §7.2.3, §7.2.3 and §A.1.1. Remove AAL3.

### B-209 — Revocation and status
Every ADI credential (role and subject) carries a `status` claim referencing a **Token Status List** (IETF, companion to SD-JWT VC). Add §8.8 "Credential status":

> Issuers MUST publish a status list for every credential type they issue and MUST include a `status.status_list` reference in each credential. Verifiers MUST fetch the referenced list and MUST reject credentials whose status is `revoked` or `suspended`. Status lists MUST be signed by the issuer and MUST carry `exp` no more than 24 hours after `iat`. Role-credential revocation propagates: revoking an ADI-IX-VC invalidates every credential whose chain passes through that Interchange.

Root key rotation: the AGD publishes a new self-signed ADI-AGD-VC signed by **both** old and new keys for a 90-day overlap; verifiers MUST accept either during overlap. Add as §8.8.1.

### B-210 — The verification algorithm
New §10.3 "Presentation verification". This is the interoperability contract; write it as numbered normative steps:

> A verifier receiving a presentation *VP* for a request *R* MUST perform every step below in order and MUST reject on the first failure.
>
> 1. **Freshness.** `VP.nonce == R.nonce`, `VP.aud == R.aud`, current time < `R.exp`.
> 2. **Presentation signature.** Verify `VP` per §6.2 using the key in `VP.cnf` (SD-JWT KB-JWT).
> 3. **Credential signature.** For each credential *C* in *VP*, resolve `C.iss` to a DIDdoc via §10.2, locate `C.kid`, verify per §8.2.
> 4. **Holder binding.** `C.cnf.jwk` equals the key used in step 2.
> 5. **Credential status.** Fetch `C.status.status_list`; verify its signature; confirm *C*'s index is not revoked or suspended.
> 6. **Validity.** `C.iat` ≤ now < `C.exp`.
> 7. **Issuer role credential.** Obtain the issuer's ADI-ISSUER-VC (from the AGD directory or the DIDdoc). Apply steps 3, 5, 6 to it.
> 8. **Entitlement.** `C.vct` ∈ issuer-role-VC `rights.authorized_schemas`.
> 9. **Chain.** Repeat steps 3, 5, 6, 8 for the ADI-IX-VC that issued the ADI-ISSUER-VC (entitlement: `ADI-ISSUER-VC` ∈ `authorized_to_issue`), then for the ADI-AGD-VC that issued the ADI-IX-VC (entitlement: `ADI-IX-VC` ∈ `authorized_to_issue`).
> 10. **Root.** The ADI-AGD-VC `iss` equals its `sub` and its signing key matches the network trust anchor configured out of band.
> 11. **Assurance.** The `ial`/`aal` carried in *C* ≥ `R.min_ial`/`R.min_aal`, and ≤ the `max_ial`/`max_aal` of every role credential in the chain.
> 12. **Schema.** *C* validates against the JSON Schema registered for `C.vct` in §11.1.
>
> A verifier MAY cache the results of steps 7–10 for the lifetime of the shortest `status_list.exp` in the chain.

### B-211, B-212, B-213 — DIDdoc response, precedence, key IDs
Add B.3.5 `did_doc` response — the `id_doc` object from the role-VC template above, plus `"proof"` = JWS by the enrolling Interchange (or self, for the AGD). §10.2 precedence rule:

> When a public key appears in both a role credential's `id_doc` and a resolved DIDdoc, the **DIDdoc is authoritative**. A mismatch MUST be treated as a verification failure.

B-213: every JOSE header carries `kid` = `<DID>#<fragment>`; DIDdocs retain rotated-out keys in `verificationMethod` with a `revoked` timestamp so old signatures still verify.

### B-214 — Bind mTLS to the DID hierarchy
§7.2.2: *"DAS-to-DAS connections MUST use mutual TLS. The client certificate's `subjectAltName` MUST contain a `uniformResourceIdentifier` equal to the connecting party's DID. The receiving DAS MUST verify the DID resolves to a DIDdoc whose `verificationMethod` includes the certificate's public key. A mismatch MUST close the connection."* That makes the X.509 layer a transport for the DID identity instead of a second trust hierarchy.

### B-216, B-218, B-219 — Names
| Narrative says | Appendix says | Use |
|---|---|---|
| `vc_authorization_request` (§10.1.3) | `vc_authorization_token` (B.2.6) | Define both: the SP sends a `vc_request` (B.2.5); the user agent returns a `vc_authorization_token` to the vault. Delete the phrase `vc_authorization_request`. |
| `~issuer/issue_vc` | `~issuer/issue_vc_token` | `~issuer/issue_vc` |
| `make_credential_offer` (§9.2) | `make_vc_offer` (B.2.1) | `make_vc_offer` |
| `~ard/enroll_ix` | — | `~agd/enroll_ix` |

---

## Part 4 — Workstream C: normative structure

### C-301, C-302 — Make the requirements normative
Two mechanical passes over the prose (not the examples):

**Pass 1 — capitalise.** Every lowercase `must` / `shall` / `should` / `may` that expresses a requirement becomes `MUST` / `SHALL` / `SHOULD` / `MAY`. Every one that is merely descriptive ("a verifier may then choose…") gets rewritten to avoid the keyword ("a verifier can then choose…"). There are 25 to decide.

**Pass 2 — promote from NOTEs.** Each of these lives in an informative NOTE and must move into body text as a numbered requirement:

| Currently | Becomes |
|---|---|
| §3.1 Note 2 "An ADI Network must include at least one ADI-Region" | §6.4.1: "An ADI Network MUST include at least one Region." |
| §3.20 Note 2 "A DID must be bound to one and only one DIDdoc" | §7.4.3: "Each DID MUST resolve to exactly one DIDdoc." |
| §3.21 Note 2 "A DA must be unique within an ADI-Region" | §7.4.1: "A Digital Address MUST be unique across the network." (per D3) |
| §3.22 Note 3 "Agents must have at least one endpoint" | §7.2.2 |
| §6.1 "All participants … must generate a PK Pair" | §6.1, as a MUST |

Add to §1: *"Terms defined in §3 are informative. Requirements appear only in §8–§12 and Appendix B."*

### C-303 — Conformance clause
New §2 (shift the change log to an appendix). Template:

> ## 2. Conformance
> This specification defines requirements for five conformance targets: **AGD**, **Interchange**, **Credential Issuer**, **Service Provider**, and **User Agent**. An implementation conforms as a given target if it satisfies every MUST and MUST NOT requirement addressed to that target in §8–§12 and produces and accepts the messages in Appendix B for that target.
>
> An implementation MAY claim conformance to more than one target. Conformance to any target requires: (a) the mandatory-to-implement algorithms of §D7; (b) the verification procedure of §10.3 where the target verifies credentials; (c) publication of status lists per §8.8 where the target issues credentials.
>
> Requirements phrased with SHOULD and MAY do not affect conformance.

### C-304 — Security Considerations (outline)
Write one paragraph each; the review already identified the content:
1. Trust anchor distribution and root key compromise (B-209 rotation)
2. Interchange as a privileged party: what it can and cannot do with the vault key (B-206)
3. Replay of presentations — why `nonce`/`aud` are mandatory (A-123)
4. Offer interception — why the subject is bound at offer time (A-122)
5. Algorithm agility and downgrade (D7)
6. HIDA enumeration and why it is keyed (D9)
7. Homograph attacks on Digital Addresses — why ASCII-only in 3.0 (D3)
8. Directory poisoning — authorisation of directory writes (D-412)
9. mTLS/DID binding (B-214)

### C-305 — Privacy Considerations (outline)
1. Stable subject identifiers and verifier linkability (D12 — stated honestly)
2. Interchange visibility of transaction metadata (§6.3)
3. PII inside role credentials published to directories (D-413) — recommend: role credentials carry `legal_name` and a contact URI only; everything else moves to an encrypted enrollment record held by the enrolling party
4. Selective disclosure and what SD-JWT does and does not hide
5. HIDA as a correlation risk even when keyed
6. Retention and the right to erasure for signed artefacts
7. Biometric data never leaves the device (B-207 step 6)

### C-306 — Error model
One object, used by every endpoint in Appendix B:

```json
{ "error": "invalid_signature", "error_description": "kid did not resolve", "request_id": "…", "retry_after": 30 }
```

Registry of `error` codes: `invalid_request`, `invalid_signature`, `unknown_kid`, `expired`, `revoked`, `not_entitled`, `assurance_insufficient`, `schema_mismatch`, `duplicate`, `rate_limited`, `internal`. HTTP status mapping in a two-column table.

### C-307 — Versioning
Issuer/IX/AGD metadata gains `"adia_versions_supported": ["3.0"]`. Every request carries `"adia_version": "3.0"`. A party receiving an unsupported version returns `invalid_request` with `error_description` naming the versions it supports. Minor versions are additive only.

### C-308 — Registries
Three tables in a new Appendix D: role-VC types (D4), `vct` schema names (§9.1), error codes (C-306). Each with a registration rule ("TWG approval; specification required").

### C-309 — Write §8.2 (Enrolling an Interchange)
Mirror §8.3's structure exactly:

```
IX_APPLICANT -> AGD           : POST ~agd/enroll_ix  { public_key, key_id, da_user_name, da_region_name, enrollment_form }
AGD          -> AGD           : Vet applicant (governance policy)
AGD          -> AGD           : Create IX DID and DIDdoc (public_key from request)
AGD          -> AGD           : Sign ADI-IX-VC  (rights per D4/D8)
AGD          -> AGD_VAULT     : Store ADI-IX-VC
AGD          -> AGD           : Add IX to network directory
AGD          -> IX_APPLICANT  : Return DID, DIDdoc, ADI-IX-VC, directory URLs
IX_APPLICANT -> IX_DAS        : Provision DAS with credential and AGD endpoints
```

Prose: four short paragraphs matching the §8.3 pattern.

### C-310, C-311
Split Appendix C into **C.1 Normative** (RFC 2119, RFC 8174, RFC 7515, RFC 7517, RFC 7519, SD-JWT VC, Token Status List, OpenID4VCI, OpenID4VP, WebAuthn L3, DID Core, NIST SP 800-63-4, JSON Schema) and **C.2 Informative** (X.1254, X.1281, VCDM 2.0, eIDAS). Add `[W3C DM]` and `[W3C JS]` entries. Replace the RFC 2119/8174 Google Doc links with `https://www.rfc-editor.org/rfc/rfc2119` and `…/rfc8174`. Delete "To be completed". Copyright → 2026. Replace every "OASIS" with "ADIA".

---

## Part 5 — Workstream D: architecture consistency

Everything here is mechanical once Part 1 is accepted.

| ID | After decision | Do this |
|---|---|---|
| D-401 | D1 | Global rename of the 18 `ard_` fields and `~ard/`. Checker goes green when zero `ard_` remain. |
| D-402 | D8 | Replace `authorized_max_assurance_level` everywhere with `max_ial`/`max_aal` (issuers) or `min_ial`/`min_aal` (SPs). §3.14 → cite SP 800-63-4; define IAL, AAL, FAL separately. §7.2.3, §7.2.3, §11.2 → AAL2. |
| D-403 | D2 | Every `did:adi:…/…` → colon form. B.3.2's `issuser1/ix3/r1` → `did:adi:r1:ix3:<uuid>`. Add §9.5.3.1 with the ABNF and a one-paragraph resolution procedure (DAS of the named IX serves `GET ~ix/did/{uuid}`). |
| D-404 | D3 | ABNF into §9.5.1. Fix the four non-conforming DAs in B.2.7–B.2.11. Delete the region-scope sentence in §3.21. |
| D-405 | D9 | Rewrite §6.7.3 and §7.4.2 with the HMAC construction and canonicalisation steps. §3.11 Note 2 and §3.24 Note 1 → "when HIDA is in use". §8.5 "is verified" → "is verified where region policy requires". |
| D-406 | D12 | Delete pairwise sentences in §3.19 Note 3 and §9.5.3. Add the honest paragraph to Privacy Considerations. |
| D-407 | D4 | One table in §4.1. Replace every variant string. Delete "ADI NETWORK VC". Add ADI-SP-VC to §4.1. |
| D-408 | — | Pick one taxonomy: **Providers** = AGD, Interchange; **Members** = Issuer, SP, User. Fix §3.8, §6.2 ("Credential Provider" → "Credential Issuer"), §6.3 (add Interchange; "Authoritative Domain Controller" → "Authoritative Global Domain"), §9.2. |
| D-409 | — | DAA = **Device Application Agent** everywhere (§9.2's "Digital Address Application" is the outlier). |
| D-410 | — | §9.1: "Domain Authorities (AGs)" → "The AGD". |
| D-411 | — | Delete the list in §6.3; replace with "See §8.7.4." Keep §6.7.4's "at time of issuance" wording — it is the one that makes sense with status lists. |
| D-412 | — | §8.4: the **Interchange** publishes to the directory. Add to §9.4.1: "Only the enrolling Interchange MAY write a Member's directory entry; writes MUST be signed by the Interchange's DID key." |
| D-413 | C-305 §3 | Role credentials carry `legal_name` + contact URI only. Move the rest to an enrollment record. |
| D-414 | — | Acronym table in §4: AGD, AAL, CI, DA, DAA, DAS, DID, FAL, HIDA, IAL, IX, JWS, KYC, PII, SD-JWT, SP, VC, VP. |

---

## Working order

1. **TWG accepts Part 1** — one meeting, twelve yes/no/amend votes.
2. **D-401, D-403, D-404, D-407** — the four global renames, one commit each, checker confirms.
3. **A-cluster 1** — the role-VC template, then propagate.
4. **B-210** — the verification algorithm. Assign to whoever knows the crypto best; everything else references it.
5. **B-206 + B-209** — sole control and status, as a pair.
6. **C-301/302** — the normative-language pass, *after* the new sections exist so they get written correctly the first time.
7. **C-303/304/305** — conformance, security, privacy. These are summaries of decisions already made by this point.
8. Everything else in the register order.

Add a check to `adia_checks.py` every time you close something that didn't have one. Coverage starts at 64 of 105.
