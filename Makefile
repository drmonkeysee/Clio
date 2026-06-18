.PHONY: check format run type

check: format type

format:
	uv format

run:
	uv run -m clio

type:
	uv check
