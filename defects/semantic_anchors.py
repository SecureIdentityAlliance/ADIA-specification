#!/usr/bin/env python3
"""
semantic_anchors.py -- automated fix for F-603.

Decouple intra-doc links from mutable heading ordinals (E-NNN):

  1. Inject a stable, topic-derived  <a id="err-<topic>"></a>  anchor onto every
     heading matching the error-id pattern. Idempotent.
  2. Rewrite every inbound link that targets a number-derived GFM slug
     (...#e-501-webauthn-ceremony-validation) to the semantic id
     (...#err-webauthn-ceremony-validation), across all files, resolving
     relative paths between files.

Join key between an old link and its heading is the TOPIC SLUG -- the heading
text with the E-NNN ordinal stripped. A renumber changes only the ordinal, so
the topic slug is invariant and the mapping is recoverable after the fact.

Python 3.8+, standard library only.
"""
from __future__ import annotations
import argparse, os, re, sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# --- configuration ----------------------------------------------------------
ID_NAMESPACE = "err-"                      # semantic id prefix: topic, never the number
MD_EXTS = (".md", ".markdown")

# Heading ordinal, e.g. "E-501", "E-501:", "E-501 - ", "E-501 . " (mid-dot U+00B7).
ORDINAL_RE = re.compile(
    r"^(?P<ordinal>[A-Za-z]+-\d+(?:\s*,\s*[A-Za-z]+-\d+)*)"
    r"\s*[:\u00b7.\u2013\u2014\-]*\s*(?P<topic>.+?)\s*$"
)
# A number-derived slug fragment: e-501-topic or e-501--topic (no digits after
# the first hyphen => not an ordinal => left alone, e.g. an existing err-*).
LINK_ORDINAL_RE = re.compile(r"^(?P<code>[a-z]+-\d+)-+(?P<topic>.+)$")

ATX_RE = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<text>.*?)\s*#*\s*$")
EXISTING_ANCHOR_RE = re.compile(r'<a\s+[^>]*id\s*=\s*"(?P<id>[^"]+)"[^>]*>\s*</a>', re.I)
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_LINK_RE = re.compile(r"(\]\()([^)\s]+)((?:\s+\"[^\"]*\")?)(\))")
REF_DEF_RE = re.compile(r"^(\s*\[[^\]]+\]:\s*<?)([^\s>]+)(>?.*)$")
_SLUG_STRIP = re.compile(r"[^\w\- ]+", re.UNICODE)

# --- slug helpers (GitHub github-slugger approximation) ---------------------
def slugify(text: str) -> str:
    s = _SLUG_STRIP.sub("", text.strip().lower())
    return s.replace(" ", "-")

def join_key(topic_slug: str) -> str:
    # normalization used ONLY to match old links to headings; collapses the
    # double hyphen that "E-501 . Topic" produces once the mid-dot is stripped.
    return re.sub(r"-+", "-", topic_slug).strip("-")

def heading_topic(text: str) -> Tuple[Optional[str], str]:
    plain = re.sub(r"<[^>]+>", "", text).strip()   # drop any existing inline anchor
    m = ORDINAL_RE.match(plain)
    if not m:
        return None, plain
    return m.group("ordinal"), m.group("topic")

# --- model ------------------------------------------------------------------
@dataclass
class Heading:
    lineno: int
    hashes: str
    ordinal: str
    topic: str
    semantic_id: str
    key: str
    has_anchor: bool

@dataclass
class FileDoc:
    path: str
    lines: List[str]
    headings: List[Heading] = field(default_factory=list)
    no_topic: List[int] = field(default_factory=list)

def parse_file(path: str) -> FileDoc:
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    doc = FileDoc(path=path, lines=lines)
    in_fence = False
    for i, line in enumerate(lines):
        fm = FENCE_RE.match(line)
        if fm:
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = ATX_RE.match(line)
        if not m:
            continue
        ordinal, topic = heading_topic(m.group("text"))
        if ordinal is None:
            continue                       # not an error-id heading; leave alone
        if not topic:
            doc.no_topic.append(i)
            continue
        topic_slug = slugify(topic)
        anchor = bool(EXISTING_ANCHOR_RE.search(line))
        if not anchor and i > 0:           # accept a block anchor on the line above
            prev = lines[i - 1].strip()
            pm = EXISTING_ANCHOR_RE.search(prev)
            anchor = bool(pm and prev == pm.group(0))
        doc.headings.append(Heading(
            lineno=i, hashes=m.group("hashes"), ordinal=ordinal, topic=topic,
            semantic_id=ID_NAMESPACE + topic_slug, key=join_key(topic_slug),
            has_anchor=anchor,
        ))
    return doc

