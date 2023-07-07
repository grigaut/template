GLOBAL_PYTHON := $(shell command -v python 2> /dev/null)
GLOBAL_POETRY := $(shell command -v poetry 2> /dev/null)

CURRENT_ENV := 

DEFAULT_ENV := .venv
HOOKS = .git/hooks

ifdef $(shell command -v poetry env info --path 2> /dev/null)
	VIRTUAL_ENV = poetry env info --path
else
	VIRTUAL_VENV = DEFAULT_ENV
endif

ifeq (${OS}, Windows_NT)
	BIN = ${VIRTUAL_ENV}/Scripts/
else
	BIN = ${VIRTUAL_ENV}/bin/
endif

# Main Rules

clean:
	rm -rf ${VIRTUAL_ENV}
	rm -rf ${HOOKS}

# Poetry Tatgets

check-poetry:
	@if [ -z ${GLOBAL_POETRY} ]; then echo "Poetry is not installed on your global python. Use 'make install-poetry' to install Poetry on your global python."; exit 2 ;fi
	${GLOBAL_POETRY} lock --no-update

install-poetry:
	curl -sSL https://install.python-poetry.org | ${GLOBAL_PYTHON} -

${VIRTUAL_ENV}:
	${PYTHON} -m venv ${VIRTUAL_ENV}

.PHONY: poetry-install
poetry-install: pyproject.toml
	${MAKE} -s check-poetry
	${GLOBAL_POETRY} install --only main --ansi

.PHONY: install
install:
	${MAKE} -s ${VIRTUAL_ENV}
	${MAKE} -s poetry-install

# Development Rules

.PHONY: poetry-install-dev
poetry-install-dev: pyproject.toml poetry.lock
	${MAKE} -s check-poetry
	${GLOBAL_POETRY} install --ansi

.PHONY: hooks_install
hooks-install: .pre-commit-config.yaml
	${BIN}pre-commit install

.PHONY: install
install-dev:
	${MAKE} -s ${VIRTUAL_ENV}
	${MAKE} -s poetry-install-dev
	${MAKE} -s hooks-install

.PHONY: tests
tests:
	${MAKE} -s install-dev
	${BIN}pytest

# Documentation Rules

.PHONY: poetry-install-docs
poetry-install-docs: poetry.lock
	${MAKE} -s check-poetry
	${GLOBAL_POETRY} install --only docs --ansi


.PHONY: install-docs
install-docs:
	${MAKE} -s ${VIRTUAL_ENV}
	${MAKE} -s poetry-install-docs

.PHONY: view-docs
view-docs:
	${MAKE} -s install-docs
	${BIN}mkdocs serve

./site:
	${MAKE} -s install-docs
	${BIN}mkdocs build

.PHONY: build-docs
build-docs:
	${MAKE} -s ./site

.PHONY: deploy-docs
deploy-docs:
	${MAKE} -s install-docs
	${BIN}mkdocs gh-deploy
	rm -r -f ./site
