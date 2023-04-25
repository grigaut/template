PYTHON = $(shell command -v python 2> /dev/null)
VIRTUAL_ENV = .venv
HOOKS = .git/hooks
ifeq ($(OS), Windows_NT)
	BIN = ${VIRTUAL_ENV}/Scripts/
else
	BIN = ${VIRTUAL_ENV}/bin/
endif
STREAMLIT_MAIN_SCRIPT = app/main.py

# Main Rules

clean:
	rm -rf ${VIRTUAL_ENV}
	rm -rf ${HOOKS}

${VIRTUAL_ENV}:
	${PYTHON} -m venv ${VIRTUAL_ENV}
	${BIN}python -m pip install poetry

.PHONY: poetry-install
poetry-install: pyproject.toml poetry.lock
	${BIN}poetry install --only main --ansi

.PHONY: install
install:
	${MAKE} -s ${VIRTUAL_ENV}
	${MAKE} -s poetry-install

# Development Rules

.PHONY: poetry-install-dev
poetry-install-dev: pyproject.toml poetry.lock
	${BIN}poetry install --ansi

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
	$(BIN)poetry install --only docs --ansi


.PHONY: install-docs
install-docs:
	$(MAKE) -s ${VIRTUAL_ENV}
	$(MAKE) -s poetry-install-docs

.PHONY: view-docs
view-docs:
	$(MAKE) -s install-docs
	$(BIN)mkdocs serve

./site:
	$(MAKE) -s install-docs
	$(BIN)mkdocs build

.PHONY: build-docs
build-docs:
	$(MAKE) -s ./site

.PHONY: deploy-docs
deploy-docs:
	$(MAKE) -s install-docs
	$(BIN)mkdocs gh-deploy
	rm -r -f ./site