# --- phase 1: anchors -------------------------------------------------------
def apply_anchors(doc: FileDoc, placement: str) -> int:
    by_line = {h.lineno: h for h in doc.headings}
    out, changed = [], 0
    for i, line in enumerate(doc.lines):
        h = by_line.get(i)
        if h and not h.has_anchor:
            anchor = f'<a id="{h.semantic_id}"></a>'
            if placement == "inline":
                out.append(f"{h.hashes} {anchor}{line[len(h.hashes)+1:].lstrip()}")
            else:
                out.append(anchor)
                out.append(line)
            changed += 1
        else:
            out.append(line)
    doc.lines = out
    return changed

# --- phase 2: link rewriting ------------------------------------------------
def mask_code(line: str) -> Tuple[str, List[str]]:
    spans: List[str] = []
    def repl(m):
        spans.append(m.group(0))
        return f"\x00{len(spans)-1}\x00"
    return re.sub(r"`+[^`]*`+", repl, line), spans

def unmask(line: str, spans: List[str]) -> str:
    return re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], line)

def resolve_target(cur_path: str, link_path: str) -> str:
    if not link_path:
        return os.path.abspath(cur_path)
    base = os.path.dirname(os.path.abspath(cur_path))
    return os.path.abspath(os.path.normpath(os.path.join(base, link_path)))

def new_fragment(frag: str, target_file: str,
                 registry: Dict[str, Dict[str, str]]) -> Optional[str]:
    lm = LINK_ORDINAL_RE.match(frag)
    if not lm:
        return None                        # not number-derived; don't touch
    table = registry.get(target_file)
    if not table:
        return None
    return table.get(join_key(lm.group("topic")))

def rewrite_links(doc: FileDoc, registry, dangling: List[str]) -> int:
    changed = 0
    in_fence = False
    for i, line in enumerate(doc.lines):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence or ("](" not in line and "]:" not in line):
            continue
        masked, spans = mask_code(line)

        def handle(dest: str) -> str:
            nonlocal changed
            if "#" not in dest:
                return dest
            path, frag = dest.split("#", 1)
            lm = LINK_ORDINAL_RE.match(frag)
            if not lm:
                return dest
            tgt = resolve_target(doc.path, path)
            sid = new_fragment(frag, tgt, registry)
            if sid is None:
                dangling.append(f"{doc.path}:{i+1}  #{frag}  (no topic match in {os.path.relpath(tgt)})")
                return dest
            changed += 1
            return f"{path}#{sid}"

        masked = INLINE_LINK_RE.sub(
            lambda m: m.group(1) + handle(m.group(2)) + m.group(3) + m.group(4), masked)
        rm = REF_DEF_RE.match(masked)
        if rm:
            masked = rm.group(1) + handle(rm.group(2)) + rm.group(3)
        doc.lines[i] = unmask(masked, spans)
    return changed

# --- driver -----------------------------------------------------------------
def discover(paths: List[str]) -> List[str]:
    files: List[str] = []
    for p in paths:
        if os.path.isfile(p):
            files.append(p)
        else:
            for root, dirs, names in os.walk(p):
                dirs[:] = [d for d in dirs if d != ".git"]
                files += [os.path.join(root, n) for n in names if n.endswith(MD_EXTS)]
    return sorted(set(files))

def main() -> int:
    ap = argparse.ArgumentParser(description="F-603: inject semantic heading anchors and rewrite number-derived links.")
    ap.add_argument("paths", nargs="+", help="markdown files or directories")
    ap.add_argument("--placement", choices=("inline", "block"), default="inline")
    ap.add_argument("--write", action="store_true", help="apply changes (default: dry run)")
    ap.add_argument("--check", action="store_true", help="exit 1 if any change is pending; write nothing")
    args = ap.parse_args()

    files = discover(args.paths)
    docs = [parse_file(f) for f in files]

    registry: Dict[str, Dict[str, str]] = {}
    collisions: List[str] = []
    for doc in docs:
        table: Dict[str, str] = {}
        by_id: Dict[str, List[str]] = {}
        for h in doc.headings:
            table[h.key] = h.semantic_id
            by_id.setdefault(h.semantic_id, []).append(h.topic)
        for sid, topics in by_id.items():
            if len(topics) > 1:
                collisions.append(f"{doc.path}: id '{sid}' claimed by {len(topics)} headings: {topics}")
        registry[os.path.abspath(doc.path)] = table
        for ln in doc.no_topic:
            collisions.append(f"{doc.path}:{ln+1}: error-id heading has no topic text; cannot derive id")

    anchors = links = 0
    dangling: List[str] = []
    for doc in docs:
        anchors += apply_anchors(doc, args.placement)
        links += rewrite_links(doc, registry, dangling)

    if args.write and not args.check:
        for doc in docs:
            with open(doc.path, "w", encoding="utf-8") as f:
                f.write("\n".join(doc.lines))

    verb = "applied" if (args.write and not args.check) else "pending"
    print(f"{len(files)} file(s) scanned; anchors {verb}: {anchors}; links {verb}: {links}")
    for c in collisions:
        print("  COLLISION:", c)
    for d in dangling:
        print("  DANGLING :", d)

    if collisions:
        return 2
    if args.check and (anchors or links):
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
