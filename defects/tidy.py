#!/usr/bin/env python3
"""
F-604 + F-605: remove invisible characters and tidy whitespace.

Run from the kit folder:   python3 defects/tidy.py
                           python3 defects/tidy.py --dry-run

Removes characters that are invisible on screen and break search:
    U+00A0 no-break space, U+202F narrow no-break space, U+2007 figure space
    U+200B zero-width space, U+2060 word joiner, U+FEFF byte-order mark
    tab characters inside prose (outside code fences)

Strips trailing whitespace, collapses runs of blank lines, guarantees a
final newline.

It does NOT touch curly quotes, en and em dashes, the section sign or the
copyright sign. Those are legitimate typography and belong in the document.
They are only a problem inside code fences, which is a separate check.
"""

import sys, os, re, unicodedata, collections

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")

# invisible or space-like characters -> replacement
ZAP = {
    "\u00a0": " ",   # no-break space
    "\u202f": " ",   # narrow no-break space
    "\u2007": " ",   # figure space
    "\u2009": " ",   # thin space
    "\u200a": " ",   # hair space
    "\u200b": "",    # zero-width space
    "\u200c": "",    # zero-width non-joiner
    "\u200d": "",    # zero-width joiner
    "\u2060": "",    # word joiner
    "\ufeff": "",    # byte-order mark
}

def main():
    dry = "--dry-run" in sys.argv
    text = open(SPEC, encoding="utf-8").read()
    before = text
    found = collections.Counter()

    # 1. invisible characters, everywhere
    for ch, rep in ZAP.items():
        n = text.count(ch)
        if n:
            found[ch] = n
            text = text.replace(ch, rep)

    # 2. tabs -> spaces, but only outside code fences (a tab in a JSON example
    #    is already caught by INV-gremlins and should be fixed deliberately)
    lines, out, fence, tabs = text.split("\n"), [], False, 0
    for l in lines:
        if l.lstrip().startswith("```"):
            fence = not fence
        elif not fence and "\t" in l:
            tabs += l.count("\t"); l = l.replace("\t", "    ")
        out.append(l)
    text = "\n".join(out)

    # 3. trailing whitespace
    trail = sum(1 for l in text.split("\n") if l != l.rstrip())
    text = "\n".join(l.rstrip() for l in text.split("\n"))

    # 4. no more than one blank line in a row, and exactly one newline at EOF
    blanks = len(re.findall(r"\n{3,}", text))
    text = re.sub(r"\n{3,}", "\n\n", text).rstrip("\n") + "\n"

    # report
    if found:
        for ch, n in found.most_common():
            try: nm = unicodedata.name(ch)
            except ValueError: nm = "?"
            print("  U+%04X  x%-5d %s" % (ord(ch), n, nm))
    print("  invisible characters removed: %d" % sum(found.values()))
    print("  tabs converted (prose only):  %d" % tabs)
    print("  lines with trailing space:    %d" % trail)
    print("  blank-line runs collapsed:    %d" % blanks)

    if dry:
        print("\n  --dry-run: nothing written")
        return
    if text == before:
        print("\n  nothing to change")
        return
    open(SPEC, "w", encoding="utf-8").write(text)
    print("\n  written")

if __name__ == "__main__":
    main()
