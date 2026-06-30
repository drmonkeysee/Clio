.PHONY: check format run test type vtype

check: format type test

format:
	uv format

run:
	uv run -m clio

test:
	uv run pytest

type:
	uv run basedpyright --level warning

vtype:
	uv run basedpyright
