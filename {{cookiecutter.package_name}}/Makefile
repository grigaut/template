GLOBAL_PYTHON := $(shell command -v python 2> /dev/null)
GLOBAL_POETRY := $(shell command -v poetry 2> /dev/null)
GLOBAL_GIT := $(shell command -v git 2> /dev/null)
GLOBAL_PYENV := $(shell command -v pyenv 2> /dev/null)

PYTHON_TARGET_VERSION := {{cookiecutter.python_local_version}}

# Paths
VENV_DIRECTORY := ${PWD}/.venv
GIT_DIRECTORY := ${PWD}/.git
HOOKS_DIRECTORY := ${GIT_DIRECTORY}/hooks
{% if cookiecutter.include_docs %}
DOCS_SITE_DIRECTORY := ${PWD}/site
{% endif -%}

# Files to Monitor
PYPROJECT := ${PWD}/pyproject.toml
POETRY_LOCK := ${PWD}/poetry.lock
PRE_COMMIT_CONFIG := ${PWD}/.pre-commit-config.yaml
PYVENV_CONFIG := ${VENV_DIRECTORY}/pyvenv.cfg
DEV_INSTALLED := ${VENV_DIRECTORY}/.dev_installed
{% if cookiecutter.include_docs %}
DOCS_INSTALLED := ${VENV_DIRECTORY}/.docs_installed
{% endif -%}
INSTALLED := ${VENV_DIRECTORY}/.installed
REQUIREMENTS := ${PWD}/requirements.txt
MKDOCS_YAML := ${PWD}/mkdocs.yaml

# Colors and Emojis

