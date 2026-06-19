.PHONY: check format run test type

check: format type test

format:
	uv format

run:
	uv run -m clio

test:
	uv run pytest

type:
	uv check
