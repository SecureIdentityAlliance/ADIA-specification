# Assurance Model — AAL2 Single Tier

**Decision taken:** the AAL3 claim is withdrawn from v3.0. This document replaces the earlier two-tier draft and supersedes the B-205 and D-402 entries in `FIX_GUIDE_A-D.md`, together with decision **D8** in that guide's Part 1.

---

## 1. The position in one paragraph

Every ADI presentation is signed by a key held in the Interchange's hardware security module and released on the User's authenticated instruction. The claimant does not possess the signing key, so SP 800-63B-4's requirement that AAL3 be *"based on the proof of possession of a key through the use of a public-key cryptographic protocol"* cannot be met for the relationship that matters to a relying party. **v3.0 supports authentication up to AAL2 and federation up to FAL2.** Stating that plainly is stronger than claiming AAL3 and failing an assessment.

This is a floor, not a ceiling on the architecture. §7 records what a later revision would need in order to reach AAL3, and nothing here forecloses it.

---

## 2. What changes, relative to the current text

| | Current spec | v3.0 position |
|---|---|---|
| Authentication assurance | "AAL1, AAL2 & AAL3" | **AAL2 maximum** |
| Federation assurance | absent | **FAL2 maximum**, explicitly defined |
| Identity assurance | conflated with AAL | **IAL**, its own field |
| Authenticator | "FIDO, Passkeys and other methods … using OAuth2 and OpenID connect" | WebAuthn, multi-factor, `UV=1` |
| Synchronised passkeys | unaddressed | **Permitted** — they meet AAL2 |
| Attestation / AAGUID policy | absent | **Not required** at AAL2 |
| Reauthentication | absent | 12 hours, 30 minutes inactivity, one factor |

Two things get *easier* by dropping AAL3. Synchronised passkeys — iCloud Keychain, Google Password Manager — are acceptable at AAL2, so the specification no longer needs to distinguish them from device-bound credentials, and device support broadens. And no authenticator attestation or AAGUID allowlist is needed, which removes an operational burden from every Interchange.

One thing does not get easier: **the sole-control machinery in §7.2.4.4 is still required in full.** It is what makes the vault signature trustworthy at all. Withdrawing the AAL3 claim removes an overclaim about assurance; it does not remove the obligation to control the key properly.

---

## 3. Draft normative text

### 7.2.4 Authentication and federation assurance

> **Placement:** insert after the `#adi-user-wallet` anchor, as the last subsection of ADI-Network software components. Section numbers below are correct as of 18 Sep 2026; if the document is renumbered, the anchor is authoritative.

> **§7.2.4.1 Assurance levels conveyed**
>
> ADI Network participants record three assurance levels as distinct integer values, with the meanings given in [NIST SP 800-63-4]:
>
> - `ial` — identity assurance level, the rigour of identity proofing (SP 800-63A), range 1 to 3
> - `aal` — authentication assurance level, the strength of the authentication event (SP 800-63B), range 1 to 2
> - `fal` — federation assurance level, the strength of the assertion conveying that event to a relying party (SP 800-63C), range 1 to 2
>
> These MUST NOT be combined into a single value. Where any of the three is absent from a credential or presentation, a verifier MUST treat that level as unspecified and MUST NOT assume it satisfies any floor.
>
> **§7.2.4.2 Maximum assurance in this version**
>
> An ADI Network presentation is signed by a key held in an Interchange-operated hardware security module and released on the User's authenticated instruction under §7.2.4.4. The User does not hold the signing key.
>
> Accordingly, a participant MUST NOT assert `aal` above 2 or `fal` above 2 in this version of this specification. A verifier MUST reject any presentation asserting a higher value.
>
> NOTE: AAL3 requires the claimant to prove possession of an authenticator key through a public-key cryptographic protocol. A signature produced on the subscriber's behalf by a third party does not satisfy that requirement, however well the key is protected. Relying parties whose use case requires AAL3 or FAL3 are not served by this version.
>
> **§7.2.4.3 Authenticator requirements**
>
> To assert `aal: 2`, all of the following MUST hold:
>
> 1. The Device Application Agent uses a WebAuthn Level 2 or later authenticator registered with the Interchange at enrollment.
> 2. Two distinct authentication factors are proven at each ceremony. A multi-factor cryptographic authenticator reporting `UV = 1` satisfies this.
> 3. The Interchange verifies the assertion against the registered credential, confirms `UV = 1`, and confirms that the signature counter has increased where the authenticator provides one.
> 4. The User has re-authenticated with at least one factor within the preceding 12 hours, and within 30 minutes of the last account activity.
>
> Synchronised (multi-device) credentials MAY be used at `aal: 2`. Authenticator attestation is NOT REQUIRED at this level.
>
> An Interchange MUST NOT permit IP address allowlisting, possession of a bearer token, or a knowledge-only factor to serve as, or count towards, either factor. Assertion of authentication success conveyed over OAuth 2.0 or OpenID Connect does not by itself establish an authentication assurance level; the underlying ceremony determines the level.
>
> **§7.2.4.4 Control of the vault signing key**
>
> The following requirements are the basis on which a relying party may rely on a signature produced on the User's behalf:
>
> 1. The signing key MUST be generated inside, and MUST never leave, a hardware security module validated to FIPS 140-3 Level 2 or higher; Level 3 is RECOMMENDED. The key MUST be marked non-exportable.
> 2. To authorise a signing operation on payload *P*, the Cloud User Agent MUST obtain a WebAuthn assertion from the User's Device Application Agent with `challenge = SHA-256(P)` and `userVerification = "required"`.
> 3. The Digital Address Service MUST verify the assertion against the credential registered at enrollment, MUST confirm `UV = 1`, MUST confirm that `clientDataJSON.challenge` equals `SHA-256(P)`, and MUST confirm that the signature counter increased.
> 4. Only on success MAY the Digital Address Service request the HSM to sign *P*. The HSM MUST refuse any signing request not accompanied by an attestation of a successful verification under step 3.
> 5. The Digital Address Service MUST append a record `{timestamp, subject, SHA-256(P), assertion digest, previous record digest}` to a hash-chained log for every signing operation, whether it succeeded or was refused, and MUST publish the log head to the AGD daily.
>
> Binding the WebAuthn challenge to the hash of the exact payload is what prevents an Interchange from signing anything other than what the User approved.
>
> **§7.2.4.5 Biometric verification**
>
> Where biometric verification is used, it is performed entirely within the authenticator and is expressed to the ADI Network solely as `UV = 1` within a WebAuthn assertion. No biometric sample, template, or comparison score is transmitted to, stored by, or processed by any ADI Network participant.