PURPLE:=\e[0;95m
GREEN:=\e[0;92m
BLUE:=\e[0;94m
NOCOLOR:=\033[0m
CONSTRUCTION:=\U1F6A7
VALID:=\U2705
FIRE:=\U1F525

# Main Rules

all:
	@${MAKE} -s install-dev

clean:
	@rm -rf ${VENV_DIRECTORY}
	@rm -rf ${HOOKS_DIRECTORY}
	@${MAKE} -s _informative-message message="Virtual Environment and Hooks have been removed"

# Installation Rules

.PHONY: install
install:
	@${MAKE} -s ${INSTALLED}
	@${MAKE} -s ${GIT_DIRECTORY}
	@${MAKE} -s _informative-message message="To run a command within poetry's environment, prefix it with 'poetry run'"

.PHONY: install-dev
install-dev:
	@${MAKE} -s ${DEV_INSTALLED}
	@${MAKE} -s ${GIT_DIRECTORY}
	@${MAKE} -s ${HOOKS_DIRECTORY}
	@${MAKE} -s _informative-message message="To run a command within poetry's environment, prefix it with 'poetry run'"

{% if cookiecutter.include_docs %}
.PHONY: install-docs
install-docs:
	@${MAKE} -s ${DOCS_INSTALLED}
	@${MAKE} -s ${GIT_DIRECTORY}
	@${MAKE} -s _informative-message message="To run a command within poetry's environment, prefix it with 'poetry run'"
{% endif -%}

# Pyenv Rules

.PHONY: check-pyenv
check-pyenv:
	@${MAKE} -s _starting-task-message message="Checking Pyenv Installation..."
	@if [ -z ${GLOBAL_PYENV} ]; then echo -e "Pyenv is not installed on your global python. Check 'https://github.com/pyenv/pyenv' to install pyenv."; exit 2 ;fi
	@${MAKE} -s _completed-task-message message="Valid Installation"

.PHONY: _pyenv-install
_pyenv-install:
	@${MAKE} -s _starting-task-message message="Installing Python ${version} using Pyenv..."
	${GLOBAL_PYENV} install --skip-existing $(version)
	@${MAKE} -s _completed-task-message message="Installation Completed"

.PHONY: _pyenv-local
_pyenv-local:
	@${MAKE} -s _starting-task-message message="Setting Python ${version} as local version..."
	${GLOBAL_PYENV} local $(version)
	@${MAKE} -s _completed-task-message message="Local Python Version Set to ${version} "

.PHONY: set-pyenv-up
set-pyenv-up: check-pyenv
	@${MAKE} -s _pyenv-install version=$(PYTHON_TARGET_VERSION)
	@${MAKE} -s _pyenv-local version=$(PYTHON_TARGET_VERSION)

# Poetry Rules

.PHONY: install-poetry
install-poetry:
	@${MAKE} -s _starting-task-message message="Installing Poetry..."
	@curl -sSL https://install.python-poetry.org | ${GLOBAL_PYTHON}
	@${MAKE} -s _completed-task-message message="Successful Installation of Poetry"

.PHONY: check-poetry
check-poetry: ${PYPROJECT}
	@${MAKE} -s _starting-task-message message="Checking Poetry Configuration..."
	@if [ -z ${GLOBAL_POETRY} ]; then echo -e "Poetry is not installed on your global python. Use 'make install-poetry' to install Poetry on your global python."; exit 2 ;fi
	@${MAKE} -s _completed-task-message message="Valid Configuration"

${PYVENV_CONFIG}:
	@${MAKE} -s set-pyenv-up
	@${MAKE} -s check-poetry
	@${MAKE} -s _starting-task-message message="Set up of Poetry's Python Version..."
	@${GLOBAL_POETRY} env use $(subst \,/, $(shell command ${GLOBAL_PYENV} which python))
	@${MAKE} -s _completed-task-message message="Set Up of Poetry's Python Version Completed."

${POETRY_LOCK}: ${PYVENV_CONFIG}
	@${MAKE} -s _starting-task-message message="Creating poetry.lock..."
	@${GLOBAL_POETRY} lock --no-update --ansi
	@${MAKE} -s _completed-task-message message="Created"

${INSTALLED}: ${POETRY_LOCK}
	@${MAKE} -s _starting-task-message message="Installing Main Dependencies..."
	@${GLOBAL_POETRY} install --without dev --ansi
	@touch ${INSTALLED}
	@${MAKE} -s _completed-task-message message="Successful Installation of Main Dependencies"

.PHONY: poetry-export
poetry-export: ${REQUIREMENTS}

${REQUIREMENTS}: ${POETRY_LOCK}
	@${MAKE} -s _starting-task-message message="Exporting Dependencies to requirements.txt..."
	@${GLOBAL_POETRY} export -f requirements.txt -o requirements.txt --without-hashes
	@${MAKE} -s _completed-task-message message="Successful Export"

# Development Rules

${DEV_INSTALLED}: ${POETRY_LOCK}
	@${MAKE} -s _starting-task-message message="Installing All Dependencies..."
	@${GLOBAL_POETRY} install --ansi
	@touch ${DEV_INSTALLED}
	@${MAKE} -s _completed-task-message message="Successful Installation of All Dependencies"

${HOOKS_DIRECTORY}: ${PRE_COMMIT_CONFIG} ${POETRY_LOCK} ${GIT_DIRECTORY}
	@${MAKE} -s _starting-task-message message="Installing Pre-Commit Hooks..."
	@${GLOBAL_POETRY} run pre-commit install
	@${MAKE} -s _completed-task-message message="Successful Installation of Hooks"
{% if cookiecutter.include_tests %}
# Test Rules

.PHONY: tests
tests: ${DEV_INSTALLED}
	@${MAKE} -s _starting-task-message message="Running Tests..."
	@${GLOBAL_POETRY} run pytest
	@${MAKE} -s _completed-task-message message="Tests Completed"
{% endif %}
{% if cookiecutter.include_docs %}
# Documentation Rules

${DOCS_INSTALLED}: ${POETRY_LOCK}
	@${MAKE} -s _starting-task-message message="Installing Docs Dependencies..."
	@${GLOBAL_POETRY} install --only docs --ansi
	@${MAKE} -s _completed-task-message message="Successful Installation of Docs Dependencies"

.PHONY: view-docs
view-docs: ${DOCS_INSTALLED}
	@${MAKE} -s _starting-task-message message="Serving Docs On Local Port..."
	@${GLOBAL_POETRY} run mkdocs serve

${DOCS_SITE_DIRECTORY}: ${MKDOCS_YAML} ${DOCS_INSTALLED}
	@${MAKE} -s _starting-task-message message="Building Local Docs Folder..."
	@${GLOBAL_POETRY} run mkdocs build
	@${MAKE} -s _completed-task-message message="Build Completed"

.PHONY: build-docs
build-docs: ${DOCS_SITE_DIRECTORY}
{% if cookiecutter.is_on_github %}
.PHONY: deploy-docs
deploy-docs: ${DOCS_INSTALLED}
	@${MAKE} -s _starting-task-message message="Deploying Docs To Github..."
	@${GLOBAL_POETRY} run mkdocs gh-deploy
	@${MAKE} -s _completed-task-message message="Successful Deployment"
	@rm -rf ${DOCS_SITE_DIRECTORY}
{% endif -%}
{% endif -%}
# Git

set-git-up:
	@${MAKE} -s ${GIT_DIRECTORY}

.PHONY: check-git
check-git:
	@${MAKE} -s _starting-task-message message="Checking Git Installation..."
	@if [ -z ${GLOBAL_GIT} ]; then echo -e "Git is not installed on your computer. Check 'https://git-scm.com/downloads' to install git."; exit 2 ;fi
	@${MAKE} -s _completed-task-message message="Valid Installation"

${GIT_DIRECTORY}:
	@${MAKE} -s check-git
	@${MAKE} -s _starting-task-message message="Git Repository Initialisation..."
	@${GLOBAL_GIT} init
	@${MAKE} -s _completed-task-message message="Repository Initialisation Completed"
{% if cookiecutter.include_notebooks %}
	@${MAKE} -s enable-nbstripout

.PHONY: enable-nbstripout
enable-nbstripout: ${DEV_INSTALLED}
	@${MAKE} -s _starting-task-message message="Enabling nbstripout..."
	@${GLOBAL_POETRY} run nbstripout --install
	@${MAKE} -s _completed-task-message message="Enabled"
{% endif -%}
# Verbose

.PHONY: _starting-task-message
_starting-task-message:
	@echo -e "\n  ${CONSTRUCTION} ${PURPLE}$(message)${NOCOLOR} ${CONSTRUCTION}"

.PHONY: _completed-task-message
_completed-task-message:
	@echo -e "  ${VALID} ${GREEN}$(message)${NOCOLOR} ${VALID}"

.PHONY: _informative-message
_informative-message:
	@echo -e "  ${FIRE} ${BLUE}$(message)${NOCOLOR} ${FIRE}"
