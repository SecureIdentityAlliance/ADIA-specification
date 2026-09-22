# Authority in the DID Document — Design Paper

**Status: draft, pending RK's confirmation.** Not applied to the specification. This paper is the complete change, ready to apply the day the decision is confirmed, and it is recorded in the Editor's Notes as open decision D13 so the ITU contribution carries it honestly.

**The proposal in one sentence.** The information now carried in ADI-ROLE Verifiable Credentials — role, entitlements, assurance ceilings, public key — moves into the entity's DID Document, which is signed by the authority that enrolled the entity. The chain of trust is preserved; the artefact that carries it changes.

---

## 1. What is preserved and what moves

The accountability model in clause 6 rests on a chain: the AGD vouches for an Interchange, the Interchange vouches for an Issuer, the Issuer signs a credential. Nothing in this proposal changes that chain. It changes *where each link is written down*.

| | Today | Proposed |
|---|---|---|
| Artefact carrying authority | ADI-ROLE VC, one per entity | DID Document, one per entity |
| Signed by | The enrolling authority | The enrolling authority (as DID `controller`) |
| Public key location | `id_doc` embedded inside the role VC | `verificationMethod` in the DID Document |
| Entitlements | `rights` inside the role VC | `adi` extension property in the DID Document |
| Chain walk in verification | Resolve each role VC in turn | Resolve each DID Document in turn |
| Trust anchor | AGD's self-signed role VC | AGD's self-signed DID Document |
| Revocation | Role VC status list | DID Document deactivation |
| Discovery | Directory, or presented by the holder | DID resolution via the issuing Interchange's DAS |

The load-bearing observation: a role VC today *contains* a DID Document (`id_doc`). The proposal deletes the wrapper and signs the contents directly. It is a simplification, not an addition.

---

## 2. The DID Document

