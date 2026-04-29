PYTHON ?= python3

.PHONY: build lint test validate run interview report mcq

build:
	$(PYTHON) -m compileall .

lint:
	$(PYTHON) -m ruff check .

test:
	$(PYTHON) -m pytest -q

validate: lint test

run:
	$(PYTHON) mba_skills.py --help

interview:
	$(PYTHON) mba_skills.py --interview

report:
	$(PYTHON) mba_skills.py --report-writing "SWOT analysis"

mcq:
	$(PYTHON) mba_skills.py --mcq --topic "operations engineering"