---

## 4. Data model changes

Replace `authorized_max_assurance_level` everywhere.

**Provider role VCs** (AGD, Interchange, Issuer) — ceilings on what the holder may assert:

```json
"rights": {
  "authorized_to_issue": ["ADI-ISSUER-VC", "ADI-SP-VC", "ADI-USER-VC"],
  "max_ial": 3,
  "max_aal": 2,
  "max_fal": 2
}
```

**Service Provider role VC** — floors the holder requires:

```json
"rights": {
  "authorized_to_issue": [],
  "min_ial": 2,
  "min_aal": 2,
  "min_fal": 1
}
```

**Presentation request** (`vc_request`) carries `min_ial`, `min_aal`, `min_fal`.

**Presentation** carries the achieved levels:

```json
"ial": 2,
"aal": 2,
"fal": 2
```

No signing-tier field is needed — there is only one signing path.

**Verification algorithm (§10.3)**, step 11:

> 11. **Assurance.** `ial`, `aal` and `fal` in the presentation each meet or exceed the corresponding floor in the request, and each is less than or equal to the corresponding ceiling in every role credential in the chain. Reject any presentation asserting `aal` or `fal` above 2.

---

## 5. Prose to correct

| Location | Current | Replace with |
|---|---|---|
| §7.2.3 | "authenticates the user with a NIST 800-63 Assurance Level AAL1, AAL2 & AAL3, and conveys that level in ADI-Network transactions" | "authenticates the User at NIST SP 800-63 authentication assurance level 1 or 2 as determined by §7.2.4, and conveys the achieved `ial`, `aal` and `fal` values in ADI Network transactions" |
| §7.2.3 | "using strong authenticators capable of AAL1, AAL2 or AAL3 assurance levels" | "using authenticators meeting the requirements of §7.2.4.3" |
| §7.2.3 | "Examples include FIDO, Passkeys and other methods (biometrics) that have the ability to securely assert success using OAuth2 and OpenID connect" | "The DAA SHALL use a WebAuthn Level 2 or later authenticator. Synchronised passkeys are permitted. Assertion of authentication success over OAuth 2.0 or OpenID Connect does not by itself establish an assurance level." |
| §8.5 | "FIDO / Strong Auth / OAuth method" | "WebAuthn authenticator" |
| §9.2.3 | "Approval given - private key signed & AAL level used" | "Approval given — WebAuthn assertion verified (UV=1), payload signed" |
| §11.2 | "ADI enables authentication of NIST AAL levels 1, 2 & 3" | "ADI supports authentication at NIST AAL 1 and 2, and federation at FAL 1 and 2" |
| §7.2.2 | "may use additional authentication methods such as IP whitelists" | Keep for DAS-to-DAS transport, and add: "Network-layer controls MUST NOT be used as, or counted towards, User authentication factors." |
| §3.14 | Cites SP 800-63-3; describes IAL while the term is used loosely | Cite SP 800-63-4; give IAL, AAL and FAL three separate definition entries |

Every remaining mention of "AAL3" and "AAL 3" should be removed. `grep -n 'AAL' spec/adia_v3.md` finds them all.

---

## 6. Register impact

| ID | Disposition |
|---|---|
| **B-205** | Resolved by this document: AAL3 withdrawn, AAL2 stated with requirements |
| **B-206** | Still required in full — §7.2.4.4. The sole-control obligation does not go away with the AAL3 claim |
| **B-207** | Resolved: "biometric approval" becomes `UV=1` inside an assertion, §7.2.4.5 |
| **B-208** | Resolved: "hardened data vault" now means FIPS 140-3 Level 2 minimum, §7.2.4.4 item 1 |
| **D-402** | Three fields with stated ranges. Note that FAL was a **missing capability**, not only a naming problem |
| **A-108** | SP role VC gains `min_ial`, `min_aal`, `min_fal` |
| **B-220** | Rescoped: reauthentication still required, at AAL2 intervals — 12 hours, 30 minutes inactivity, one factor |
| **B-221** | **Superseded.** No signing-tier field is needed with a single signing path |

---

## 7. What a later revision would need for AAL3

Recorded so the decision stays deliberate rather than becoming accidental.

AAL3 requires the claimant to hold the key. That means a presentation's key-binding JWT must be signed by the Device Application Agent's own authenticator, with `cnf` bound to that key rather than to the vault key. With that one change the same architecture reaches AAL3 and FAL3, because proof of possession travels all the way to the relying party.

It would additionally require: WebAuthn origin verification at every ceremony; device-bound credentials only, with authenticator attestation checked against an AAGUID policy; and reauthentication at 12 hours and 15 minutes of inactivity using both factors.

Such a revision would most sensibly **add** a second tier rather than replace the vault path, since the vault path is what admits users whose devices cannot hold a credential store — the inclusion property the architecture exists to provide.
