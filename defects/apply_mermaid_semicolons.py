#!/usr/bin/env python3
"""
Fix: replace semicolons inside Mermaid sequence-diagram message labels.

    python3 defects/apply_mermaid_semicolons.py --dry-run
    python3 defects/apply_mermaid_semicolons.py

Figures 12-20 render on GitHub as a plain code block instead of a diagram.
Figure 11, the one Mermaid diagram with no semicolon in it, renders correctly.
Every failing diagram contains at least one semicolon used as an ordinary
English sentence-joiner inside a message label, e.g.

    IX->>IX: Generate key pair; store private key in HSM

Mermaid's sequence-diagram grammar uses `;` internally in some parser
versions as a statement terminator, so a semicolon appearing inside message
text -- syntactically ordinary prose -- can silently break parsing depending
on which parser version a given renderer bundles. GitHub's failure mode for
this is exactly what was observed: no visible error, just a fallback to the
raw fenced block.

The fix replaces `; ` with `, ` inside every Mermaid block only. Prose
elsewhere in the document, and any semicolon outside a ```mermaid fence, is
left untouched.

Safe to re-run.
"""

import sys, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")


def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()

    def fix_block(m):
        body = m.group(1)
        new_body, n = re.subn(r";\s*", ", ", body)
        if n:
            fix_block.count += n
            fix_block.diagrams += 1
        return "```mermaid\n%s\n```" % new_body
    fix_block.count = 0
    fix_block.diagrams = 0

    new_text = re.sub(r"```mermaid\n(.*?)\n```", fix_block, text, flags=re.S)

    print("  semicolons replaced: %d, across %d diagram(s)" % (fix_block.count, fix_block.diagrams))

    if dry:
        print("\n  --dry-run: nothing written")
        return
    if fix_block.count == 0:
        print("\n  nothing to change")
        return
    open(SPEC, "w", encoding="utf-8").write(new_text)
    print("\n  written -- now run: make save")


if __name__ == "__main__":
    main()
