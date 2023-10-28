GLOBAL_PYTHON := $(shell command -v python 2> /dev/null)
GLOBAL_POETRY := $(shell command -v poetry 2> /dev/null)
GLOBAL_PYENV := $(shell command -v pyenv 2> /dev/null)

PYTHON_TARGET_VERSION := {{cookiecutter.python_local_version}}

HOOKS = .git/hooks

# Colors and Emojis

PURPLE:=\e[0;35m
GREEN:=\e[0;32m
NOCOLOR:=\033[0m
CONSTRUCTION:=\U1F6A7
VALID:=\U2705

# Main Rules

all:
	@${MAKE} -s install-dev

clean:
	@rm -rf ${GLOBAL_POETRY} env remove
	@rm -rf ${HOOKS}

# Installation Rules

.PHONY: install
install:
	@${MAKE} -s pyenv-set-up
	@${MAKE} -s poetry-install

.PHONY: install-dev
install-dev:
	@${MAKE} -s pyenv-set-up
	@${MAKE} -s poetry-install-dev
{% if not cookiecutter.is_project_only_local -%}
	@${MAKE} -s hooks-install
{% endif -%}

# Pyenv

.PHONY: check-pyenv
check-pyenv:
	@${MAKE} -s _starting-task-message message="Checking Pyenv Installation..."
	@if [ -z ${GLOBAL_PYENV} ]; then echo -e "Pyenv is not installed on your global python. Check 'https://github.com/pyenv/pyenv' to install pyenv."; exit 2 ;fi
	@${MAKE} -s _completed-task-message message="Valid Installation"

.PHONY: pyenv-install
pyenv-install: 
	@${MAKE} -s _starting-task-message message="Installing Python ${version} using Pyenv..."
	@${MAKE} -s check-pyenv
	${GLOBAL_PYENV} install --skip-existing $(version)
	@${MAKE} -s _completed-task-message message="Installation Completed"

.PHONY: pyenv-local
pyenv-local: 
	@${MAKE} -s _starting-task-message message="Setting Python ${version} as local version..."
	@${MAKE} -s check-pyenv
	${GLOBAL_PYENV} local $(version)
	@${MAKE} -s _completed-task-message message="Local Python Version Set to ${version} "

.PHONY: 
pyenv-set-up:
	@${MAKE} -s pyenv-install version=$(PYTHON_TARGET_VERSION)
	@${MAKE} -s pyenv-local version=$(PYTHON_TARGET_VERSION)

# Poetry Targets

.PHONY: check-poetry
check-poetry: pyproject.toml
	@${MAKE} -s _starting-task-message message="Checking Poetry Configuration..."
	@if [ -z ${GLOBAL_POETRY} ]; then echo -e "Poetry is not installed on your global python. Use 'make install-poetry' to install Poetry on your global python."; exit 2 ;fi
	@${GLOBAL_POETRY} lock --no-update --ansi
	@${MAKE} -s _completed-task-message message="Valid Configuration"

.PHONY: install-poetry
install-poetry:
	@${MAKE} -s _starting-task-message message="Installing Poetry..."
	@curl -sSL https://install.python-poetry.org | ${GLOBAL_PYTHON}
	@${MAKE} -s _completed-task-message message="Successful Installation of Poetry"

.PHONY: poetry-install
poetry-install:
	@${MAKE} -s _starting-task-message message="Installing Main Dependencies..."
	@${MAKE} -s check-poetry
	@${GLOBAL_POETRY} install --only main --ansi
	@${MAKE} -s _completed-task-message message="Successful Installation of Main Dependencies"

# Development Rules

.PHONY: poetry-install-dev
poetry-install-dev:
	@${MAKE} -s _starting-task-message message="Installing All Dependencies..."
	@${MAKE} -s check-poetry
	@${GLOBAL_POETRY} install --ansi
	@${MAKE} -s _completed-task-message message="Successful Installation of All Dependencies"

{% if not cookiecutter.is_project_only_local -%}
.PHONY: hooks_install
hooks-install: .pre-commit-config.yaml
	@${MAKE} -s _starting-task-message message="Installing Pre-Commit Hooks..."
	@${GLOBAL_POETRY} run pre-commit install
	@${MAKE} -s _completed-task-message message="Successful Installation of Hooks"
{% endif -%}
{% if cookiecutter.include_tests %}
# Test Rules

.PHONY: tests
tests:
	@${MAKE} -s _starting-task-message message="Running Tests..."
	@${MAKE} -s install-dev
	@${GLOBAL_POETRY} run pytest
	@${MAKE} -s _completed-task-message message="Tests Completed"
{% endif %}
{% if cookiecutter.include_docs %}
# Documentation Rules

.PHONY: poetry-install-docs
poetry-install-docs:
	@${MAKE} -s _starting-task-message message="Installing Docs Dependencies..."
	@${MAKE} -s check-poetry
	@${GLOBAL_POETRY} install --only docs --ansi
	@${MAKE} -s _completed-task-message message="Successful Installation of Docs Dependencies"

.PHONY: install-docs
install-docs:
	@${MAKE} -s poetry-install-docs

.PHONY: view-docs
view-docs:
	@${MAKE} -s _starting-task-message message="Serving Docs On Local Port..."
	@${MAKE} -s install-docs
	@${GLOBAL_POETRY} run mkdocs serve

./site:
	@${MAKE} -s _starting-task-message message="Building Local Docs Folder..."
	@${MAKE} -s install-docs
	@${GLOBAL_POETRY} run mkdocs build
	@${MAKE} -s _completed-task-message message="Build Completed"

.PHONY: build-docs
build-docs:
	@${MAKE} -s ./site
{% if not cookiecutter.is_project_only_local %}
.PHONY: deploy-docs
deploy-docs:
	@${MAKE} -s _starting-task-message message="Deploying Docs To Github..."
	@${MAKE} -s install-docs
	@${GLOBAL_POETRY} run mkdocs gh-deploy
	@${MAKE} -s _completed-task-message message="Successful Deployment"
	rm -r -f ./site
{% endif -%}
{% endif -%}
# Verbose

.PHONY: _starting-task-message
_starting-task-message:
	@echo -e "  ${CONSTRUCTION} ${PURPLE}$(message)${NOCOLOR} ${CONSTRUCTION}"

.PHONY: _completed-task-message
_completed-task-message:
	@echo -e "  ${VALID} ${GREEN}$(message)${NOCOLOR} ${VALID}"