One shape for all five entity types, distinguished by `adi.role`. The `adi` property is a DID Core extension, declared through the `@context`.

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://adiassociation.org/ns/adi/v1"
  ],
  "id": "did:adi:r1:ix1:3b576f82-3506-4663-8ca4-51d614aea318",
  "controller": "did:adi:r1:ix1:f6e18f71-4311-4e09-8bfc-9980a90e4be7",
  "verificationMethod": [
    {
      "id": "did:adi:r1:ix1:3b576f82-3506-4663-8ca4-51d614aea318#key-1",
      "type": "JsonWebKey2020",
      "controller": "did:adi:r1:ix1:3b576f82-3506-4663-8ca4-51d614aea318",
      "publicKeyJwk": { "kty": "EC", "crv": "P-256", "x": "…", "y": "…" }
    }
  ],
  "assertionMethod": ["#key-1"],
  "authentication": ["#key-1"],
  "service": [
    { "id": "#agent", "type": "ADIAgent", "serviceEndpoint": "https://issuer1.ix1.example/agent" }
  ],
  "adi": {
    "role": "ISSUER",
    "digitalAddress": "issuer_admin@ix1",
    "enrolledBy": "did:adi:r1:ix1:f6e18f71-4311-4e09-8bfc-9980a90e4be7",
    "validFrom": "2026-09-22T00:00:00Z",
    "validUntil": "2028-09-22T00:00:00Z",
    "authorizedSchemas": ["UniversityDegreeCredential"],
    "maxIal": 3,
    "maxAal": 2,
    "maxFal": 2
  }
}
```

**Field rules by role.** `authorizedSchemas` appears on ISSUER only. `authorizedToEnrol` (values from `IX`, `ISSUER`, `SP`, `USER`) appears on AGD and IX. `minIal` / `minAal` / `minFal` appear on SP only, in place of the `max` ceilings. USER carries none of these; its DID Document exists to publish keys and the Digital Address.

**Controller.** The `controller` is the enrolling authority: the AGD for an Interchange, the Interchange for an Issuer, Service Provider or User. The AGD is its own controller. This is the DID Core term for "who may change this document", and it coincides exactly with "who vouches for this entity".

---

## 3. Who signs, and how

DID Core deliberately says nothing about how a DID Document is signed; that is left to the method. For `did:adi`, resolution returns the document **as the payload of a JWS signed by the controller**:

```
JWS header:  { "alg": "ES256", "typ": "did+jwt", "kid": "did:adi:global:agd:8c01…#key-1" }
JWS payload: { the DID Document above, plus "iat" and "exp" }
```

A resolver verifies the JWS against the controller's own DID Document — which it resolves the same way — until it reaches the AGD, whose document is self-signed and whose key is the configured trust anchor. That is the chain of trust, expressed as a chain of signed DID Documents.

This settles a question the draft has never answered (B-211, §3.20): *who signs a DIDDoc?* The controller does.

---

## 4. Verification algorithm, revised

Clause 10.3 as drafted walks a chain of role VCs. The revised procedure is shorter, because each step is the same operation:

> 1. **Freshness.** `VP.nonce == R.nonce`, `VP.aud == R.aud`, current time < `R.exp`.
> 2. **Presentation signature.** Verify per clause 6.2 against the key in `VP.cnf`.
> 3. **Credential signature.** Resolve `C.iss`; verify per clause 6.2 against the key identified by `C.kid`.
> 4. **Holder binding.** `C.cnf.jwk` equals the key used in step 2.
> 5. **Credential status.** Fetch `C.status`; confirm not revoked or suspended.
> 6. **Validity.** `C.iat` ≤ now < `C.exp`.
> 7. **Issuer authority.** In the resolved DID Document for `C.iss`: `adi.role == "ISSUER"`, `C.vct ∈ adi.authorizedSchemas`, now within `adi.validFrom … validUntil`, and the document is not deactivated.
> 8. **Chain.** Resolve `adi.enrolledBy`; confirm `adi.role == "IX"` and `"ISSUER" ∈ adi.authorizedToEnrol`, with the same validity and deactivation checks. Repeat for that document's `enrolledBy`; confirm `adi.role == "AGD"` and `"IX" ∈ adi.authorizedToEnrol`.
> 9. **Root.** The AGD document's `controller` equals its `id`, and its signing key matches the configured trust anchor.
> 10. **Assurance.** `C.ial/aal/fal` ≥ the request floors and ≤ the `max` ceilings of every document in the chain.
> 11. **Schema.** `C` validates against the JSON Schema registered for `C.vct`.
>
> A verifier MAY cache resolved DID Documents for the lifetime of their JWS `exp`.

Steps 7–9 replace the four separate role-VC steps of the current draft.

---

## 5. Enrollment flows, simplified

Today, enrolling an Issuer involves: submit request → vet → provision agent → `vc_offer` → applicant signs `issue_vc_token` → Interchange verifies → Interchange signs role VC → store → return. The offer/token round trip exists because the applicant must accept a credential being issued *to* it.

A DID Document is not issued to the applicant; it is published *about* the applicant by its controller. The applicant already supplied its public key in the enrollment request. So the flow becomes:

```
ISSUER  -> IX      : POST ~ix/enroll_issuer (public key, enrollment form)
IX      -> IX      : Vet applicant
IX      -> IX      : Provision CI Agent
IX      -> IX      : Construct DID Document (role, entitlements, key)
IX      -> IX      : Sign DID Document as controller
IX      -> DAS     : Publish; DID now resolves
IX      -> AGD     : Register DID in network directory
IX      -> ISSUER  : Return DID, signed DID Document
```

Three messages fewer, and `issue_vc_token` disappears from the role path entirely. It remains for *subject* credentials, where the holder genuinely must accept issuance.

Figures 12, 13, 14, 15 and their Flow Descriptions change accordingly.

---

## 6. Revocation

Withdrawing an entity's authority means deactivating its DID Document. The controller republishes with `"deactivated": true` in resolution metadata (DID Core §7.1.3) and a new `iat`; resolvers MUST honour it. Because every verification resolves the chain, deactivation propagates: deactivating an Interchange invalidates every Issuer it enrolled, without touching their documents.

This is simpler than role-VC status lists, and it reuses a DID Core mechanism. Subject credentials still need their own status mechanism (B-209 remains, scoped to credentials only).

Key rotation: the controller republishes with a new `verificationMethod`, retaining the old one marked with a `revoked` timestamp so past signatures still verify (B-213).

---

## 7. Trade-offs — stated so the decision is made with them in view

**Every verification requires resolution.** A role VC can be presented by its holder and verified offline against a cached root. A DID Document must be fetched from the issuing Interchange's DAS. Caching for the JWS `exp` window mitigates this, but a verifier with no network path to the Interchange cannot verify. For ADIA's architecture — where the Interchange is already a required party — this is a smaller cost than it would be elsewhere, but it should be stated in Security Considerations as an availability dependency.

**DID Core has no signature slot.** The JWS-wrapped resolution in §3 is method-specific. Off-the-shelf DID resolvers return a plain document and will not verify the signature; ADIA verifiers need a `did:adi`-aware resolver. This makes publishing the method specification (D-403) a prerequisite rather than a follow-on.

**Capability relationships do not carry entitlements.** DID Core's `capabilityInvocation` and `capabilityDelegation` name *which keys* may act, not *what the entity may do*. The `adi` property is a necessary extension; it cannot be expressed in DID Core vocabulary alone. Some in the DID community regard entitlement data in a DID Document as a misuse of the format. The counter-argument is that the document is already controller-signed and already the thing a verifier resolves, so it is the natural place.

**The Interchange becomes a stronger single point of trust.** It signs the document that grants every Issuer its authority, and it serves that document on every verification. Today it does the first but not the second. Security Considerations should say so.

---

## 8. Clause-by-clause impact

| Clause | Change |
|---|---|
| 3.20 DIDDoc | Rewrite: signed by its controller; carries verification methods and the `adi` extension; may be deactivated |
| 3.2, 3.3 | Delete references to ADI-[role] VC |
| 4.2 ADI-Role VCs | **Delete.** Replace with a table of `adi.role` values |
| 4.1 Acronyms | Remove role-VC entries if any; no change otherwise |
| 5.5.3 Roles | Rewrite: "Each entity's role and entitlements are recorded in its DID Document, signed by the authority that enrolled it" |
| 6.3 Roles and Authorities | Rewrite around signed DID Documents |
| 6.6 Chain of Trust | Rewrite: chain of controller-signed DID Documents; add the deactivation propagation rule |
| 6.7.1 ADI-ROLE VC Schemas | Replace with the DID Document schema |
| 6.7.4 Authority Entitlements | Rewrite: the `adi` property, field rules by role |
| 7.2.1 DAS | Add: publishes and serves DID Documents; honours deactivation |
| 7.4.3 DID Addressing | Add resolution returns a controller-signed JWS |
| 8.1–8.5 Enrollment | Remove `vc_offer`/`issue_vc_token` from the role path; "issue role VC" → "publish DID Document" |
| 10.2 Requesting a public key | Becomes DID resolution; define the response |
| 10.3 Verification | Replace with §4 above |
| B.2.7–B.2.11 | **Delete.** Replace with B.2.7 "DID Document" (one example per role, or one with a note on role-specific fields) |
| B.3.4 get_did_doc | Response is the JWS in §3 |
| Figures 5, 12–15 | Redraw |

Approximately 80 occurrences of role-VC terminology across 28 clauses.

---

## 9. Register impact

**Closed or made moot:** A-101, A-102, A-103, A-104, A-105, A-106, A-107, A-109, A-110 (the role-VC example defects — the examples are deleted), B-211 (DIDDoc response now defined), B-212 (one source of keys, no precedence question), D-407 and decision D4 (role-VC type naming — becomes a five-value enum).

**Rescoped:** B-209 (revocation — now credentials only; entity revocation is deactivation), B-213 (key rotation — via republished DID Document), D-403 and decision D2 (the method specification becomes a prerequisite, not a follow-on).

**New:** D13 (this decision), plus a Security Considerations item for the resolution availability dependency.

**Net effect on the outstanding count:** roughly 12 items close, 3 are rescoped, 2 open. The register gets smaller.

---

## 10. Recommendation on timing

Do not apply this before the ITU submission. Two reasons beyond RK's confirmation being pending:

The change touches 28 clauses and five figures. Applied under time pressure it will be applied unevenly, and a Study Group receiving a document that is half role-VC and half DID-Document will have a worse starting point than one receiving either consistently.

The decision is genuinely architectural and carries the trade-offs in §7. It deserves to be seen and agreed by the working group as a decision, not discovered as a fait accompli in the submitted text.

Record it as D13 in the Editor's Notes with this paper attached. If RK confirms before submission, add one sentence to the D13 entry saying the working group's architect has endorsed the direction and the change is scheduled. The Study Group then inherits a clear intent rather than a partial migration.
