PY := python
VENV := venv
ACTIVATE := source $(VENV)/bin/activate

.PHONY: purge run

run: $(VENV)
	$(ACTIVATE) && $(PY) main.py

purge:
	$(RM) -r $(VENV)

$(VENV):
	$(PY) -m venv $@
	$(ACTIVATE) && pip install -U pip setuptools wheel
