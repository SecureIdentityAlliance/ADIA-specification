SPEC := spec/adia_v3.md

help:       ## show this list
	@grep -E '^[a-z-]+:.*##' Makefile | sed 's/:.*##/ —/' | sed 's/^/  make /'

setup:      ## one-time: install the safety net
	@python3 -m pip install --quiet pyyaml 2>/dev/null || true
	@git init -q 2>/dev/null || true
	@cp defects/pre-commit .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit
	@python3 defects/adia_checks.py $(SPEC) --ci >/dev/null 2>&1 || true
	@echo "Ready. Try: make status"

validate:   ## check the tracker file is well-formed
	@python3 defects/validate.py

register:   ## rebuild the report from the tracker + the spec
	@python3 defects/validate.py
	@python3 defects/render.py

status:     ## how many problems are left
	@python3 defects/adia_checks.py $(SPEC) | head -3

check:      ## full checker report
	@python3 defects/adia_checks.py $(SPEC)

ci:         ## has anything that used to pass started failing?
	@python3 defects/adia_checks.py $(SPEC) --ci

save:       ## record today's work in the local history
	@python3 defects/validate.py
	@python3 defects/make_editors_notes.py
	@python3 defects/render.py >/dev/null
	@git add -A && git commit -q -m "$(m)" && echo "Saved: $(m)"

.PHONY: help setup validate register status check ci save explain relocate anchors figures tidy assurance notes

explain:    ## why a check fails, e.g. make explain ID=E-501
	@python3 defects/adia_checks.py $(SPEC) --explain $(ID)

relocate:   ## refresh every line reference in defects.yaml from its anchor phrase
	@python3 defects/adia_checks.py $(SPEC) --relocate
	@python3 defects/render.py > /dev/null

anchors:    ## F-601/F-603: add stable anchors and rewrite the Google Docs links
	@python3 defects/add_anchors.py

figures:    ## F-602: swap media/imageN.png for named SVGs and Mermaid (needs spec/figures/)
	@python3 defects/apply_figures.py

tidy:       ## F-604/F-605: remove invisible characters, strip trailing whitespace
	@python3 defects/tidy.py

assurance:  ## apply the ASSURANCE_MODEL data model changes to Appendix B
	@python3 defects/apply_assurance.py

notes:      ## regenerate the Editor's Notes clause from the register
	@python3 defects/make_editors_notes.py
