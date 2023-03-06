PY := python
VENV := venv
ACTIVATE := source $(VENV)/bin/activate
PYPATH := PYTHONPATH=src

.PHONY: int purge run

int: $(VENV)
	$(ACTIVATE) && $(PYPATH) $(PY)

run: $(VENV)
	$(ACTIVATE) && $(PYPATH) $(PY) -m clio

purge:
	$(RM) -r $(VENV)

$(VENV):
	$(PY) -m venv $@
	$(ACTIVATE) && pip install -U pip setuptools wheel
