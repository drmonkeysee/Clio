# Clio

A civilization simulator, focused on procedurally-generated economics and history. Written in [Python](https://www.python.org), on top of [pygame-ce](https://pyga.me) with the assistance of large-language model genAI tools like [Claude Code](https://claude.com/product/claude-code). The idea is to simulate trade and economic development between civilizational units with a set of (hopefully) simple rules that result in complex behavior. My ambition may exceed my grasp!

This project is built and managed using the [Astral](https://astral.sh) tool suite.

*[Clio](https://en.wikipedia.org/wiki/Clio) (Κλειώ)*: the muse of history

## Build

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
2. `uv sync` to install dependencies

## Run

The Makefile provides the following targets:

- `make run`: run the app
- `make format`: format source files
- `make type`: run the type checker
