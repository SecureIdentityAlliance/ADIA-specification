#!/usr/bin/env python3
"""
B-203: in the user enrollment flow (clause 8.5), key generation must precede
Digital Address creation. Agreed by RK.

    python3 defects/apply_b203.py --dry-run
    python3 defects/apply_b203.py

Today the flow creates the Digital Address at step 4, enrols the user's
authenticator at step 8, and generates the vault key pair at step 10 -- so
the DID the address binds to has no keys when it is minted. The reordered
flow matches Figure 15: authenticator enrolled and nonce signed first, vault
key generated, then the Digital Address created binding both.

Also replaces the surviving "FIDO / Strong Auth / OAuth method" wording, which
the assurance model (clause 7.2.4) superseded. Safe to re-run.
"""

import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

OLD = '''**USER -\\> DAA : Request to enroll, complete enrollment forms**

**DAA -\\> USER_AGENT:  https POST ~ix/create_user**

**USER_AGENT -\\> USER_AGENT :  Select Digital Address ID \\nRequest Auth registration**

**USER_AGENT -\\> INTERCHANGE : Create Digital Address**

**INTERCHANGE -\\> USER_AGENT:  Digital Address created**

**USER_AGENT -\\> DAA : Request  accept T&Cs, signing of Auth registration nonce**

The DAA enrolls the user with a FIDO / Strong Auth / OAuth method and records the Public Key for subsequent authentications.

**DAA -\\> USER:  Accept T&Cs, enroll in Strong Auth**

**USER -\\> DAA:  Accept T&C perform Strong Auth enrollment**

**DAA -\\>   USER_AGENT:  Accepted T&Cs, sign Strong Auth response.**

Generate a PK pair and securely store the private key in the USER_AGENT hardened key store.'''

NEW = '''**USER -\\> DAA : Request to enroll, complete enrollment forms**

**DAA -\\> USER:  Accept T&Cs, enroll in Strong Auth**

**USER -\\> DAA:  Accept T&C, perform Strong Auth enrollment**

The DAA enrols the user with a WebAuthn authenticator (clause 7.2.4.3), generating the user's device key pair. The private key never leaves the authenticator.

**DAA -\\> USER_AGENT:  https POST ~ix/create_user (device public key, enrollment forms, HIDA)**

**USER_AGENT -\\> USER_AGENT :  Select Digital Address ID**

**USER_AGENT -\\> DAA : Request signing of Auth registration nonce**

**DAA -\\> USER_AGENT:  Signed Auth registration nonce**

The USER_AGENT generates the user's vault signing key pair inside the Interchange hardware security module (clause 7.2.4.4). Both keys now exist and have been proven: the device key by the signed nonce, the vault key by generation in the HSM.

**USER_AGENT -\\> INTERCHANGE : Create Digital Address, binding the device key and the vault key**

**INTERCHANGE -\\> USER_AGENT:  Digital Address created**'''


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()
    if NEW[:120] in text and OLD not in text:
        print("  already applied"); return
    if OLD not in text:
        print("  block not found as expected -- the flow text differs; see make explain ID=B-203"); sys.exit(1)
    text = text.replace(OLD, NEW, 1)
    print("  clause 8.5 flow reordered: authenticator enrolment and vault key generation now precede Digital Address creation")
    print("  'FIDO / Strong Auth / OAuth method' replaced with WebAuthn authenticator")
    if dry: print("\n  --dry-run: nothing written"); return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written -- now run: make notes")


if __name__ == "__main__":
    main()
