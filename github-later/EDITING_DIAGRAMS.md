# Editing the Diagrams

The ADIA specification has two kinds of figure, and they are edited differently.

| Figures | Form | Edit by |
|---|---|---|
| 1–10 | SVG in `spec/figures/` | Editing the PowerPoint source, re-exporting |
| 11–20 | Mermaid text inside `spec/adia_v3.md` | Editing the text directly |

This page is about the second kind. **Do not convert a Mermaid diagram back into an image.** The whole reason they are text is so a reviewer can see what changed in a pull request, and so the diagram cannot quietly disagree with the prose beside it. That is not a theoretical concern — Figure 15 showed the User Agent issuing the User's own credential for two revisions while the prose said the Interchange did, because nobody could read a PNG in a diff.

---

## 1. Where the diagrams live

Open `spec/adia_v3.md` and search for ` ```mermaid `. There are ten, each immediately below its section heading and immediately above its caption:

````markdown
<a id="creating-an-agd"></a>
## 10.1 Creating an AGD

```mermaid
sequenceDiagram
    ...
```

*Figure 11. Creating an AGD*
````

Edit between the fences. Nothing else needs to change.

---

## 2. See it while you work

**mermaid.live** — the official editor. Paste your diagram on the left, see it drawn on the right as you type. Errors are reported in plain language with a line number.

Use it for anything beyond a one-word change. BBEdit's Markdown preview does not render Mermaid, so a diagram that looks broken locally may be perfectly fine — check in mermaid.live before concluding anything is wrong.

GitHub renders Mermaid natively once the repository exists, so what you see in mermaid.live is what a reader will see.

---

## 3. The five things you need

### Participants

Declared at the top, in left-to-right order. `as` gives a short name for use in the diagram and a readable label for the reader.

```
participant DAS as IX DAS
participant UA as Cloud User Agent
actor USER as User
```

`actor` draws a stick figure. Use it for the human; `participant` for everything else.

**Declare every participant explicitly.** If you skip a declaration, Mermaid invents one the first time it sees the name, and it appears in whatever order the messages happen to run — which is rarely the order you want.

### Arrows

Three cover almost everything in this specification:

```
CIA->>UA: vc_offer                  solid arrow — a request or a send
UA-->>CIA: issue_vc_token           dashed arrow — a response or a return
DAS->>DAS: Create DID and DIDdoc    self-call — an internal step
```

The convention in this document: a solid arrow when one party acts on another, a dashed arrow when returning a result, and a self-call for work a party does alone. Follow it so the diagrams read consistently.

### Optional and alternative blocks

```
opt Interchange outsources identity proofing
    DAS->>CI: Request identity proofing
    CI-->>DAS: Proofing result (IAL)
end
```

`opt` — this section may or may not happen.
`alt` / `else` — one path or the other:

```
alt Credential is in the user vault
    UA->>VAULT: Fetch VC
else Credential is in the issuer vault
    UA->>CIA: Fetch VC
end
```

`loop` — repeat:

```
loop For each credential in the presentation
    SPA->>SPA: Verify signature and status
end
```

Every block ends with `end`, on its own line. Forgetting it is the most common error, and mermaid.live will tell you exactly which line.

### Automatic numbering

```
sequenceDiagram
    autonumber
    USER->>DAA: Request enrollment
```

Numbers every message. Insert a message in the middle and everything renumbers itself. Use it on flows the prose refers to by step number.

### Notes

For something that is not a message:

```
Note over DAS,UA: Vault key is created inside the HSM and never leaves it
Note right of USER: User verification happens on device
```

Use sparingly. If a note is doing a lot of work, the prose should probably be saying it instead.

---

## 4. A worked example

Figure 15, annotated. This is the most complex diagram in the specification; everything else is simpler.

```mermaid
sequenceDiagram
    autonumber
    actor USER as User
    participant DAA as Device App (DAA)
    participant DAS as IX DAS
    participant CI as CI Agent
    participant UA as Cloud User Agent
    participant AGD
    USER->>DAA: Request enrollment; complete forms; accept T&Cs
    DAA->>DAA: Generate FIDO credential (user verification enrolled)
    DAA->>DAS: POST ~ix/enroll_user (FIDO public key, HIDA if required, forms)
    DAS->>DAS: Check Digital Address uniqueness; verify HIDA per region policy
    opt Interchange outsources identity proofing
        DAS->>CI: Request identity proofing
        CI-->>DAS: Proofing result (IAL)
    end
    DAS->>UA: Provision Cloud User Agent; create vault signing key in HSM
    DAS->>DAS: Create User DID and DIDdoc (binds FIDO key and vault key)
    DAS->>DAS: Sign ADI-USER role VC with Interchange key
    DAS->>UA: Store ADI-USER role VC in user vault
    DAS->>AGD: Register User DID in directory
    DAS-->>DAA: Return Digital Address, DID, ADI-USER role VC
    DAA-->>USER: Enrollment complete
