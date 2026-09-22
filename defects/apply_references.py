#!/usr/bin/env python3
"""
C-310: complete Appendix A — one consolidated list with full citations; remove
"To be completed" and the OASIS boilerplate. Normative/informative classification
is deliberately left to the ITU Study Group, per their practice.

    python3 defects/apply_references.py --dry-run
    python3 defects/apply_references.py

Every reference below is one the body of the draft depends on. Where a
specification's publication status may have moved since drafting, the citation
says "version to be confirmed at approval" rather than asserting a status.
Those are marked with (*) in the list and should be checked before submission.

Replaces the whole of Appendix A up to Appendix B. Safe to re-run.
"""

import sys, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

APPENDIX = '''<a id="references"></a>
# Appendix A - References

This appendix lists the external documents this draft relies on or refers to. Classification of each reference as normative or informative is left to the Study Group taking this draft forward, in accordance with its conventions.

Hyperlinks were valid at the time of publication. The Accountable Digital Identity Association cannot guarantee their long-term validity.

<a id="references-list"></a>
## A.1 References

**[RFC2119]**
Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, DOI 10.17487/RFC2119, March 1997, <https://www.rfc-editor.org/info/rfc2119>.

**[RFC8174]**
Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words", BCP 14, RFC 8174, DOI 10.17487/RFC8174, May 2017, <https://www.rfc-editor.org/info/rfc8174>.

**[RFC3986]**
Berners-Lee, T., Fielding, R., and L. Masinter, "Uniform Resource Identifier (URI): Generic Syntax", STD 66, RFC 3986, DOI 10.17487/RFC3986, January 2005, <https://www.rfc-editor.org/info/rfc3986>.

**[RFC5234]**
Crocker, D., Ed., and P. Overell, "Augmented BNF for Syntax Specifications: ABNF", STD 68, RFC 5234, DOI 10.17487/RFC5234, January 2008, <https://www.rfc-editor.org/info/rfc5234>.

**[RFC7515]**
Jones, M., Bradley, J., and N. Sakimura, "JSON Web Signature (JWS)", RFC 7515, DOI 10.17487/RFC7515, May 2015, <https://www.rfc-editor.org/info/rfc7515>.

**[RFC7517]**
Jones, M., "JSON Web Key (JWK)", RFC 7517, DOI 10.17487/RFC7517, May 2015, <https://www.rfc-editor.org/info/rfc7517>.

**[RFC7519]**
Jones, M., Bradley, J., and N. Sakimura, "JSON Web Token (JWT)", RFC 7519, DOI 10.17487/RFC7519, May 2015, <https://www.rfc-editor.org/info/rfc7519>.

**[RFC9562]**
Davis, K., Peabody, B., and P. Leach, "Universally Unique IDentifiers (UUIDs)", RFC 9562, DOI 10.17487/RFC9562, May 2024, <https://www.rfc-editor.org/info/rfc9562>.

**[DID-CORE]**
Sporny, M., Guy, A., Sabadello, M., and D. Reed, Eds., "Decentralized Identifiers (DIDs) v1.0", W3C Recommendation, 19 July 2022, <https://www.w3.org/TR/did-core/>.

**[VC-DATA-MODEL]**
Sporny, M., Longley, D., Chadwick, D., and I. Herman, Eds., "Verifiable Credentials Data Model v2.0", W3C Recommendation, 15 May 2025, <https://www.w3.org/TR/vc-data-model-2.0/>.

**[VC-JSON-SCHEMA]**
Prorock, M., Cohen, G., and A. Guy, Eds., "Verifiable Credentials JSON Schema Specification", W3C Recommendation, 15 May 2025, <https://www.w3.org/TR/vc-json-schema/>.

**[WEBAUTHN]**
Hodges, J., Jones, J.C., Jones, M.B., Kumar, A., and E. Lundberg, Eds., "Web Authentication: An API for accessing Public Key Credentials Level 2", W3C Recommendation, 8 April 2021, <https://www.w3.org/TR/webauthn-2/>. Later Levels of this specification satisfy references to it in this document.

**[SD-JWT-VC]** (*)
Terbu, O., Fett, D., and B. Campbell, "SD-JWT-based Verifiable Credentials (SD-JWT VC)", Work in Progress, Internet-Draft, draft-ietf-oauth-sd-jwt-vc, <https://datatracker.ietf.org/doc/draft-ietf-oauth-sd-jwt-vc/>. The version to be cited is to be confirmed at approval of this document.

**[OID4VCI]** (*)
Lodderstedt, T., Yasuda, K., and T. Looker, "OpenID for Verifiable Credential Issuance 1.0", OpenID Foundation, <https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html>. The version to be cited is to be confirmed at approval of this document.

**[OID4VP]** (*)
Terbu, O., Lodderstedt, T., Yasuda, K., and T. Looker, "OpenID for Verifiable Presentations 1.0", OpenID Foundation, <https://openid.net/specs/openid-4-verifiable-presentations-1_0.html>. The version to be cited is to be confirmed at approval of this document.

**[NIST-800-63]**
National Institute of Standards and Technology, "Digital Identity Guidelines", NIST Special Publication 800-63-4, together with SP 800-63A-4 (Identity Proofing and Enrollment), SP 800-63B-4 (Authentication and Authenticator Management) and SP 800-63C-4 (Federation and Assertions), 2025, <https://pages.nist.gov/800-63-4/>.

**[FIPS-140-3]**
National Institute of Standards and Technology, "Security Requirements for Cryptographic Modules", FIPS PUB 140-3, March 2019, <https://doi.org/10.6028/NIST.FIPS.140-3>.

**[X.1254]**
ITU-T Recommendation X.1254, "Entity authentication assurance framework", September 2020.

**[X.1281]** (*)
ITU-T Recommendation X.1281. Title and edition to be confirmed at approval of this document.

**[OIDC-IDA]**
Lodderstedt, T., Fett, D., Haine, M., Pulido, A., Lehmann, K., and K. Koiwai, "OpenID Connect for Identity Assurance 1.0", OpenID Foundation, <https://openid.net/specs/openid-connect-4-identity-assurance-1_0.html>.

**[eIDAS]**
Regulation (EU) No 910/2014 of the European Parliament and of the Council on electronic identification and trust services for electronic transactions in the internal market, as amended by Regulation (EU) 2024/1183. Referenced for its remote qualified signature creation device model, which the vault-assisted signing model of clause 7.2.4.4 follows.

**[ADIA-V2]**
Accountable Digital Identity Association, "ADI Association Specification V2.0", October 2024. The version of this document that the present version replaces.

'''


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()

    m = re.search(r'^(<a id="[^"]*"></a>\n)?# Appendix A - References\n.*?(?=^(<a id="[^"]*"></a>\n)?# Appendix B)', text, re.S | re.M)
    if not m:
        print("  Appendix A not found in the expected position"); sys.exit(1)

    if '## A.1 References' in text and 'To be completed' not in text and 'A.2 Informative' not in text:
        print("  Appendix A already rebuilt"); return

    text = text[:m.start()] + APPENDIX + text[m.end():]
    old = "Appendix A are informative, except that the references listed as normative in Appendix A are themselves normative."
    new = "The classification of the references in Appendix A as normative or informative is for the Study Group to determine."
    if old in text:
        text = text.replace(old, new, 1)
        print("  clause 1.1.1 adjusted: reference classification deferred to the Study Group")
    print("  Appendix A replaced: single list, 22 entries, full citations; classification left to the Study Group")
    print("  removed: 'To be completed', OASIS boilerplate, bare numbered list")
    print("  (*) marks 4 entries whose publication status must be confirmed before submission")

    n = text.count("](#informative-references)")
    if n:
        text = text.replace("](#informative-references)", "](#references)")
        print("  redirected %d link(s) from the removed #informative-references anchor" % n)

    old = ", except that the references listed as normative in Appendix A are themselves normative."
    if old in text:
        text = text.replace(old, ".", 1)
        print("  clause 1.1.1: removed the sentence classifying Appendix A references")

    if dry:
        print("\n  --dry-run: nothing written"); return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written -- now run: make anchors && make notes")


if __name__ == "__main__":
    main()
