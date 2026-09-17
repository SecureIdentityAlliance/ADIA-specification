#!/usr/bin/env python3
"""
Check that defects.yaml is well-formed.

    python3 validate.py

Runs before every render and before every commit. Reports problems in
plain language, because the person most likely to trip over them is not
the person who wrote the file format.
"""

import sys, os, re
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
YAML_PATH = os.path.join(HERE, "defects.yaml")

OK_STATUS = {"Open", "Fixed", "Verified", "Rejected"}
REQUIRED  = ("id", "severity", "workstream", "status")


def fail(msg, detail=""):
    print("\n  PROBLEM: %s" % msg)
    if detail:
        for line in str(detail).split("\n")[:6]:
            print("    %s" % line)
    print()
    sys.exit(1)


def main():
    raw = open(YAML_PATH, encoding="utf-8").read()

    # tabs break YAML and are invisible on screen, so name them specifically
    for n, line in enumerate(raw.split("\n"), 1):
        if "\t" in line:
            fail("Line %d contains a Tab character." % n,
                 "YAML cannot use Tabs. Delete it and press the space bar instead.\n"
                 "  %s" % line.replace("\t", "→   "))

    try:
        doc = yaml.safe_load(raw)
    except Exception as e:
        fail("The tracker file could not be read.",
             "Usually this means the spacing at the start of a line changed,\n"
             "or a quote mark is unmatched. Details follow:\n%s" % e)

    if not isinstance(doc, dict) or "defects" not in doc:
        fail("The file is missing its 'defects:' list.")

    entries = doc["defects"]
    seen = {}
    for i, e in enumerate(entries, 1):
        if not isinstance(e, dict):
            fail("Entry %d is not shaped like the others." % i)
        for k in REQUIRED:
            if k not in e:
                fail("Entry %d is missing its '%s' line." % (i, k))

        did = e["id"]
        if did in seen:
            fail("Two entries share the ID %s (entries %d and %d)." % (did, seen[did], i),
                 "You probably copied an entry instead of editing it.\n"
                 "Delete the copy you added.")
        seen[did] = i

        if not re.match(r"^[A-F]-\d{3}$", str(did)):
            fail("'%s' is not a valid ID." % did, "IDs look like A-101 or E-510.")

        s = str(e["status"])
        if s not in OK_STATUS and not s.startswith(("Blocked(", "Superseded(")):
            fail("%s has an unrecognised status: '%s'" % (did, s),
                 "Allowed: Open, Fixed, Verified, Rejected,\n"
                 "         Blocked(D4), Superseded(A-102)\n"
                 "Capital letters matter — 'fixed' is not the same as 'Fixed'.")

        if e.get("check") == "auto" and s in ("Fixed", "Verified"):
            print("  note: %s is checked automatically, so its status will be" % did)
            print("        recalculated when the register is rebuilt.")

    print("  defects.yaml is fine — %d entries, no problems found." % len(entries))


if __name__ == "__main__":
    main()
