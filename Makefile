PY := python
VENV := venv
ACTIVATE := source $(VENV)/bin/activate
SRC := src
PYPATH := PYTHONPATH=$(SRC)

.PHONY: clean int purge run type

int: $(VENV)
	$(ACTIVATE) && $(PYPATH) $(PY)

run: $(VENV)
	$(ACTIVATE) && $(PYPATH) $(PY) -m clio

type: $(VENV)
	$(ACTIVATE) && MYPYPATH=$(SRC) mypy -p clio

clean:
	find src -type d -name __pycache__ -exec $(RM) -rv {} +

purge: clean
	$(RM) -r $(VENV)

$(VENV):
	$(PY) -m venv $@
	$(ACTIVATE) && pip install -U pip setuptools wheel && pip install -r requirements.txt
