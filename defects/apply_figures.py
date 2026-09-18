#!/usr/bin/env python3
"""
F-602: replace media/imageN.png references with named SVGs (Figures 1-10)
and Mermaid source (Figures 11-20).

Run from the kit folder:   python3 defects/apply_figures.py
Expects:  spec/figures/fig-NN-*.svg   and   spec/figures/figures-11-20-mermaid.md
Safe to re-run: it only acts on lines that still reference media/image.
"""
import re, os, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "adia_v3.md")
FIGDIR = os.path.join(HERE, "..", "spec", "figures")

CAPTIONS = {
    1: "Verifiable Credential Structure", 2: "Digital Credential Marketplace",
    3: "The ADI Ecosystem", 4: "ADI Roles", 5: "ADI Roles and Chain of Trust",
    6: "Authoritative Global Domain", 7: "Interchange Architecture", 8: "ADI Network",
    9: "Digital Address", 10: "ADI Network DID Addressing",
    11: "Creating an AGD", 12: "Enrolling an Interchange", 13: "Enrolling an Issuer",
    14: "Enrolling a Service Provider", 15: "Enrolling a User",
    16: "Issuing a VC — High-Level Flow", 17: "Issuing a VC — Detailed Flow",
    18: "Requesting a VC — High-Level Flow", 19: "Service Provider Requests a VC",
    20: "Service Provider Requests a DID Document",
}

# mermaid blocks keyed by figure number
mer_src = open(os.path.join(FIGDIR, "figures-11-20-mermaid.md"), encoding="utf-8").read()
MERMAID = {}
for m in re.finditer(r"## Figure (\d+)\..*?\n(```mermaid\n.*?\n```)", mer_src, re.S):
    MERMAID[int(m.group(1))] = m.group(2)

text = open(SPEC, encoding="utf-8").read()
lines = text.split("\n")
out, done = [], 0
for l in lines:
    m = re.search(r"media/image(\d+)\.\w+", l)
    if not m:
        out.append(l); continue
    n = int(m.group(1))
    cap = "Figure %d. %s" % (n, CAPTIONS[n])
    if n <= 10:
        svg = glob.glob(os.path.join(FIGDIR, "fig-%02d-*.svg" % n))
        if not svg:
            print("  WARNING: no SVG for figure %d -- line left unchanged" % n); out.append(l); continue
        rel = "figures/" + os.path.basename(svg[0])
        out.append("![%s](%s)" % (CAPTIONS[n], rel))
        out.append("")
        out.append("*%s*" % cap)
    else:
        if n not in MERMAID:
            print("  WARNING: no Mermaid for figure %d -- line left unchanged" % n); out.append(l); continue
        out.extend(MERMAID[n].split("\n"))
        out.append("")
        out.append("*%s*" % cap)
    done += 1

text = "\n".join(out)
# the old lines sometimes carried the caption after the <img>; drop now-duplicate bare captions
text = re.sub(r"\n\*Figure (\d+)\. [^\n]*\*\n+Figure \1[.:][^\n]*\n", lambda m: "\n*Figure %s. %s*\n" % (m.group(1), CAPTIONS[int(m.group(1))]), text)
open(SPEC, "w", encoding="utf-8").write(text)
print("figures replaced: %d   media/image references remaining: %d" % (done, text.count("media/image")))