```

Reading it line by line:

- `autonumber` — steps are numbered, so §10.5's prose can say "at step 7".
- `actor USER` — the only human, drawn as a figure.
- `participant AGD` — declared with no `as`, because "AGD" is already short and readable.
- Participants are declared in the order the reader should scan them: the user on the left, the network on the right.
- `DAA->>DAA` at step 2 — the device generating its own key. Nobody else is involved, so it is a self-call.
- The `opt` block — identity proofing by an Issuer is permitted but not required. Everything indented inside it renders as a labelled box.
- `DAS->>DAS` at step 8 — the Interchange signs the User's role credential. **This is the line that was wrong for two revisions.** It said `UA->>UA`, meaning the User's own agent issued the User's own credential, which breaks the chain of trust in §8.6. If you change this line, you are changing the security model, not the picture.
- `DAS-->>DAA` at the end — dashed, because it is the return.

---

## 5. Rules for this document

**Message text stays short.** Mermaid does not wrap; a long message makes the whole diagram wide. If a message needs more than about ten words, the detail belongs in the prose.

**No colons in message text.** A colon separates the arrow from its label, so a second one confuses the parser. Write `POST ~ix/enroll_user` rather than `POST: ~ix/enroll_user`. Semicolons are also best avoided.

**Names match the prose.** If the specification says "Cloud User Agent", the participant label says "Cloud User Agent" — not "Wallet", not "UA". The point of text diagrams is that a reader can grep for a term and find it in both places.

**Change the diagram and the prose together, in one commit.** They describe the same flow. A commit that changes one and not the other is how they drifted in the first place.

**Use the sequence diagram type only.** Mermaid supports flowcharts, state diagrams, ER diagrams and more, but Figures 11–20 are all sequence diagrams and consistency matters more than expressiveness here. If you think a flow needs a different diagram type, raise it with the working group first.

---

## 6. When Mermaid is the wrong tool

Mermaid chooses its own layout and gives you very little control over it. That is fine for a sequence — the order of messages carries the meaning — but poor for a drawing where the *arrangement* carries meaning.

Figures 3–10 stay as SVG for exactly this reason. The pyramid in Figure 4, the nested boxes in Figure 7, the network topology in Figure 8: their layout is the content. Mermaid would draw something technically correct and much harder to read.

**The rule:** a sequence of messages over time → Mermaid. A picture whose arrangement matters → SVG from the PowerPoint source.

If you need a new architecture figure, edit the PowerPoint, export the slide as SVG into `spec/figures/` with a name like `fig-21-something-descriptive.svg`, and reference it as:

```markdown
![Short description for screen readers](figures/fig-21-something-descriptive.svg)

*Figure 21. Something Descriptive*
```

The alt text is required — `make status` will fail `F-602` without it.

---

## 7. After editing

```bash
cd ~/Documents/adia-spec/local-kit
make status
make save m="Update Figure 15: correct the role VC issuer"
```

`make explain ID=F-602` checks that every image has alt text and that every referenced file exists. It does not check Mermaid syntax — mermaid.live is the tool for that, and a broken diagram will render as an error box on GitHub rather than failing a build.

---

## 8. Reference

- **mermaid.live** — live editor, the place to work
- **mermaid.js.org/syntax/sequenceDiagram.html** — full sequence diagram syntax
- **GitHub's announcement of Mermaid support** — background on how it renders in repositories

Everything in this specification uses the small subset described above. You should not need more.
