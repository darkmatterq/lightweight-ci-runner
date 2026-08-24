# AGENTS.md

## Project overview

This repository is a lightweight, self-hosted GitOps CI/CD pipeline and build engine for Linux. The codebase mixes Python utilities, a small C++ monitor binary, shell-oriented automation, and Docker-based deployment examples.

## Key commands

Use the project commands from the root `Makefile`:

- `make install-deps` — install Python dependencies from `requirements.txt`
- `make build` — compile the C++ monitor binary into `bin/ci-monitor`
- `make lint` — run `flake8` on `src/` and `sample-app/`
- `make test` — run the pytest suite from the repo root
- `make clean` — remove generated artifacts and caches

## Repository conventions

- Prefer changes that stay small and scriptable; this project is intentionally lightweight.
- Keep Python code compatible with the repo's current tooling and `flake8` checks.
- For C++ changes, maintain compatibility with the existing `g++ -std=c++17` build target.
- Treat `sample-app/` as a reference/demo app and keep it runnable without extra setup.
- When adding new tooling or dependencies, prefer the smallest necessary change and document why it is needed.

## Working expectations

- Validate with the most relevant command before finishing work: `make lint` and/or `make test` for Python changes, and `make build` when changing C++.
- Avoid broad refactors unless the task specifically requires them.
- Keep generated artifacts under `bin/` and do not commit temporary files from local runs.

## Relevant files

- `README.md` — project overview and high-level scope
- `Makefile` — canonical commands for install, build, lint, test, and clean
- `requirements.txt` — Python dependency list
- `sample-app/` — example app and validation target
