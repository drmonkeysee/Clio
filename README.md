# Clio

A prototyping project currently written in [Python](https://www.python.org). Eventually will be a simulator of some kind, but for now this is a project to play around with various generative algorithms such as [Perlin Noise](https://en.wikipedia.org/wiki/Perlin_noise).

*[Clio](https://en.wikipedia.org/wiki/Clio) (Κλειώ)*: the muse of history

## Make Commands

There is a Makefile provided for easy access to various build and run commands. Every command that invokes Python will also verify a virtual-environment is set up locally.

- `make int`: start a Python interpreter session using the Clio package's Python environment
- `make run`: run Clio with the appropriate Python environment
- `make type`: type-check the code base using [mypy](https://mypy-lang.org)
- `make clean`: delete cached bytecode files
- `make purge`: run `make clean` and delete the local virtual-environment
