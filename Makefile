.PHONY: format run type

format:
	uv format

run:
	uv run -m clio

type:
	uv check
