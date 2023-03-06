PY := python
VENV := venv
ACTIVATE := source $(VENV)/bin/activate
PYPATH := PYTHONPATH=src

.PHONY: clean int purge run

int: $(VENV)
	$(ACTIVATE) && $(PYPATH) $(PY)

run: $(VENV)
	$(ACTIVATE) && $(PYPATH) $(PY) -m clio

clean:
	find src -type d -name __pycache__ -exec $(RM) -rv {} +

purge: clean
	$(RM) -r $(VENV)

$(VENV):
	$(PY) -m venv $@
	$(ACTIVATE) && pip install -U pip setuptools wheel
