# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

The high-level project description can be found in @README.md.

The initial design document is in @design.md (not checked into git).

## Commands

All common tasks are exposed via `make` and are defined in @README.md.

Any Python commands not found in the @Makefile can be run using `uv`.

## Architecture

Clio is a pygame-ce civilization simulator focused on procedurally-generated economics and history. The goal is emergent complexity from simple trade and economic rules between civilization units.

The entry point is `clio/__main__.py`, which calls `clio.app.run()`. The project is in early development — the `clio/` package currently contains only the stub `app.run()` function.

pygame-ce documentation can be found here @https://pyga.me/docs/

- when chosing a glyph to represent an entity stick with the available glyphs in @clio/codepage.py

## Code Style

- use modern Python constructs like type-hints, match statements, and the walrus operator `:=`, we're using 3.14+
- all module-public symbols should have type-hints, module- and class-private symbols do not need type-hints

## Environment

- `uv` is the build-tool for this project, all Python commands should go through `uv`
- do not install any dependencies yourself, only recommend any dependencies when the need arises
