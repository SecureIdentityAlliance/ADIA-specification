**ACCOUNTABLE DIGITAL IDENTITY ARCHITECTURE SPECIFICATION **

**Version 3.0**

**Committee Specification Draft 3**

**17 Sep 2026**

**This stage:**

Fourth draft in MD format

**Previous stage:**

Third draft in .docx format

**Latest stage:**

N/A

**Technical Committee**

SIA/ADIA Technical Working Group

**Chair:**

Alan Bachmann (<aabachmann@cvshealth.com>)

**Editor:**

Nathan Dent ([<u>nathan@adiassociation.org</u>](mailto:nathan@adiassociation.org))

**Material Changes:**

- Change ADIA to Accountable Digital Identity Architecture

**Additional artifacts:**

This document is one component of a Work Product that also includes:

- N/A

**Related work:**

This document replaces or supersedes:

- Accountable Digital Identity Association Specification Version 2.0

**Abstract:**

This document provides a reference model, concepts, terms, and protocols for an accountable digital identity system. 

**Status:**

This document is a draft document that has NOT yet been approved by the ADIA Technical Working Group (TWG). The level of approval is also listed above. Check the "Latest stage" location noted above for possible later revisions of this document.

**Key words:**

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 \[[RFC2119](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#bookmark=kix.dz6nownqsfba)\] and \[[RFC8174](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#bookmark=kix.e8fivmxekybu)\] when, and only when, they appear in all capitals, as shown here.

**Citation format:**

When referencing this document, the following citation format should be used:

**\[ADIA Specification-V3.0\]**

*Accountable Digital Identity Architecture and Specification – Version 3.0 Draft*

**Notices:**

Copyright © ADIA 2026. All Rights Reserved.

Distributed under the terms of the Accountable Digital Identity Architecture (ADIA). For complete copyright information please see the full Notices section in an Appendix below.

# 1. Introduction

All text is normative unless otherwise labeled.

The Accountable Digital Identity Architecture Network (“ADI-Network”) is a distributed identity system consisting of people, processes and technologies that together deliver global digital identity services for individuals.   

This document provides an overall perspective of the “ADI-Network” and introduces its fundamental concepts and terms. In addition, this document specifies protocols for onboarding Participants and for issuing and presenting Verifiable Credentials with the consent of the Participant. 

This document includes:

- a reference model for Accountable Digital Identity Networks (ADI Networks);

- concepts and terminology for describing ADI Networks;

- a framework for operations and management of an ADI-Network; and

- Protocols for issuing and presenting Verifiable Credentials.

# 2. Changes from earlier Versions

This document entirely replaces the previous Accountable Digital identity Architecture (ADIA) Specification dated October 15, 2024).

# 3. Definitions of terms

## 3.1 Accountable Digital Identity Network (ADI-Network)

> Ecosystem of people, processes and technologies for issuing, holding, controlling and dispensing Verifiable Credentials.
>
> NOTE 1 to entry: One or more ADI Networks may exist as distinct ecosystems that may or may not be interoperable.
>
> NOTE 2 to entry: An ADI-Network must include at least one ADI-Region.

## 3.2 ADI-Administrator (ADI-\[role\]-Admin) (“administrator”)

> Organization role that performs administrative and management functions for an ADI-Interchange Provider. 
>
> NOTE 1 to entry: Administrator services include but are not limited to reviewing and approving requests to enroll in the ADI-Network as a Credential Issuer or a Service Provider.
>
> NOTE 2 to entry: ADI-Network Providers must implement at least one administrator role. This includes CI-Admin, IX-Admin, SP-Admin, and AGD-Admin.
>
> Note 3 to entry: ADI-Administrators can be a person or a system.

## 3.3 ADI-Agent (ADI-\[role\]-Agent) (“agent”)

> Role that represents an entity in an ADI-Interchange 
>
> Note 1 to entry: Agents are primarily but not exclusively deployed and controlled by an ADI-Interchange.
>
> Note 2 to entry: An agent performs functions on behalf of the entity it represents. Each entity has an associated instance of an Agent which maintains its cryptographic keys, offers endpoint services, and maintains compliance with ADI-Network governance.
>
> Note 3 to entry: Agents include but are not restricted to SP-Agent, CI-Agent, User-Agent, and IX-Agent.
>
> Note 4 to entry: A User-Agent may include cloud-based wallet functions. A User App or Wallet App on the End User’s device interacts with the User-Agent in the ADI-Interchange. 

## 3.4 ADI-Credential Issuer (ADI-CI) (“Credential Issuer”)

> Organization that issues Verifiable Credentials to a Holder.
>
> Note 1 to entry: A Credential Issuer can ingest and assess evidence for Claims in various ways including physically in-person or remotely via electronic submission.
>
> Note 2 to entry: A Credential Issuer can be accredited by an authority such as an ADI-Governor.
>
> Note 3 to entry: A Credential Issuer may be assigned an Assurance Level based on its reputation or on a risk assessment of its proofing processes.

## 3.5 ADI-Governor  

> Organization or system that provides governance functions in an ADI-Network.
>
> Note 1 to entry: An ADI-Governor may have a global or regional authority.
>
> Note 2 to entry: An ADI-Region scope may have organizational, political, geographic or jurisdictional significance. ADI-Regions may overlap.  

## 3.6 ADI-Interchange (ADI-IX) (“Interchange”)

> Technology platform for providing ADI-Network services.
>
> Note 1 to entry: An ADI-Interchange includes multiple service subsystems that may be offered by the same or different Interchange Providers.
>
> Note 2 to entry: An ADI-Network must include at least one ADI-Interchange.
>
> Note 3 to entry: An ADI-Region must include at least one ADI-Interchange. 

## 3.7 ADI-Interchange Provider (ADI-IP) (“Interchange Provider”)

> Organization offering ADI-Interchange services within a region of an ADI-Network
>
> Note 1 to entry: Services include Agent services for Issuers, Service Providers and Holders.  
>
> Note 2 to entry: An ADI-IP may offer other value-added services, such as Identity Escrow, Vetting, and Payment Services (*future*).

## 3.8 ADI-Network Provider (ADI-NP) (“Provider”)

> Organization that administers and manages a Credential Issuer, a Service Provider or an Interchange.
>
> Note 1 to entry: ADI-NPs perform various roles. For example, a Verifier is a Service Provider role that can evaluate the Verifiable Credentials and Presentations.
>
> Note 2 to entry: The term Service Provider is not the same as an ADI-NP. It refers to an organization that provides business or consumer products or services to End Users (i.e., ADI-Network Users).

## 3.9 ADI-Network User (ADI-NU) (“User”)

> Individual that requests and uses one or more Verifiable Credentials
>
> Note 1 to entry: ADI-Network Users include Holders and Subjects.

## 3.10 ADI-Network Provider application form

> Form that ADI-Network Providers complete when applying to join an ADI-Network.
>
> Note 1 to entry:  A NEW-SP Form includes the information required to enroll a Service Provider; a NEW-CI Form includes the information required to enroll a Credential Issuer; A NEW-IX Form includes the information required to enroll an Interchange Provider.

## 3.11 ADI-Region (region)

> Virtual or physical scope or boundaries for the uniqueness of a Digital Address.
>
> Note 1 to entry: A region may include one or more ADI-Interchanges.  
>
> Note 2 to entry: Entities within an ADI-Region are unique when they do not have matching HIDAs.

## 3.12 ADI-Service Provider (ADI-SP) (“Service Provider”) (“SP”)

> Organization offering products and services to ADI-Network Users.
>
> Note 1 to entry: The terms Service Provider and Verifier are also referred to as a “relying party”.
>
> Note 2 to entry: The Service Provider, an enterprise that supplies goods and/or services to customers or clients, is not a synonym for a Verifier which is an SP role that evaluates Verifiable Credentials and Presentations for authenticity and sufficiency.

## 3.13 ADI-wallet (wallet)

> Secure mobile or desktop application designed to store, manage, and share personal information and Verifiable Credentials in digital format.
>
> Note 1 to entry: ADI-wallets, which represent a User in an ADI-Network, are also referred to as a User Agent.
>
> Note 2 to entry: A User-based Wallet can be dedicated to the ADI-Network or shared with external credential-based systems.
>
> Note 3 to entry: ADI-wallets may be fully deployed in a user device, as part of a cloud-based service, or as a hybrid that includes functions in both components.

## 3.14 Assurance Level

> Level of confidence in the binding between an entity and the presented evidence.
>
> Note 1 to entry: Identity assurance refers to the strength of the identity proofing process carried out by the Issuer.
>
> Note 2 to entry: Assurance levels are described in detail in NIST SP 800-63-3 and in ITU-T X.1254 (2020).

## 3.15 Authoritative Global Domain (ADI-AGD)

> System that provides the overall ADI-Network trust anchor and searchable directory of ADI-Providers.
>
> Note 1 to entry:  An AGD provides services as defined on this specification, it is administered and operated by a Legal Entity capable of contractually enforcing and managing the ADI-Network.

## 3.16 Claim

Assertion made about a Subject

> Note 1 to entry: Assertions can refer to a Subject’s basic identity (e.g. name and birth date) or to related information (e.g., certificates, licenses, qualifiers, eligibilities, permissions).
>
> Note 2 to entry: Claims can be formatted in various ways (e.g., JSON, JWT, or SD-JWT).  

## 3.17 Claim Evidence

> Information that validates a Claim.
>
> Note 1 to entry: Evidence can be provided in various forms including physical or electronic, depending on assurance requirements.

## 3.18 Credential

> Set of claims about an individual.
>
> Note 1 to entry: A credential is transformed into a Verifiable Credential by adding metadata and a Credential Issuer signature. 
>
> Note 2 to entry: The Claims in a credential can have different levels of assurance.

## 3.19 Decentralized Identifier (DID)

> Portable URI-based identifier associated with an entity.
>
> Note:  ADI uses DID address formatting and refers to a DID Document for the purpose of retrieving the public key.  ADI relies upon Role VCs which include the public key (DIDDoc) and is signed  by issuing authority and contains entitlement rights the holder has within the network.  Other DID features are not required.
>
> Note 1 to entry: An example of a DID is:  did:example:123456abcdef
>
> Note 2 to entry: A DID represents a private key whose public key is notarized in a DIDDoc which is bound to the DID.
>
> Note 3 to entry:  Every ADI-Network entity has a primary DID that includes its own cryptographic keys that can be used for digital signing and data encryption. ADI-Network entities may also have temporary, pairwise DIDs for session use. 

## 3.20 DIDDoc

> Document signed using the private key of the issuer.  
>
> Note 1 to entry: A DIDDoc contains the associated DID, the public key of the DID, the verification method(s) and optionally other metadata.
>
> Note 2 to entry: A DID must be bound to one and only one DIDDoc.
>
> Note 3 to entry: A DIDDoc may be packaged as a JWT VC.

## 3.21 Digital Address (DA)

> Human-friendly name assigned by the ADI-Interchange that enrolled the User or Provider.
>
> Note 1 to entry: The format of a User DA is user@interchange_name
>
> Note 2 to entry: A DA must be unique within an ADI-Region.
>
> Note 3 to entry: ADI-Network Providers can also be assigned a DA by their controlling entity.

## 3.22 Endpoint (agent endpoint) (\[Role]-Agent endpoint)

> URL that resolves to an ADI-Network service access point.
>
> Note 1 to entry: An “endpoint” or “agent endpoint” refers to any endpoint in the ADI-Network. A \[Role\]-Agent endpoint refers to an endpoint in an agent playing a specific role (e.g. IX-Agent endpoint refers to an endpoint in an Interchange Agent).   
>
> Note 2 to entry: An endpoint identifies the source or destination agents for a protocol exchange using OIDC or ADIA protocols. 
>
> Note 3 to entry: Agents must have at least one endpoint in order to communicate. 
>
> Note 4 to entry: Agent endpoints can only communicate with specified other endpoints.

## 3.23 Entity

> Anything referenceable in statements as an abstract or concrete noun.
>
> Note 1 to entry: Entities include but are not limited to people, organizations, physical things, documents, abstract concepts, fictional characters, and arbitrary text.
>
> Note 2 to entry: Entities perform roles in an ADI-Network if they have the ability to do so.
>
> Note 3 to entry: In an ADI-Network, the CI, SP, IX, AGD are provider-entities, and the Holder and Subject are user-entities.

## 3.24 Hash of (Subject) ID Attributes (HIDA)

> Cryptographic hash computed over a specified set of Claims about a Subject.
>
> Note 1 to entry: The HIDA is a key driver for performing lookup operations to ensure that no two entities have the same DA within an ADI-Region. HIDAs are used to ensure uniqueness among entities that are applying for a DID and/or DA. 
>
> Note 2 to entry: The ID attributes to be used for HIDA calculations are specified by regional policies.
>
> Note 3 to entry: Agents that compute a HIDA are typically those that have access to the specified ID attributes, either through data entry, a scan operation, or a connector to the system of record. 
>
> Note 4 to entry: ID attributes of a User or organizational entity such as the ADI-Network Governor (regional), an Issuer, or a SP.

## 3.25 Verifiable Credential (VC)

> Tamper-evident credential that has authorship that can be cryptographically verified.
>
> Note 1 to entry: A VC consists of metadata, one or more claims, and a signature.  See \[W3C DM\] for details.
>
> Note 2 to entry: A VC could represent the same information as a physical credential such as a birth certificate. Addition of metadata and a digital signature can make a VC more tamper-evident and trustworthy than their physical counterparts. 

## 3.26 VC Schema (credential schema)

> Data model for all or part of a credential or Verifiable Credential.
>
> Note 1 to entry: A schema may apply to all of or any portion of a VC. Multiple JSON schemas may describe a single VC, e.g., one schema for the Subject and another for related Claims.
>
> Note 2 to entry: A Credential Schema publishes the structure and contents of a Credential or Verifiable Credential.  See \[W3C JS\] W3C Verifiable Credentials JSON Schema Specification for more information.** **

## 3.27 VC Vault

> Secure encrypted data store for issued VCs and other confidential data.

# 4. Acronyms and abbreviations

## 4.1 ADI-Role VCs 

> All participants of the ADI-Network are vetted and issued an ADI-ROLE VC which defines their role and authority to transact in the network. Each ADI-ROLE VC is defined by a schema of the same name. 
>
> **ADI-AGD VC** ADI-ROLE VC of an AGD
>
> **ADI-INTERCHANGE VC** ADI-ROLE VC of an Interchange
>
> **ADI-ISSUER VC** ADI-ROLE VC of an authorized Issuer of User Credentials 
>
> **ADI-USER VC** ADI-ROLE VC of a Holder (which could also be the VC Subject)
>
> **ADI-Network VC** ADI-ROLE VC of an AGD & Interchange.  

## 4.2 Identifiers

> **SP_ID** Service Provider DID or DA
>
> **CI_ID** Credential Issuer ID or DA
>
> **IX_ID** Interchange DID or DA
>
> **User_ID** User DID or DA
>
> **AGD_ID** AGD DID or DA

# 5. Overview and Background

## 5.1 Digital transformation

> Many of today’s digital innovations are part of the global transformation towards a digital society. Various forms of automation, such as robotics, digital twins, driverless cars, smart cities, and digital money, are advancing rapidly. Smartphones enable very powerful personal applications that use artificial intelligence and promote mobile living. The ability to securely and reliably identify people, things, and objects has become a ubiquitous requirement for the digital world.   
>
> There is a general agreement among industry experts, standards bodies, governments, and global enterprises that addressing the need for verifiable, accountable digital identities is a priority. There is a strong conviction among experts that:

- Innovative approaches to digital identity are needed to align the digital world with the physical world

- User accountability is essential for a functioning society, but is currently inadequate in the digital world

- Digital identity ecosystems must facilitate and preserve personal privacy

- Checking a user’s digital identity and asserted credentials should be straightforward and also reduce fraud and friction in the physical world

- Support needs to be provided for the 20% of the global population that is without a digital identity today

> The purpose of any digital identity ecosystem is to orchestrate the issuance and disclosure of digital credentials in a way that provides issuer assurance and holder consent. The digital identity ecosystem must provide standard ways to:

- Express claims digitally and to compose credentials

- Validate (“proof”) the claims

- Structure and cryptographically sign credentials 

- Issue verifiable (i.e., signed) credentials upon consent from the Subject or Holder

- Store and transport issued credentials securely

- Disburse the issued credentials upon consent from the Subject or Holder

- Verify the credential signatures, check credential validity and correctness, and determine Issuer certification and reputation

> This document describes an architecture and ecosystem for Accountable Digital Identities (ADI). It defines a scalable digital identity framework that establishes trust and active accountability across all participants. This framework is based on emerging standards, and is designed to be open, interoperable, trustable across borders, and equitable across participants.

## 5.2 Identities, credentials and claims

Every individual has their own unique identity – it is the sum of everything that makes them who they are and differentiates them from everyone else. No two people are truly indistinguishable – they can never claim to have identical characteristics, features, capabilities, experiences and relationships (not even twins). A person’s identity (called a credential) is typically a set of facts (called claims) that together serve as a unique identifier.

Note: While other entities such as organizations, physical objects and information can be identified in a similar manner, this document addresses only identifiers for individuals. 

In the physical world, a person’s first identity is usually established by a group of trusted people. Parents choose a name, doctors record the birth details, and governments issue a formal birth certificate (which is a credential). The birth certificate can then be used to create extended identities for schools, employers, banks, medical facilities, and so on. Everything an individual does in life is tied to their identity, and that identity becomes the accountable party.

The number of claims needed to distinguish a person with a high probability can vary significantly. For example, a person’s name by itself is rarely enough to be a unique identity (there are lots of John Smith’s) whereas a name combined with a validated address, photo and birth certificate is usually sufficient.

People can prove who they are by personally presenting paper documents as evidence – for example, a driver’s license, a passport, or a birth certificate (these are classified as “trustworthy” credentials). These documents provide evidence of identity, and their authenticity can be “proofed” by human inspection. In the digital world, definitive proof of identity is not quite as easily demonstrated, and malicious actors can more easily masquerade as someone they are not.

Establishing an equivalent identity model for the digital world is a priority that spans industries and jurisdictions. The traditional approach to online identification has been an account – often using an email address as the account name – plus a password. Enterprises offering services or products usually offer their customers an account and then assume it can be adequately secured. However, accounts can be breached, and personal data can be compromised. Service providers may not know their customer or even whether the account holder is legitimate (or even human!). This security gap between physical and digital identities has led to an exponential increase in online fraud. It has also led to a rapid rise in misinformation and disinformation propagating through online social media.

## 5.3 Verifiable credentials

<span class="mark">A Credential is a set of one or more Claims about an entity. </span>

A structured <span class="mark">Credential includes metadata to describe Credential properties including but not limited to the issuer ID, the validity date and time, a representative image, verification material, status information, and so on. </span>

<span class="mark">A credential is said to be verifiable</span> when it contains tamper-evident Claims and cryptographic proof from the issuer<span class="mark">. Verifiable Credentials (VCs), illustrated in Figure 1, are defined by World Wide Web Consortium standards. VCs can (but do not have to) represent the same data as is contained in physical credentials such as a passport, and they can also represent data that have no physical equivalent, such as the ownership of a bank account.</span>

Claims are not restricted to fundamental identification characteristics and <span class="mark">can include, for example, digital employee ids, digital driver's licenses, and digital educational certificates.</span>

<img src="media/image1.png" style="width:2.67269in;height:1.95956in" />

*<span class="mark">Source: www.w3.org/TR/vc-data-model-2.0</span>*

<span class="mark">**Figure 1**: Verifiable Credential structure</span>

## 5.4 Accountable digital identity marketplace

A digital identity marketplace enables a customer (i.e., a person or organization that wants to buy a product or service) to supply evidence to a supplier (i.e., a person or organization that sells the product or service) so that the supplier can “know their customer” (i.e., is able to minimize the risk of fraud, theft, or illegal activities) before delivering the product or service.

In the digital marketplace customers and suppliers can be anywhere in the world, be subject to different laws, and operate across multiple time zones. Digital marketplaces are also subject to the network effect – the more consumers there are the more the suppliers want to participate, and vice versa.

Figure 2 provides an overview of how credentials about a Subject are created, processed, and distributed with the consent of the Holder. It illustrates the marketplace functions of creating and issuing VCs, controlling their presentation, and delivering them to approved destinations. 

<figure>
<img src="media/image2.png" style="width:5.13889in;height:2.42639in" alt="A diagram of a company Description automatically generated" />
<figcaption aria-hidden="true">A diagram of a company Description automatically generated</figcaption>
</figure>

**Figure 2**: Digital Credential Marketplace

The basic steps in the process are: 

**Proofing of Claims**

1.  A Subject (most often an individual) presents evidence for a set of Claims to a Credential Issuer (i.e., a person or organization that is authorized to examine and validate the Claim evidence). The Claims required, which vary by Credential type, are identified in a Credential Schema \[see W3C XXX\].    

2.  The Credential Issuer’s software assembles the Claims into a Credential and validates completeness against the Credential Schema. The package of Claims and Metadata is then signed using the Credential Issuer’s private key and becomes a VC.

**Issuing a Verifiable Credential**

1.  The Credential Issuer offers to issue the VC to the Holder via the Interchange to which they are connected; a Credential Issuer is enrolled with one and only one Interchange. 

2.  The Holder and Subject are most often the same entity, but this is not mandatory. 

3.  Upon receiving approval from the Holder, the Credential Issuer submits the VC to the Interchange where it is stored either in the interchange platform’s vault or, alternately, in the Holder’s Wallet. The Wallet may belong entirely to the Holder, be hosted by the platform, or be a hybrid of both.

4.  Once stored in the Vault or Wallet, the VC is considered to be issued and is available for use in accordance with applicable rules or policies.      

**Requesting a Verifiable Presentation **

1.  When a Holder requests a product or service from a Service Provider, it may be necessary to obtain information about the Holder. There can be multiple reasons for this, not the least of which are to (a) ensure the request is legal and (b) minimize the risk of payment default. 

2.  The Service Provider requests a Verifiable Presentation from the Holder via an Interchange and specifies the Credential Schema(s) and specific Claims that are to be presented.  

3.  The Holder assembles a VP by selecting VCs (and Claims within a VC) to be included in the VP. A VP is very similar to a VC except that the payload is one or more VCs, and the Holder signs the VP.

**Delivering a Verifiable Presentation **

Upon receiving the Holder’s consent, the Vault or Wallet delivers the requested VP via the Interchange.

The Service Provider serves as a Verifier for the VP, the VC(s) it contains, and ultimately accepts or rejects the Claims that have been presented. To verify the VP and its contents, the Verifier must

- Obtain the Public Key of the Holder to test the VP signature;

- Obtain the Public Key of the Issuer to test the VC signature; and

- Obtain the Credential Schema(s) for the presented VCs to ensure the VCs are complete and in the correct format.  

The SP makes a judgment call on the acceptability of the Holder (the prospective customer) based on the Claims received and the Assurance Levels of the VC, the Issuer and potentially the Holder.   

\*\*\*\*

## 5.5 Accountable digital identity reference model

### 5.5.1 The ADI Ecosystem

The Accountable Digital Identity (ADI) ecosystem includes all the entities in the ADI universe – participants, providers, users, systems and infrastructures. Figure 3 provides an illustration of this “big picture” perspective.

<img src="media/image3.png" style="width:6.5in;height:3in" />

Figure 3: The ADI ecosystem

### 5.5.2 Participants

Participants are organizations and individuals that either make use of the services offered by the ADI-Network or implement policies and practices. 

Participants can be Users, Providers (Credential or Business), or Governors:

1.  A User is a person that wants to obtain a physical or digital service (or product) from a Service Provider.  This is a very common consumer/supplier transaction – a purchase at a store or an online marketplace, for example. Users can be classified as Subjects or Holder.

2.  A Service Provider is an organization that can supply the product or service but may require information in order to complete the transaction. The information required ranges from simple proof of humanity to a significant set of personal information.

3.  A Credential Provider is an organization that can collect, validate, package and then issue the information that the Service Provider needs.

4.  A Governor is an organization that sponsors and oversees an ADI-Network including its component systems.     

Participants must be enrolled in the ADI-Network to use its services (i.e., to use or provide accountable digital identity information). Participants may be enrolled in the same or different regions. 

### 5.5.3 Roles

Roles are specific sets of related activities (i.e., processing functions) that participants or their proxies execute as part of their involvement in the ADI ecosystem.

The roles currently defined for the ADI ecosystem are:

1.  VC Wallet – A User connects to the ADI-Network via a Wallet role that can provide a VC Vault, VP functions, and VC disclosure control. The Wallet role can be deployed in the User’s device, in a User-provided cloud service, in an ADI interchange, or a hybrid configuration. The Wallet role interacts with the User on behalf of the ADI-Network.

2.  VC Verifier – A Service Provider connects to the ADI-Network via a VC Verifier role that can receive and verify the format of a VP and its source and authenticity. The VC Verifier functions can be deployed by the Service Provider or by the Service Provider Agent (or a combination of both). 

3.  VC Issuer – A Credential Provider connects to the ADI-Network via a VC Issuer role that can prepare and issue a VC based on validated Claims. The VC Issuer functions can be deployed by the Credential Provider or by the VC Issuer Agent (or a combination of both).

4.  AGD – An ADI-Network Governor connects to the ADI-Network via an Authoritative Domain Controller role that can establish management policies and controls at a global or regional level.    

Actors on an ADI-Network have an ADI-ROLE VC that defines:

- The role they have the authority to perform (AGD, Interchange, Credential Issuer, Service Provider and User)

- The authority that issued this ADI-ROLE VC

- The types of role VCs this role VC is allowed to issue

- The levels of VC assurance this role VC is allowed to issue

- The assurance level of the actor holding this role VC

- Confirmation and evidence that ADI policies have been applied

- Identity vetting performed to a specific assurance level

- PII (As required per policy, encrypted by issuer)

- Metadata for the actor & directory listing

- HIDA information 

- Digital Address 

Roles, Authorities, confirmations and evidence are defined in ADI-ROLE VCSchemas.

Governance is enforced with both contractual agreements and network policy configurations.

### 5.5.4 ADI-Network overview

An ADI-Network is governed by an "authoritative global domain" (AGD) which sets network policy and enrolls other network authorities who in turn enroll members of the network. A Digital Address can obtain, store and use Verifiable Credentials in the ADI-Network.

The Accountable Digital Identity Architecture is a decentralized interconnected network of networks consisting of an Authoritative Global Domain, Interchanges and their underlying hardware, software and network platform.

All entities within the architecture are represented by a Digital Address which is bound to a DID. Each DIDDoc contains the DID's public keys and metadata, used to verify the Digital Address holder's authorizations and digital signatures.

DID formats include network locations which enable global navigation and communication within the ADI-Network. See §9.5.3.

Every Digital Address holds exactly one ADI-ROLE VC, issued and signed by the ADI-Network authority that enrolled it. See §8.3.

Strong auth is required to authenticate the holder of a Digital Address. Using this authentication method an Interchange can establish remote authenticity and provide surrogate agent services to perform ADI functions and authorizations on behalf of the holder. See §9.3.2.

Digital Addresses are created, registered and maintained by a Digital Address Service (DAS). A DAS is a component internal to the AGD and to each Interchange; together they form the ADI-Network backbone. Each DAS enforces network governance rules, enrolls participants within its scope, and creates Digital Addresses on authorized instruction. See §9.3.

Once the Digital Address is created and bound with Strong Authentication, the user can request credentials from ADI-Network Issuers, such as educational institutions, employers, financial institutions, medical facilities, and government entities like the DMV and Passport Office.

Service Providers can trust a credential because verification comes directly from an ADI-vetted Issuer that is contractually obliged to perform identity vetting at a stated assurance level. How the network records and, where lawful, discloses transaction history is described in §8.

# 6. ADI-Network Accountability

All VCs and many ADI-Network protocol requests require Digital Signatures by the issuer or requestor. An ADI-Network User digitally signs a VP to approve use of a VC. Requesters may need to sign the request to prove authorization.

All ADI-Network transactions are logged by the Interchange and AGD in an audit log keyed by Digital Address or DID. Based on regional laws, and with proper legal order, transaction details and participants' information may be retrieved, and the Interchange can provide a Service Provider with the issuing information for a Digital Address. This is what brings accountability into the system: it may be leveraged under appropriate legal and governance frameworks across scopes, boundaries and borders.

## 6.1 Authorizations and signing

ADI uses public-key cryptography for authorization and signing to enforce accountability. All participants in an ADI-Network must generate a PK Pair using their agent which acts on their behalf. The agent must securely store the private key in a hardened data vault.

The public key is given to the ADI-Network authority enrolling the participant to be registered and used to verify the participant's digital signature.

## 6.2 ADI Verifiable Credentials

ADI uses W3C Verifiable Credentials signed by ADI Credential Issuers to enforce accountability.

All VCs contain an assurance level per ADI-Network policy. Users can present these VCs to Service Providers to prove their identity required to access a provider's service.

The VC attribute "issuer" is the DID of the ADI Issuer and the VC attribute "subject" is the DID of the ADI participant the VC is about, typically the User. The VC is signed by the issuer and that signature is included in the VC as proof.

The credential metadata describes the format of the VC and the definition of the proof(s) used. For example, using JWT format with ES256 algorithm the jwt signature is included as the proof.

Note: This document will be using JWT VC formatting in examples. Other formats may be used.

The verifier can check the signature by combining the metadata and claims sections to create a SHA256 hash. Using the public key from the issuers ADI DIDDoc, the signature is valid if the public key encryption of the hash matches the signature of the proof, using the specified encryption algorithm in the metadata

## 6.3 Roles and Authorities

Roles and authorities are defined as claims in an ADI-ROLE VC. Accountability and authority are cryptographically documented and enforced using public key cryptography and ADI-\[role\] VCs that define provider roles and authorities. Providers are defined in §8.4 and Members in §8.5.

![Figure 4: ADI Roles](media/image4.png)
Figure 4: ADI Roles

## 6.4 ADI-Network Providers

ADI-Network Providers offer ADI enrollment, transaction processing and directory services.

### 6.4.1 Authoritative Global Domain (AGD)

> The AGD is the root issuing authority of an ADI-Network. The AGD defines governance policies and requirements for all providers and members to follow. The AGD vets and onboards Interchanges.
>
> There is only one AGD in an ADI-Network.

### 6.4.2 Interchanges (IX)

> An interchange operates as an IdP within a region and offers ADI-Network connectivity and transaction services to ADI members. An Interchange may offer value added services for member connectivity, key management and secure document storage vaults, and provides the user wallet application through which Users access Interchange and ADI services.
>
> An Interchange vets and onboards Credential Issuers, Service Providers and Users to join the ADI-Network based on global and regional network policies.
>
> There may be more than one Interchange.

## 6.5 Members

Members enroll with an Interchange. Member uniqueness is enforced within an Interchange; the PII attributes that comprise the HIDA are described in Network Governance (§8.7.3).

### 6.5.1 Credential Issuers (CI)

> A Credential Issuer is a legal entity that issues VCs following ADI-Network vetting and governance processes.

### 6.5.2 Service Providers (SP)

> A Service Provider is a legal entity that requests and obtains VCs. In this document the Service Provider is the same as the role of the Relying Party and Verifier in OAuth, OIDC4VC and NIST specifications.

### 6.5.3 Users (User)

> A user is a real person that can be verified to a NIST assurance level and assigned one or more Verifiable Credentials (VCs).
>
> *Note: User definition may be extended to support any identifiable entity or object, provided that the entity or object is properly capable of identifying itself using asymmetric keys (public key / private key pairs)*

## 6.6 Chain of Trust

The root of signing trust begins at the AGD and extends to all participants and members of the ADI-Network.

Each ADI-ROLE is issued and signed by an ADI-Authority.  Role VCs designate which role VCs the holder has authority to issue and sign.

<img src="media/image5.png" style="width:6.5in;height:3.31944in" />

Figure 5: ADI Roles & Chain of Trust

## 6.7 Governance 

An ADI-Network is governed by the controlling authority of the AGD, the AGD-Provider. Governance is enforced with both contractual agreements and network policy configuration.

This specification aims to support flexible governance models that may stand alone,  join,  link or refer to each other, thereby allowing for a truly global identity ecosystem.

### 6.7.1 ADI-ROLE VC Schemas

VC governance rules may be defined in ADI-ROLE VC schema metadata.  

For example, an Interchange may issue an ADI-IX VC with authority to issue VCs up to a certain assurance level and be authorized to issue ADI-CI VCs but not ADI-SP VCs.  Other services may be offered such as vc_vault, identity_escrow, identity_broker, financial_services and other value-added services. 

Logic to process rules should be automated to work off of a configurable data set by network administrators.  The ADI DAS component is responsible for enforcing these rules based on configurable settings and verifiable attributes in ADI-ROLE VCs.

Roles, authorities, confirmations and evidence can be defined in ADI-ROLE VC schemas.

### 6.7.2 User VC Schemas

For user VC schemas, the AGD in conjunction with Interchanges, maintains a directory of schema definition and claims acceptable within the Network.  Interchanges and regions may maintain unique schemas to their jurisdiction.

Credential Issuers are vetted and required to perform identity verification to a certain assurance level, and to issue certain types of VC Schema.  Each VC issued contains an assurance level and may contain evidence and risk attributes.  All of which can be used to create and enforce ADI-Network policies.

### 6.7.3 HIDA

A HIDA is a hash of PII attributes to maintain privacy.   Which PII attributes are used to comprise a HIDA may vary.  

HIDA construction, management and usage rules are defined within a region scope.  For example, in a global ADI-Network that uses national identity to create a HIDA, the HIDA may be comprised of: Name,  Date of Birth & National ID card \#.  In an enterprise it may be defined as name and employee ID.  In a social or community ADI-Network it may be simply phone or email.

HIDA usage is implementation-specific and should be set by ADI-Provider governance policies.

### 6.7.4 Authority Entitlements

Authority to perform ADI-Network transactions are defined in ADI-ROLE VCs.  Role VCs are checked to see if the holder of the VC has the authority to issue a VC of a schema type.  An ADI-Issuer would have the authority to issue VCs to an ADI-Network User.

ADI-Role VCs may specify value added services the authority has rights to issue.  For example, an interchange may have the authority entitlement  to issue VCs to ADI-Network providers to offer valid added financial services & payment processing.  Vetting and contractual agreements are enforced when on-boarding third-party value-added service providers. 

Actors on an ADI-Network have an ADI-ROLE VC that defines:

- The role they have the authority to perform:

  - AGD, Interchange, Credential Issuer, Service Provider and User

- The authority that issued this ADI-ROLE VC

- The types of role VCs this role VC is allowed to issue

- The levels of VC assurance this role VC is  allowed to issue

- The assurance level of the VC subject at the time of issuance

- Confirmation and evidence that ADI policies have been applied

  - Identity vetting performed to a specific assurance level

- PII (As required per governance policy, encrypted by issuer)

- Metadata for the actor & directory listing

- HIDA information 

- Digital Address  

### 6.7.5 Users

ADI-Network User VCs must contain minimum information as required by ADI-Network governance policies. For example, participants may be required to be vetted to a certain level, and HIDA attributes may be collected from government, enterprise or financial KYC identities.  For lesser scope deployments minimum information may be an OTP via mobile or email, or other methods and information in between these scopes.

Note: User VCs may be delegated to other users.  For example, a health identity may be delegated  between family members or care providers to pick up prescriptions. 

# 7. ADI-Network Architecture

## 7.1 Overview

An ADI-Network consists of a collection of Interchanges that each service users, credential issuers and service providers.  Interchanges communicate with each other through their agents' published endpoints.  In this way users, credential issuers and service providers can transact throughout the global ADI-Network.

VCs are stored and retrieved from an Agents published VC Vault endpoint. This may vary, some credential issuers may require the VC be stored in the CI’s Vault, others may allow the VC to be stored in the User Vault.  The CI can define the location of the vault endpoints it allows in the CI metadata.

Domain Authorities (AGs) also publish agent endpoints to service ADI requests in their respective domains. See [<u>3.3 Roles & Authorities</u>](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#heading=h.bvasm53r31m) for a description of network participants.

Agents communicate network requests using endpoints, the red line in the figure 4.

Agent endpoint metadata is obtained from GET ~*participant*/metadata.

ADI-Network participant URLs can be obtained by calling the AGD with a DID or DA using ~agd/network_location.

*Implementation option:  user, issuer, service provider and interchange digital addresses may contain a suffix containing ADI region.  For example, [<u>issuer1@ix3.region</u>](mailto:issuer1@ix3.region)1  or the interchange id can be globally unique.*

## 7.2 ADI-Network software components

ADI-Network Providers: AGD, Interchanges are built using the following software components:

- Digital Address Service (DAS)

- ADI-Agents (AGD, Interchange, Issuer & Service Provider)

- User Wallet

  - ADI-Agent (Cloud) 

  - Digital Address Application (DAA) (User Device)

Note:  For AGD & Interchanges the user wallet is used for administrative and operational users.

### 7.2.1 Digital Address Service (DAS)

A **Digital Address Service** is the core of an ADI-Network.  The DAS is designed to register and manage Digital Addresses, DIDs, DIDdocs & ADI-ROLE VCs throughout the ADI-Network.  The DAS will enforce network governance policies for authority and usage of ADI-ROLE VCs, Network transactions and auditing.  Depending on the governance rules, a DAS component may require ADI-Network certification that it enforces programmatic policy rules as expected.

Each Network Provider runs DAS software within their environment

Each DAS is configured with the URL endpoint of the ADI AGD.  From there a directory of other endpoints (Interchanges) are available.  Every DAS speaks to other DAS endpoints to perform ADI-Network Transactions throughout the ADI Global Network.

The DAS records the public keys of Digital Addresses & DIDs, maintains Network Directories and may enforce HIDA uniqueness.

DAS functions include:

> Register Digital Addresses, DIDs & DIDdocs
>
> HIDA Registration and Verification
>
> Update ADI-Network Directories
>
> Issue ADI-ROLE VCs
>
> Digital signature validation services
>
> *Verify & manage authorities (schema check for approved rights) *

### 7.2.2 Agents

Agents act as surrogates within the ADI-Network and perform tasks on behalf of their respective owner.  Agents may create, use and manage cryptographic keys for their owner.   

Users are authenticated to their agents using strong authentication.

Entities authenticate using mutual TLS and may use additional authentication methods such as IP whitelists.

Agents listen on endpoints to support requests from their owner and ADI-Network requests from other network agents.

Agents process requests by calling their local DAS or other ADI-Network agents to perform network transactions.

Types of ADI-Agents:

- AGD

- Interchange

- Service Provider

- Issuer

- User

Once an owner is authenticated with its agent, the agent can perform ADI-Network transactions on behalf of the owner.

### 7.2.3 ADI User Wallet

The ADI wallet is a hybrid architecture consisting of a cloud User Agent hosted in the Interchange and a User Device Agent (native or web app) running on the user’s device.

This model is similar to the [<u>eIDAS Trust Service Providers</u>](https://ec.europa.eu/digital-single-market/en/trust-services) Digital Signature legal binding model.

This hybrid model enables improved user experience and secure key management.  

Users are in control of the VCs they hold.  With an ADI Wallet the user can obtain and present and securely store VCs.

An ADI wallet authenticates the user with a NIST 800-63 Assurance Level AAL1, AAL2 & AAL3, and conveys that level in ADI-Network transactions.

#### 7.2.3.1 Cloud User Agent 

The user agent creates, manages and uses cryptographic keys securely stored at the Interchange.  Using these keys the User Agent will coordinate with the interchange DAS  to sign and perform ADI-Network transactions on behalf of the User.  

The User Agent enrolls and authenticates the user with the Device Application Agent  using strong authenticators capable of AAL1, AAL2 or AAL3 assurance levels.

#### 7.2.3.2 Device Application Agent (DAA)

The DAA operates on a user’s device and performs strong authentication.  Examples include FIDO, Passkeys and other methods (biometrics) that have the ability to securely assert success using OAuth2 and OpenID connect.

The User Device Agent works in conjunction with the interchange provisioned user agent to perform user authentication and VC wallet functions on behalf of the User.  

## 7.3 ADI Provider Architecture

ADI-Network Providers (AGD, Interchange) each operate a local DAS to perform ADI-Network Transactions and one or more ADI-Agents to perform delegated tasks on behalf of the agent owner.  

The following defines a systems architecture and API endpoints for each provider role.

### 7.3.1 AGD provider architecture

The AGD maintains the master provider directory, which contains provider metadata, ADI-Network DID address and URL service endpoints.  AGD administrators access console settings with user agent / wallet authentication.  AGD keys are stored on the hardened vault.

<img src="media/image6.png" style="width:6.5in;height:4.04167in" />

Figure 6: Authoritative Global Domain

### 7.3.2 Interchange provider architecture

The interchange maintains keys and ADI-ROLE VCs for credential issuers, service providers and users.  Agents control these keys and act on behalf of their owner. These keys are stored in the hardened vault, as are ADI-ROLE VCs.

The interchange supports location & identifier resolutions and performs auditing of all transactions,

<img src="media/image7.png" style="width:6.5in;height:4.04167in" />Figure 7: Interchange Architecture

### 7.3.3 ADI-Network overall view

Interchanges and domain authorities (AGDs) all communicate directly using published endpoints in the ADI-Network directory.  The red line represents requests, typically OIDC / VC formatted, to issue and obtain VC, authorization and consent.

The Interchange offers a hybrid wallet service to ADI-Network Users, providers and interchange administrators.

<img src="media/image8.png" style="width:6.5in;height:3.33333in" />

Figure 8: ADI-Network

## 7.4 Identifiers

### 7.4.1 Digital Address

A **Digital Address i**s an identifier that is unique in an ADI-Network.   It has the form of username@interchange_name.  For example, alice@interchange_1.

All entities within the architecture are represented by a Digital Address which is bound to an ADI-Network DID and may be bound to one or more privacy preserving pairwise DIDs. DIDdocs contain the public key of the DID.   DIDs digitally sign using their private key and can be verified using the DIDDoc public key.

Each Digital Address is bound to one or more DIDs and is assigned an ADI-ROLE VC by an ADI issuing authority.

<img src="media/image9.png" style="width:6.5in;height:3.15278in" />

Figure 9: Digital Address

### 7.4.2 HIDA

Participant uniqueness can be globally or regionally enforced by creating a participant HIDA (Hashed ID Attributes) from required PII data.   The hashed PII data will produce a digital fingerprint that can be used to check for pre-existence of an identity to ensure uniqueness.

 HIDA usage is optional.  HIDA requirements should be specified in governance policies.  

See [<u>Governance HIDA</u>](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#heading=h.g7c9avwei6bl).

### 7.4.3 DID Addressing

All Digital Addresses have a primary DID and one or more pairwise DIDs.

DIDs are identifiers of a private key the DID owner securely holds.  The public key is available through the DID’s DIDDoc / VC in the ADI-Network.

DID addresses include network locations which enable global navigation and communication within the ADI-Network.  See figure 4.4.3 DID issuance & format.

An ADI-Network DID bound to the Digital Address and may have the format of -  did:adi:issuer_6/r1/ix6.

<img src="media/image10.png" style="width:6.5in;height:3.30556in" />

Figure 10. ADI-Network Addressing

# 8. Enrollment

## 8.1 Creating an AGD

The ADI Global Domain (AGD) serves as a root of trust for all participants in the ecosystem. The AGD ensures interoperability between Interchanges

Note: Create_agd does not have an authority_issuer since it is the root.  Implementations should provide administrative operator consoles to set up & configure the new AGD and create and store keys.

The following request and response descriptions are used during AGD enrollment.

- [<u>create_agd</u>](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#heading=h.hfgugc59964c)

<img src="media/image11.png" style="width:6.5in;height:4.98611in" />Figure 11. Creating an AGD

This flow is the first step to create an ADI-Network.  An AGD must be created, which contains the root signing key for all other ADI signed transactions.

Since this is the root, a DID for the AGD is created and the DIDDoc must be the public key of the AGD private key. The ADI-AGD ADI-ROLE VC is self-signed using the AGD DID.

The AGD posts a signed request to enroll to the AGD. The request includes the private key identifier and required information about the AGD. 

**AGD -\> AGD: POST ~agd/create_agd \n (self-signed by the AGD private key)**

The AGD will create, sign, store and return an ADI-AGD role VC.

**AGD -\> AGD:  Create and sign the ADI-AGD VC**

**AGD -\>** **AGD-VAULT:  Store the ADI-AGD VC**

**AGD -\> AGD: Update directory with \n AGD listing Information**

DIDDoc, endpoint location

**AGD -\> AGD: Return success**

The AGD can now issue ADI-AGD VCs 

## 8.2 Enrolling an Interchange 

The following request and response JSON objects are used during Interchange enrollment.

- [<u>enroll_ix</u>](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#heading=h.e4s937b5x8r8)

- [<u>vc_offer</u>](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#heading=h.c36eaqi0mzdk)

- [<u>issuance_token</u>](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#heading=h.4dmxauxtiwp0)

- [<u>ADI-IX role VC</u>](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#heading=h.flj1plkiyk8p)

<img src="media/image12.png" style="width:6.5in;height:3.36111in" />

Figure 12. Enrolling an Interchange

## 8.3 Enrolling an Issuer

The following request and response JSON objects are used during Issuer enrollment.

- [<u>enroll_issuer</u>](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#heading=h.sqxdeon7jrjh)

- [<u>vc_offer</u>](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#heading=h.c36eaqi0mzdk)

- [<u>issuance_token</u>](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#heading=h.4dmxauxtiwp0)

- [<u>ADI-ISSUER role VC</u>](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#heading=h.7s49za3wsph9)

Issuers are onboarded into the ADI Ecosystem by an Interchange. The process starts with the Interchange requiring the prospective Issuer to provide organizational information, a contact person for the organization and details to qualify the Issuer as a member in good business standing, financial status and criteria to meet the certification process established by the ADI Governance policies.

The governing body within the Interchange may approve or reject requests to enroll into the Interchange and the ADI ecosystem. Successful approval of an entity as an Issuer results in a Digital Address, DID (i.e. ISSUER_ID) and network VC being created. A VC is issued by the Interchange using information used to verify the Issuer. The VC may also enforce additional policies to ensure that the Issuer can issue Digital Addresses to Users or issue Verifiable Credentials with a certain Assurance Level. 

<img src="media/image13.png" style="width:6.5in;height:3.38889in" />

Figure 13. Enrolling an Issuer

The Issuer administration applies to the Interchange to join the ADI ecosystem as an Issuer. 

The Interchange should have an enrollment form the issuer can fill out and submit.

The Issuer submits an enrollment request to the interchange. The request includes required information about the issuer.   This request may be submitted via a web form at the Interchange or other method.

**ISSUER -\> INTERCHANGE: POST ~ix/enroll_issuer**

The Interchange will vet the Issuer information and execute a contract to join ADI.

Once vetting of the Issuer is completed, the Interchange provisions a CI_AGENT to perform ADI functions for the issuer. The CI_AGENT generates PK pairs, is assigned a DID & DIDDoc and OIDC endpoints & metadata using an issuer-selected domain / sub-domain.

**INTERCHANGE -\> INTERCHANGE:  Provision issuer agent, create keys, \n listing data & endpoints**

Once the CI_AGENT is created, the Interchange sends a vc_offer for an ADI-Issuer role VC to the CI_AGENT to accept and sign. 

**INTERCHANGE -\> CI_AGENT: POST ~CI_AGENT/vc_offer**

The CI_AGENT signs the offer with its private_key and returns an issue_vc_token.

**CI_AGENT -\> INTERCHANGE: Returns issue_vc_token**

The interchange creates and signs an ADI-ISSUER role VC for the issuer, stores it in the interchange vault, updates the AGD provider directory listing and returns the VC to the CI_Agent.

**INTERCHANGE -\> IX-VAULT:  POST ~ix_vault/ADI-ISSUER role VC **

**INTERCHANGE -\>  AGD:  List issuer in AGD provider directory**

**INTERCHANGE -\> CI_AGENT: Return ADI-ISSUER role VC**

**INTERCHANGE -\> ISSUER:   Notification of successful enrollment**

The issuer can now issue VCs to ADI participants.  

## 8.4 Enrolling a Service Provider

The following request and response JSON objects are used during Service Provider enrollment.

- [<u>Enroll_sp</u>](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#heading=h.dgy3qb3slgrx)

- [<u>vc_offer</u>](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#heading=h.c36eaqi0mzdk)

- [<u>issuance_token</u>](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#heading=h.4dmxauxtiwp0)

- [<u>ADI-SP role VC</u>](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#heading=h.u4e8qubh20j5)

Service Providers are onboarded into the ADI-Network by an Interchange. The process starts with the Interchange requiring the prospective Service Provider to provide organizational information, a contact person for the organization and details required to join the ADI-Network.

The Interchange will perform due diligence, information validation and contract execution per ADI-Network governance rules.

The governing body within Interchange may approve or reject requests to enroll onto the Interchange. Successful approval of a requesting entity as a Service Provider results in a Digital Address being assigned and an SP_DID & associated DID_DOC being created. 

The Interchange will also create an Agent for the Service Provider.  This Agent is the Service Provider's surrogate within the ADI-Network and will execute requests from the Service Provider and from the ADI-Network on behalf of the Service Provider. For example, a user is requesting a service that requires a VC of a certain type to access.  The Service Provider will request a VC with a schema type from their Agent endpoint. 

The SP Agent will list the Service Provider in the AGD Service Provider Directory.

The SP Agent is now ready to accept and process ADI-Network requests.

<img src="media/image14.png" style="width:6.5in;height:3.27778in" />

Figure 14. Enrolling a Service Provider

The service provider submits an enrollment request to the interchange. The request includes required information about the  service provider.   This request may be submitted via a web form at the Interchange or other method.

**SERVICE_PROVIDER -\> INTERCHANGE: POST ~ix/enroll_sp  **

The Interchange will vet the service provider information and execute a contract to join ADI.

Once vetting of the service provider is completed, the Interchange provisions an SP_AGENT to perform ADI functions for the  service provider. The SP_AGENT generates PK pairs,  is assigned a DID & DIDDoc and OIDC endpoints & metadata using a service provider selected domain / sub-domain.

**INTERCHANGE -\> INTERCHANGE:  Provision agent, create keys, \n listing data & endpoints**

Once the SP_AGENT setup  is completed,  the Interchange sends a vc_offer for an ADI-SP ROLE VC to the SP_AGENT to accept and sign.

**INTERCHANGE -\> SP_AGENT: POST ~sp_agent/vc_offer **

The SP_AGENT signs the offer with its private_key returns an issue_vc_token.

**SP_AGENT -\> INTERCHANGE: POST return issue_vc_token**

The interchange creates and signs an ADI-SP role VC for the service provider, stores it in the interchange vault, updates the AGD provider directory listing and returns the ADI-SP role VC to the SP agent.

**INTERCHANGE -\> IX-VAULT:  POST ~ix_vault/ADI-SP role VC **

**INTERCHANGE -\>  AGD:  List SERVICE_PROVIDER in AGD provider directory**

**INTERCHANGE -\> SP_AGENT: Return ADI-SP role VC**

**INTERCHANGE -\> SERVICE_PROVIDER:   Notification of successful enrollment**

The  service provider can now request VCs from ADI participants.  

## 8.5 Enrolling a user

~ix/[<u>enroll_user</u>](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#heading=h.wb30ofcvwe63)

User Enrollment

A user may enroll in an ADI-Network starting at either (1) an issuer who is authorized to do ADI-Network User identity verification, or (2) at an interchange who may themselves act as the ADI-Network User identity issuer or outsource this to an approved ADI-Network User identity issuer.

1.  Issuers may initiate User Digital Address enrollment, by inviting the user to receive a VC. In this case the Issuer validates and supplies necessary PII to meet ADI-Network governance requirements for uniqueness verification and User Identity validation.

2.  Users may initiate Digital Address registration with an Interchange directly.  In this case the Interchange will perform vetting and issuing procedures to meet Network governance requirements or use a partnered network Issuer to perform vetting procedures.

In both cases during the enrollment process:

- The User HIDA is verified for uniqueness, and an ADI-Network User VC is issued to the user for participation in the ADI ecosystem.

The user can now participate in the ADI-Network to:

- Receive additional VCs by complying with Identification validation processes from Issuers (§ 11.1 Verifiable Credential Issuance Protocols).

- Authorize requests from a Service Provider for a VC (See [<u>VC Presentation</u>](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#heading=h.rqh1pxmhaus7)).

- Authorize VC issuance offers to obtain a VC from Credential Issuers (See [<u>VC Issuance Protocols</u>](https://docs.google.com/document/d/1jwhmY0vXv1tI1v9RXlx-ELG7UQXTSF03IE-C-WqLIxM/edit#heading=h.iryjgqua2c71)).

Depending upon governance policies a user may enroll starting at an Issuer or an Interchange.

The following describes when a user enrolls at an Interchange.

<img src="media/image15.png" style="width:6.5in;height:3.38889in" />

Figure 15. Enrolling a User

The user uses the INTERCHANGE “wallet” web, mobile or computer DAA *(& associate cloud agent)*  to enroll with the INTERCHANGE.

**USER -\> DAA : Request to enroll, complete enrollment forms**

**DAA -\> USER_AGENT:  https POST ~ix/create_user**

**USER_AGENT -\> USER_AGENT :  Select Digital Address ID \nRequest Auth registration** 

**USER_AGENT -\> INTERCHANGE : Create Digital Address**

**INTERCHANGE -\> USER_AGENT:  Digital Address created**

**USER_AGENT -\> DAA : Request  accept T&Cs, signing of Auth registration nonce**

The DAA enrolls the user with a FIDO / Strong Auth / OAuth method and records the Public Key for subsequent authentications.

**DAA -\> USER:  Accept T&Cs, enroll in Strong Auth**

**USER -\> DAA:  Accept T&C perform Strong Auth enrollment**

**DAA -\>   USER_AGENT:  Accepted T&Cs, sign Strong Auth response.**

Generate a PK pair and securely store the private key in the user agent hardened key store.

The interchange will vet the user identity and issue an ADI-Network User VC to the user.  

**USER_AGENT -\> USER_AGENT :  Vet user and issue ADI-Network User VC **

**alt if an Issuer is used to issue the ADI-Network User VC**

The INTERCHANGE may require an Issuer perform an identity proofing at a certain level.  If required, the INTERCHANGE will validate the identity with a selected Credential Issuer.

**USER_AGENT -\> CI_AGENT :  Verify the ADI-Network User VC Identity**

**CI_AGENT -\> USER_AGENT:  Verified VC claims**

**end**

**USER_AGENT -\> USER_AGENT:  Sign and create ADI-Network User VC**

The INTERCHANGE responds with success 

**USER_AGENT -\> DAA:   Success **

**DAA -\> USER:   Success**

The User now has a DA, DAA & USER_AGENT *(wallet)* and may obtain and use VCs with ADI Credential Issuers and Service Providers.

# 9. Verifiable Credential Issuance Protocols

## 9.1 Schemas

A VC schema describes the claims a VC contains.  A government ID schema might contain gov ID#, name, address and date of birth, whereas a university diploma schema might contain name, graduation date and degree.   The VC name denotes the schema that was used.  A US-GOV-PASSPORT VC and US-DIPLOMA VC are VCs using their respective schemas.

ADI maintains a list of approved schemas that are commonly used within the ADI-Network.  This list expands as needed per ADI governance regulations.

ADI defines reserved VC schema protocols for ADI-Network roles.  These schemas are designed to convey accountability and authority.

User schemas are approved for use in the ADI-Network and stored in the ADI Schema directory.

## 9.2 Credential Issuer

Issuers may issue one or more Verifiable Credentials to a User who has a Digital Address. A VC contains user-related claims based on well-defined and ADI-approved credential schemas. 

VC Issuance begins with the issuer vetting and validating the user’s identity per ADI-Network governance rules for the VC Schema to be issued.

Once verified, the Issuer creates a make_credential_offer containing the VC information for the user to review and approve.

The issuer sends this make_credential_offer request to its agent for processing to obtain user approval to issue the VC.

The issuer agent saves the VC offer and requests the user’s agent to return a user signed issuance_token to demonstrate acceptance.  

The user agent signs an issuance_token request for the VC using the private key bound to the VC subject DID to prove they are the subject of the VC.

The user agent  sends the signed issuance_token back to the issuer agent, who will then sign,  Issue and store the VC in a secure VC Vault.  The credential issuer agent will send the VC or its metadata to the user agent.

### 9.2.1 High Level Flow

<img src="media/image16.png" style="width:6.5in;height:3.08333in" />

Figure 16. Issuing a VC - High-Level Flow

### 9.2.2 Detailed Flow

<img src="media/image17.png" style="width:6.5in;height:3.40278in" />

Figure 17. Issuing a VC - Detailed Flow

### 9.2.3 Flow Description

The user interacts with the issuer’s site to request a VC of a particular schema.  The credential issuer validates the user’s identity required to issue the VC.

**USER -\> ISSUER: Request VC\n Credential Issuer verifies user**

Once the user’s claims for the VC are verified, the credential issuer sends an ADI make_credential_offer request to its CI-Agent to make the offer to the user.  

This make_credential_offer request contains the VC claims, values and schema type to be used.  The issuer sends this request to its agent to fulfill.

**ISSUER -\> CI_AGENT: POST ~issuer/make_vc_offer**

The issuer agent creates a vc_offer containing a pre_authorized_code (OIDC4VCI).

The issuer agent creates a URI referring to this vc_offer.  This is returned as a link and can be used as a redirect, QR or notification action for the user agent to fulfill.

**CI_AGENT -\> USER_AGENT: return URI: ~user_agent/get_credential_offer/{offer_id} \n via URL Link, QR Code or Notification **

**USER_AGENT -\> CI_AGENT:  POST ~issuer/get_credential_offer/{offer_id}**

**CI_AGENT -\> USER_AGENT:  Return vc_offer**

The USER_AGENT will request consent and authorization from the User. Note: the nonce signed by the USER_AGENT may be the hash of the VC offer.

**USER_AGENT -\> USER: Request consent and signed approval**

**USER -\> USER_AGENT: Approval given - private key signed & AAL level used**

The USER_AGENT verifies the authentication and consent of the user and creates an issue_vc token  signed by the user as confirmation.  

The USER_AGENT sends the issue_vc token to the issuer agent’s endpoint to validate and issue the VC.

**USER_AGENT -\> CI_AGENT: POST ~issuer/issue_vc**

The issuer agent validates the user's signature of the issue_vc token and retrieves VC claims based on the pre_authorized_code.   Using the user DID from the issue_vc token for the VC subject, a VC is generated and signed with DID private key.  The issuer agent  stores the VC in the VC Vault specified by the credential issuer.  (NOTE based on the issuer metadata the VC may be stored at the issuer or user vault.  The issuer_vault endpoint will point to the location the issuer supports.)

**CI_AGENT -\> VAULT_AGENT: ~issuer\_ or user\_  vault/VC **

**CI_AGENT -\> USER_AGENT:  Return issued VC**

returns success and VC or metadata to the user

**USER_AGENT -\> USER_AGENT:  VC Issued**

**USER_AGENT -\> USER:  VC Issued**

**USER_AGENT -\> CI_AGENT: Success**

# 10. Verifiable Credential Presentation

## 10.1 Service Provider

The service provider may request a user for one or more claims about their identity.  This can be a single claim such as “over 18” or a set of claims such as in government, institutional and enterprise IDs.

Claims are contained in a VC.  Each VC is signed by an approved ADI credential issuer.   

When requesting a VC, the service provider must specify one or more schemas that are acceptable.

The SP agent requests the USER_AGENT <span class="mark">to provide one or more of an acceptable list of VCs</span>.  

The USER_AGENT will ask the user to select one or more VCs from their wallet (if there is more than one) to use for this request.  If the User has no acceptable VCs, then the user may be redirected to a Credential Issuer to obtain a suitable VC.

The USER_AGENT will then ask the user for consent to present this VC to the service provider, using Strong Auth.  The USER_AGENT will then take the VC to create and sign a VP with the users’ private key to demonstrate user consent. 

The VP is then returned as a response to the service provider request.

*Tech Note:*

*The User may be referenced by a User ID or a null if not known at the time of request.*

*If not known, the USER_AGENT will  supply the ID of the User when processing the request. Because the wallet was redirected there it can supply the user DID or DA during processing, therefore it is not required.*

### 10.1.1 High Level Flow

<img src="media/image18.png" style="width:6.5in;height:3.40278in" />

Figure 18. Requesting a VC - High-Level Flow

### 10.1.2 Detailed Flow

<img src="media/image19.png" style="width:6.5in;height:3.40278in" />Figure 19. Service Provider Requests a VC

### 10.1.3 Flow Description

1. The user requests a service from a service provider.  While interacting with a service provider site / service, the service provider may require a VC to verify the user's identity.  

**USER -\> SERVICE_PROVIDER: 1. Requests service**

2. The service provider requests its agent to obtain a VC from a list of acceptable list VC schemas. This *vc_request* is sent to the SP agents for fulfillment.

**SERVICE_PROVIDER -\> SP_AGENT: 2. POST ~service_provider/vc_request**

3. The SP_AGENT notifies the USER_AGENT authorize the request

The SP_AGENT creates a vc_authorization_request and constructs a URI, referencing the request, to be used as a link, redirect, QR code or USER_AGENT notification action for the USER_AGENT to fulfill.

**SP_AGENT -\> USER_AGENT: 3. POST ~user_agent/vc_request\n Redirect, Link, QR Code or App Notification**

4. The USER_AGENT selects an acceptable VC from the user’s VCs.  If there are more than one the user is requested to select one.  If there are no VCs that match the request, the user may be directed to an Issuer to obtain an acceptable VC. 

The USER_AGENT obtains user consent & authorization using strong authentication.

**USER_AGENT -\> USER: 4. Select VC to use & Authorize use**

**USER -\> USER_AGENT: VC selected & confirm consent**

**USER_AGENT -\> USER:  Request Biometric approval**

**USER -\> USER_AGENT: Biometric approval given**

5. The USER_AGENT creates a user signed authorization_token and sends the request to the VAULT_AGENT endpoint to retrieve the VC.

This may be from the issuer vault or the user vault depending on issuer endpoint setting rules for this.

**USER_AGENT -\> VAULT_AGENT: 5. POST ~vc_vault/vc_authorization_token **

6. The VAULT_AGENT verifies the authorization_token, retrieves and returns the VC

**VAULT_AGENT -\> USER_AGENT: 6. Return the VC requested**

7. The USER_AGENT signs the VC with the users’ private key to create a VP. 

**USER_AGENT -\> USER_AGENT: 7. Create and sign VP**

8. The USER_AGENT sends the VP to the SP agent.

**USER_AGENT -\> SP_AGENT: 8. Respond to SP Agent with VP**

9.  The SP agent responds to the original request for a VC from the service provider.

**SP_AGENT -\> SERVICE_PROVIDER: 9. Success: Respond VP to Request for VC**

10.  The USER_AGENT informs the user that the VC has been presented to the service provider

**USER_AGENT -\> USER: 10. <span class="mark">VC presented to SP</span>**

## 10.2 Requesting a public key

Keys may be obtained in the ADI-ROLE VC / DIDDoc based upon  the subject DID (subject of VC).

Service Providers need to be assured that the VC was properly issued and signed by an ADI Credential Issuer and that the VP was signed by the ADI-Network User to show proof of ownership.

They may rely on their Agent to perform this task for them, or they may check the digital signatures themselves by requesting the DIDDoc public key of the signer. 

VC issuers and subjects can be validated  by using their VC DID to request their public key.  With the public key the VP (user) & VC (Issuer) signatures can each be validated using the VC proof cryptographic algorithms specified in the VC metadata header. 

To request the DIDDoc, the service provider calls get_did_doc.

<img src="media/image20.png" style="width:6.5in;height:3.94444in" />Figure 20. Service Provider Requests a DID Document

The Service Provider asks its SP Agent for the DIDDoc public key of the signer, by a get_did_doc request containing the DID requested.

**SERVICE_PROVIDER -\> SP_AGENT: POST ~service_provider/get_did_doc**

The Agent will return the  DID_DOC

**SP_AGENT -\> SERVICE_PROVIDER:   DIDDoc Public Key**

The agent can now verify the signature of the signer, using the Public Key from the  DIDDoc & cryptography signature algorithm listed.

# 11. Additional Use Cases

The following are additional use cases that can be enabled in an ADI-Network.

## 11.1 Financial Services

ADI can be used to identify and authenticate shoppers conducting payment transactions.  Payment processing services offered by service providers to accept and receive payments can be enhanced with accountable identity and superior payer/payee authentication offered by ADI.  VC architecture proposed by ADI can include credit and debit tokens representing payment account ownership connected to a user's identity in a cloud or hybrid wallet.

Financial service offerings may include such enhanced VCs that are further extended to represent user’s financial information such as credit ability & ratings, financial status, other connected wallets, and more.  

## 11.2 Authentication

ADI enables authentication of NIST AAL levels 1, 2 & 3.  Interchanges may offer technologies capable of tailored authentication such as user biometrics and notarized verification.

Details of integration with these technologies are technology implementation specific but must be approved by regional and global domain authorities for use within an ADI-Network.

ADI can be used for authentication to login or approve transactions by a service provider.   For example, login to financial services, approving payments and funds transfers or log into or consent to any service or transaction,

## 11.3 Identity Escrow

Service providers may not want to hold sensitive PII, instead just relying on ADI assurance that the PII meets certain criteria required for a service.  The actual PII can be escrowed by an Interchange and retrieved as needed by a service provider in the case of disputes or fraud.

# Appendix A - References

This appendix contains the informative references that are used in this document.
While any hyperlinks included in this appendix were valid at the time of publication, OASIS cannot guarantee their long-term validity.
## C.1 Informative References
The following referenced documents are not required for the application of this document but may assist the reader with regard to a particular subject area.
**[RFC2119]**
Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", BCP 14, RFC 2119, DOI 10.17487/RFC2119, March 1997, <<https://www.rfc-editor.org/info/rfc2119>>.
**[RFC8174]**
Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words", BCP 14, RFC 8174, DOI 10.17487/RFC8174, May 2017, <<https://www.rfc-editor.org/info/rfc8174>>.
**To be completed - which references are normative is for further study.**
This document is based on and makes use of the following external standards:
1. W3C Verifiable Credentials Data Model V2.0 
2. W3C Verifiable Credentials JSON Schema Specification
3. ITU-T X.1254
4. ITU-T X.1281
5. OpenID for Verifiable Credential Issuance
6. OpenID for Verifiable Presentations
7. OpenID Identity Assurance schema definition 1.0
8. IETF SD-JWT-based Verifiable Credentials (SD-JWT VC)
9. NIST SP 800-63

# Appendix B - Schemas

## B.1 Enrollment

### B.1.1 create_agd

JWT create request is signed by the AGD private key, validated by the public key in the enroll request.

POST ~agd/create_agd

```json
{
  "header": {
    "alg": "RS256",
    "type": "JWT"
  },
  "payload": {
    "request_id": "45bde61c-7da0-4f85-aed4-39d2d7508e99",
    "action": "CREATE",
    "role": "AGD",
    "ard_da_user_name": "agd_admin",
    "ard_da_global_name": "global_1",
    "agd_key_id": "cee86113-7989-4f04-b368-ab3127ccd51d",
    "agd_public_key": {
      "kty": "RSA",
      "n": "j503kLmfDyyKNxrEjbWjAoZaGxGzO-0CKQsedoJHqr0aREu-KgKmgJK9McFAH-ZiNj9yc-SZVSi_wEYfEZYvB7iZwKy86bTotN9ZF4dA2iPuJCYpOC1xMo87kVv45Xjb9SURXcmpuUmPf4PN4ZdT07JRs41f126YUfePqvxDhzoX5q0to1OEBszsjZUKGjvKb7rdSOYqmuEmdfI2PlGBl6vq4nbIV_zxCAseN-CYUWKR3sylJX3Mg9N5V0W-WcOEvaNHumu73gIEjS8HhJmtZ636gXY3ePhzDeo2Mxurj902WZR3QFjrqSPp2-_OBalxxvdLOP-JMBRNEoNjjV5nRQ",
      "e": "AQAB"
    },
    "agd_enrollment_form": {
      "legal_name": "ADI Entity legal name",
      "address": "legal address",
      "email": "email@aglobal_1_domain.com",
      "phone": "+1-650-555-1212",
      "license_id": "ADI-Lic#9348145"
    },
    "url": "https://adi.global_1_domain.com"
  },
  "signature": "hbGciOiJSUzI...1NObTjhad8d8adjadnap1c2VySWQiOiJhMS"
}
```

### B.1.2 enroll_ix

JWT create request is signed by the interchange private key, validated by the public key in the enroll request.

POST ~ard/enroll_ix

```json
{
  "header": {
    "alg": "RS256",
    "type": "JWT"
  },
  "payload": {
    "request_id": "a523335a-df3b-41cc-b371-88034beb1e5c",
    "action": "ENROLL",
    "role": "INTERCHANGE",
    "ard_da_user_name": "interchange_admin",
    "ard_da_region_name": "ix_1",
    "ard_key_id": "f6e18f71-4311-4e09-8bfc-9980a90e4be7",
    "ard_public_key": {
      "kty": "RSA",
      "n": "6yQ2uHyv4yyKNxrEjbWjAoZaGxGzO-0CKQsedoJHqr0aREu-KgKmgJK9McFAH-ZiNj9yc-SZVSi_wEYfEZYvB7iZwKy86bTotN9ZF4dA2iPuJCYpOC1xMo87kVv45Xjb9SURXcmpuUmPf4PN4ZdT07JRs41f126YUfePqvxDhzoX5q0to1OEBszsjZUKGjvKb7rdSOYqmuEmdfI2PlGBl6vq4nbIV_zxCAseN-CYUWKR3sylJX3Mg9N5V0W-WcOEvaNHumu73gIEjS8HhJmtZ636gXY3ePhzDeo2Mxurj902WZR3QFjrqSPp2-_OBalxxvdLOP-JMBRNEoNjjV5nRQ",
      "e": "AQAB"
    },
    "ard_enrollment_form": {
      "legal_name": "ADI Entity legal name",
      "address": "legal address",
      "email": "email@ix_1_domain.com",
      "phone": "+1-650-555-1212",
      "license_id": "ADI-Lic#9348145"
    },
    "url": "https://adi.ix_1_domain.com"
  },
  "signature": "kajdfi8J4piJSUzI...1NObTjhad8d8adjadnap1c2VySWQiOiJhMS"
}
```

### B.1.3 enroll_issuer

```json
{
  "request_id": "bb20b6aa-2063-45f5-ab20-9f2b4f1224ec",
  "action": "ENROLL",
  "role": "ISSUER",
  "ard_da_user_name": "issuer_admin",
  "ard_da_name": "issuer_1",
  "ard_enrollment_form": {
    "legal_name": "ADI Entity legal name",
    "address": "legal address",
    "email": "email@issuer_1_domain.com",
    "phone": "+1-650-555-1212",
    "license_id": "ADI-Lic#9348145"
  },
  "url": "https://adi.issuer_1_domain.com"
}
```

### B.1.4 enroll_sp

```json
{
  "request_id": "bb20b6aa-2063-45f5-ab20-9f2b4f1224ec",
  "action": "ENROLL",
  "role": "SERVICE_PROVIDER",
  "ard_da_user_name": "adi_authority",
  "ard_da_name": "service_provider_1",
  "service_provider_enrollment_form": {
    "legal_name": "ADI Entity legal name",
    "address": "legal address",
    "email": "email@service_provider_1_domain.com",
    "phone": "+1-650-555-1212",
    "license_id": "ADI-Lic#9348145"
  },
  "url": "https://adi.service_provider_1_domain.com"
}
```

### B.1.5 enroll_user

```json
{
  "request_information": {
    "id": "45bde61c-7da0-4f85-aed4-39d2d7508e99",
    "digital_address": "user2@ix_1",
    "legal_info": {
      "name": "Jane Doe",
      "address": "legal address"
    },
    "contact_info": {
      "email": "jane@example.com",
      "phone": "+1-650-555-1212"
    },
    "authorized_by": "did:adi:f6e18f71-4311-4e09-8bfc-9980a90e4be7/region_1/ix_1",
    "url": "https://user.ix.com"
  },
  "auth_signature": "hbGciOiJSUzI...1NObTjhad8d8adjadnap1c2VySWQiOiJhMS"
}
```

## B.2 Verifiable Credentials (VCs)

### B.2.1 make_vc_offer

```json
{
  "credential_detail": {},
  "issuer_state": "eyJhbGciOiJSU0Et...FYUaBy",
  "nonce": "ekjer09e0909rkkr9r"
}
```

### B.2.2 vc_offer

POST ~user/vc_offer

```json
{
  "id": "7560e8400-e79n-21d4-f719-748646810442",
  "credential_detail": {
    "subject": "did:adi:{subject_did}",
    "credential_issue_request": {
      "credential_issuer": "https://adi.issuer_domain.com",
      "credential_configuration_ids": [
        "VC_Schema_Id"
      ],
      "grants": {
        "pre_authorized_code": "twwZFMTzWP_TGTWy7IB6faNhBkO2slAS-_bjQHNt0us",
        "authorization_code": {}
      }
    }
  }
}
```

### B.2.3 issue_vc_token

POST ~issuer/issue_vc_token

```json
{
  "header": {
    "alg": "RS256",
    "type": "JWT"
  },
  "payload": {
    "vc_offer": {
      "id": "7560e8400-e79n-21d4-f719-748646810442",
      "credential_detail": {
        "subject": "did:adi:user2/r_1/ix_1",
        "credential_issue_request": {
          "credential_issuer": "https://credential-issuer.issuer_1.com",
          "credential_configuration_ids": [
            "UniversityDegree"
          ],
          "grants": {
            "pre_authorized_code": "twwZFMTzWP_TGTWy7IB6faNhBkO2slAS-_bjQHNt0us",
            "authorization_code": {}
          }
        }
      }
    }
  },
  "signature": "hbGciOiJSUzI...1NObTjhad8d8adjadnap1c2VySWQiOiJhMS"
}
```

### B.2.4 VC

```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1"
  ],
  "vc_id": "http://example.edu/credentials/3732",
  "type": [
    "VerifiableCredential",
    "UniversityDegreeCredential"
  ],
  "issuer": "did:adi:eedec811-0f26-4656-a6cd-59d5f0bf2c16/region_1/ix_3",
  "issuanceDate": "2024-01-01T19:23:24Z",
  "expirationDate": "2025-01-01T19:23:24Z",
  "credentialSubject": {
    "id": "did:adi:ebfeb1f712ebc6f1c276e12ec21/region_2/ix_1",
    "degree": {
      "type": "BachelorDegree",
      "name": "Bachelor of Science and Arts"
    }
  },
  "proof": {}
}
```

### B.2.5 vc_request

```json
{
  "sp_id": "sp1@interchange1",
  "schemas_accepted": [
    "US_Passport",
    "US_Driver_License",
    "Univ_ID"
  ]
}
```

### B.2.6  vc_authorization_token

```json
{
  "authorization_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL0hPTUVAREFTMSIsInN1YmoiOiJ1c2VyMkBEQVMxIiwiYXVkIjoiaWQuSE9NRUBEQVMxIiwiY0dVSUQiOiJ1c2VyMkBEQVMxIiwiY3VzdG9tOnVzZXJJZCI6InVzZXIyQERBUzEiLCJkZXZpY2VJRCI6ImQxIiwiZW52aXJvbm1lbnRJRCI6IkhPTUVAREFTMSIsImZpbmdlclByaW50IjoiVVJtaUdRMG1uN2wvS0ZFOEJTdE96VXJTYlJ3dEVRZTdJbGpIUUdoa0NxYz0iLCJpc0xvZ2luQXV0aG9yaXplZCI6dHJ1ZSwiaWF0IjoxNzIxNTkwMDE2LCJleHAiOjE3MjE1OTM2MTZ9.euXn53CnX3xq6zYIklvKa3SnUoNrqF1nn80Un9E1lZMhEmifwR__sR9OYDDRdnxgk3nCZrlTnyV_cKLpXivSl-lAY3-wYUxe5uDFb7qxIQnGPC-VIS4fdifTyrOmAILHJNftGICxY0mSsRAZWQSD4gdImb0Yp2UF-ijiLJJdnASLdM7to1gbu4joTdgkSKwCsMTzs87m4pNlJCzzqpdlcIWkndewoY8-cBxatYOzvwYJoE52-o86lFiHj1uRU4EPyxCfynw4mh_zumfjhsUyS1HyRM7Iv77EVllp1hkWhVynzH8w85TthSiYwjBpL-WfN9nEVG-q6e7nzB4okRiMKw"
}
```

### B.2.7  ADI-AGD role VC

```json
{
  "request_id": "aa2f772-0c23-4d11-99b6-c7fdc932ca26",
  "status": "{ OK | FAILED | PENDING }",
  "error_msg": "error msg or null if none",
  "adi_ard_role_vc": {
    "header": {
      "alg": "RS256",
      "type": "JWT"
    },
    "payload": {
      "type": "ADI-AGD-VC",
      "issuer": "did:adi:8c019421-2920-410c-acfe-77d5c87b187c",
      "credentialSubject": {
        "subject": "did:adi:71a39c8d-0500-45d0-88d0-9c08d3931cce",
        "digital_address": "agd_admin@global_1",
        "role": "AGD",
        "ard_da_global_name": "global_1",
        "id_doc": {
          "id": "did:adi:71a39c8d-0500-45d0-88d0-9c08d3931cce/region_1/",
          "public_key": {
            "kty": "RSA",
            "n": "6yQ2uHyv4yyKNxrEjbWjAoZaGxGzO-0CKQsedoJHqr0aREu-KgKmgJK9McFAH-ZiNj9yc-SZVSi_wEYfEZYvB7iZwKy86bTotN9ZF4dA2iPuJCYpOC1xMo87kVv45Xjb9SURXcmpuUmPf4PN4ZdT07JRs41f126YUfePqvxDhzoX5q0to1OEBszsjZUKGjvKb7rdSOYqmuEmdfI2PlGBl6vq4nbIV_zxCAseN-CYUWKR3sylJX3Mg9N5V0W-WcOEvaNHumu73gIEjS8HhJmtZ636gXY3ePhzDeo2Mxurj902WZR3QFjrqSPp2-_OBalxxvdLOP-JMBRNEoNjjV5nRQ",
            "e": "AQAB"
          }
        },
        "ard_information": {
          "legal_name": "ADI Entity legal name",
          "address": "legal address",
          "email": "email@region_1.com",
          "phone": "+1-650-555-1212",
          "license_id": "ADI-Lic#9348145",
          "service_url": "https://agd.global_1.com"
        },
        "rights": {
          "authorized_to_issue": [
            "AGD-VC"
          ],
          "authorized_max_assurance_level": [
            "3"
          ]
        }
      }
    },
    "vc_signature": "hbGciOiJSUzI...1NObTjhad8d8adjadnap1c2VySWQiOiJhMS"
  }
}
```

### B.2.8 ADI-IX role VC

```json
{
  "header": {
    "alg": "RS256",
    "type": "JWT"
  },
  "payload": {
    "type": "ADI-IX-VC",
    "issuer": "did:adi:8c019421-2920-410c-acfe-77d5c87b187c",
    "credentialSubject": {
      "subject": "did:adi:f6e18f71-4311-4e09-8bfc-9980a90e4be7/region_1/ix_1",
      "digital_address": "interchange_admin@ix_1",
      "role": "IX",
      "ard_da_interchange_name": "ix_1",
      "id_doc": {
        "id": "did:adi:f6e18f71-4311-4e09-8bfc-9980a90e4be7/region_1/ix_1",
        "public_key": {
          "kty": "RSA",
          "n": "6yQ2uHyv4yyKNxrEjbWjAoZaGxGzO-0CKQsedoJHqr0aREu-KgKmgJK9McFAH-ZiNj9yc-SZVSi_wEYfEZYvB7iZwKy86bTotN9ZF4dA2iPuJCYpOC1xMo87kVv45Xjb9SURXcmpuUmPf4PN4ZdT07JRs41f126YUfePqvxDhzoX5q0to1OEBszsjZUKGjvKb7rdSOYqmuEmdfI2PlGBl6vq4nbIV_zxCAseN-CYUWKR3sylJX3Mg9N5V0W-WcOEvaNHumu73gIEjS8HhJmtZ636gXY3ePhzDeo2Mxurj902WZR3QFjrqSPp2-_OBalxxvdLOP-JMBRNEoNjjV5nRQ",
          "e": "AQAB"
        }
      },
      "ard_information": {
        "legal_name": "ADI Entity legal name",
        "address": "legal address",
        "email": "email@ix_1.com",
        "phone": "+1-650-555-1212",
        "license_id": "ADI-Lic#9348145",
        "service_url": "https://ix.ix_1.com"
      },
      "rights": {
        "authorized_to_issue": [
          "ADI-IX-VC"
        ],
        "authorized_max_assurance_level": [
          "3"
        ]
      }
    }
  },
  "vc_signature": "lek55jJuJSUzI...1NObTjhad8d8adjadnap1c2VySWQiOiJhMS"
}
```

### B.2.9 ADI-ISSUER role VC

```json
{
  "header": {
    "alg": "RS256",
    "type": "JWT"
  },
  "payload": {
    "type": "ADI-ISSUER-VC",
    "issuer": "did:adi:f6e18f71-4311-4e09-8bfc-9980a90e4be7/region_1/ix_1",
    "credentialSubject": {
      "subject": "did:adi:3b576f82-3506-4663-8ca4-51d614aea318/region_1/ix_1/issuer_1",
      "digital_address": "issuer_admin@issuer_1",
      "role": "ISSUER",
      "id_doc": {
        "id": "did:adi:f6e18f71-4311-4e09-8bfc-9980a90e4be7/region_1/ix_1",
        "public_key": {
          "kty": "RSA",
          "n": "7JKshd33Hyv4yyKNxrEjbWjAoZaGxGzO-0CKQsedoJHqr0aREu-KgKmgJK9McFAH-ZiNj9yc-SZVSi_wEYfEZYvB7iZwKy86bTotN9ZF4dA2iPuJCYpOC1xMo87kVv45Xjb9SURXcmpuUmPf4PN4ZdT07JRs41f126YUfePqvxDhzoX5q0to1OEBszsjZUKGjvKb7rdSOYqmuEmdfI2PlGBl6vq4nbIV_zxCAseN-CYUWKR3sylJX3Mg9N5V0W-WcOEvaNHumu73gIEjS8HhJmtZ636gXY3ePhzDeo2Mxurj902WZR3QFjrqSPp2-_OBalxxvdLOP-JMBRNEoNjjV5nRQ",
          "e": "AQAB"
        }
      },
      "ard_information": {
        "legal_name": "ADI Entity legal name",
        "address": "legal address",
        "email": "email@issuer_1.com",
        "phone": "+1-650-555-1212",
        "license_id": "ADI-Lic#9348145",
        "service_url": "https://issuer.issuer_1.com"
      },
      "rights": {
        "authorized_to_issue": [
          "ADI-User-VC"
        ],
        "authorized_max_assurance_level": [
          "3"
        ]
      }
    }
  },
  "vc_signature": "lek55jJuJSUzI...1NObTjhad8d8adjadnap1c2VySWQiOiJhMS"
}
```

### B.2.10 ADI-SP role VC

```json
{
  "header": {
    "alg": "RS256",
    "type": "JWT"
  },
  "payload": {
    "type": "ADI-SP-VC",
    "issuer": "did:adi:f6e18f71-4311-4e09-8bfc-9980a90e4be7/region_1/ix_1",
    "credentialSubject": {
      "subject": "did:adi:3b576f82-3506-4663-8ca4-51d614aea318/region_1/ix_1/sp_1",
      "digital_address": "sp_admin@service_provider_1",
      "role": "SERVICE_PROVIDER",
      "id_doc": {
        "id": "did:adi:f6e18f71-4311-4e09-8bfc-9980a90e4be7/region_1/ix_1",
        "public_key": {
          "kty": "RSA",
          "n": "7JKshd33Hyv4yyKNxrEjbWjAoZaGxGzO-0CKQsedoJHqr0aREu-KgKmgJK9McFAH-ZiNj9yc-SZVSi_wEYfEZYvB7iZwKy86bTotN9ZF4dA2iPuJCYpOC1xMo87kVv45Xjb9SURXcmpuUmPf4PN4ZdT07JRs41f126YUfePqvxDhzoX5q0to1OEBszsjZUKGjvKb7rdSOYqmuEmdfI2PlGBl6vq4nbIV_zxCAseN-CYUWKR3sylJX3Mg9N5V0W-WcOEvaNHumu73gIEjS8HhJmtZ636gXY3ePhzDeo2Mxurj902WZR3QFjrqSPp2-_OBalxxvdLOP-JMBRNEoNjjV5nRQ",
          "e": "AQAB"
        }
      },
      "ard_information": {
        "legal_name": "ADI Entity legal name",
        "address": "legal address",
        "email": "email@service_provider_1.com",
        "phone": "+1-650-555-1212",
        "license_id": "ADI-Lic#9348145",
        "service_url": "https://adi.service_provider_1.com"
      },
      "rights": {
        "authorized_to_issue": [],
        "authorized_max_assurance_level": []
      }
    }
  },
  "vc_signature": "lek55jJuJSUzI...1NObTjhad8d8adjadnap1c2VySWQiOiJhMS"
}
```

### B.2.11 ADI-Network User role VC

```json
{
  "header": {
    "alg": "RS256",
    "type": "JWT"
  },
  "payload": {
    "type": "ADI-User-VC",
    "issuer": "did:adi:f6e18f71-4311-4e09-8bfc-9980a90e4be7/region_1/ix_1",
    "credentialSubject": {
      "subject": "did:adi:3b576f82-3506-4663-8ca4-51d614aea318/region_1/ix_1/issuer_1",
      "digital_address": "USER_DA@IX_1",
      "role": "USER",
      "id_doc": {
        "id": "did:adi:f6e18f71-4311-4e09-8bfc-9980a90e4be7/region_1/ix_1",
        "public_key": {
          "kty": "RSA",
          "n": "7JKshd33Hyv4yyKNxrEjbWjAoZaGxGzO-0CKQsedoJHqr0aREu-KgKmgJK9McFAH-ZiNj9yc-SZVSi_wEYfEZYvB7iZwKy86bTotN9ZF4dA2iPuJCYpOC1xMo87kVv45Xjb9SURXcmpuUmPf4PN4ZdT07JRs41f126YUfePqvxDhzoX5q0to1OEBszsjZUKGjvKb7rdSOYqmuEmdfI2PlGBl6vq4nbIV_zxCAseN-CYUWKR3sylJX3Mg9N5V0W-WcOEvaNHumu73gIEjS8HhJmtZ636gXY3ePhzDeo2Mxurj902WZR3QFjrqSPp2-_OBalxxvdLOP-JMBRNEoNjjV5nRQ",
          "e": "AQAB"
        }
      },
      "user_information": {
        "legal_name": "ADI Entity legal name",
        "address": "legal address",
        "email": "email@issuer_1.com",
        "phone": "+1-650-555-1212",
        "service_url": "https://USER_DID_NUMBER.iX_1.com"
      },
      "rights": {}
    }
  },
  "vc_signature": "lek55jJuJSUzI...1NObTjhad8d8adjadnap1c2VySWQiOiJhMS"
}
```

## B.3 Network Services

### B.3.1 metadata

```json
{
  "credential_issuer": "https://credential-issuer.example.com",
  "authorization_servers": [
    "https://users.adi.com"
  ],
  "credential_endpoint": "https://credential-issuer.example.com",
  "credential_vault_endpoint": "https://vault.example.com",
  "batch_credential_endpoint": "https://credential-issuer.example.com/batch_credential",
  "deferred_credential_endpoint": "https://credential-issuer.example.com/deferred_credential",
  "credential_configurations_supported": {
    "UniversityDegreeCredential": {
      "format": "jwt_vc_json",
      "scope": "UniversityDegree",
      "credential_signing_alg_values_supported": [
        "ES256"
      ],
      "credential_definition": {
        "type": [
          "VerifiableCredential",
          "UniversityDegreeCredential"
        ],
        "credentialSubject": {
          "given_name": {
            "display": [
              {
                "name": "Given Name",
                "locale": "en-US"
              }
            ]
          },
          "family_name": {
            "display": [
              {
                "name": "Surname",
                "locale": "en-US"
              }
            ]
          },
          "degree": {},
          "gpa": {
            "display": [
              {
                "name": "GPA"
              }
            ]
          }
        }
      },
      "proof_types_supported": {
        "jwt": {
          "proof_signing_alg_values_supported": [
            "ES256"
          ]
        }
      },
      "display": [
        {
          "name": "University Credential",
          "locale": "en-US",
          "logo": {
            "url": "https://university.example.edu/public/logo.png",
            "alt_text": "a square logo of a university"
          },
          "background_color": "#12107c",
          "text_color": "#FFFFFF"
        }
      ]
    }
  }
}
```

### B.3.2 network_location

```json
{
  "digital_address": "issuer1@ix3.r1",
  "did": "did:adi:issuser1/ix3/r1"
}
```

### B.3.3 network_location_response

```json
{
  "metadata_url": "https://adi.issuer1.com"
}
```

### B.3.4 get_did_doc

```json
{
  "did": "did:adi:09f4cee0-b3a8-4bfe-a1f7-69d834764159/region1/IX_2"
}
```


