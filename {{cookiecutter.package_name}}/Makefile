GLOBAL_PYTHON := $(shell command -v python 2> /dev/null)
GLOBAL_POETRY := $(shell command -v poetry 2> /dev/null)

HOOKS = .git/hooks

# Main Rules

clean:
	rm -rf ${GLOBAL_POETRY} env remove
	rm -rf ${HOOKS}

# Poetry Targets

.PHONY: check-poetry
check-poetry: pyproject.toml
	@if [ -z ${GLOBAL_POETRY} ]; then echo "Poetry is not installed on your global python. Use 'make install-poetry' to install Poetry on your global python."; exit 2 ;fi
	${GLOBAL_POETRY} lock --no-update

.PHONY: install-poetry
install-poetry:
	curl -sSL https://install.python-poetry.org | ${GLOBAL_PYTHON} -

.PHONY: poetry-install
poetry-install:
	${MAKE} -s check-poetry
	${GLOBAL_POETRY} install --only main --ansi

.PHONY: install
install:
	${MAKE} -s poetry-install

# Development Rules

.PHONY: poetry-install-dev
poetry-install-dev:
	${MAKE} -s check-poetry
	${GLOBAL_POETRY} install --ansi

{% if not cookiecutter.is_project_only_local -%}
.PHONY: hooks_install
hooks-install: .pre-commit-config.yaml
	${GLOBAL_POETRY} run pre-commit install
{% endif -%}

.PHONY: install-dev
install-dev:
	${MAKE} -s poetry-install-dev
{% if not cookiecutter.is_project_only_local -%}
	${MAKE} -s hooks-install
{% endif -%}
{% if cookiecutter.include_tests %}
# Test Rules

.PHONY: tests
tests:
	${MAKE} -s install-dev
	${GLOBAL_POETRY} run pytest
{% endif %}
{% if cookiecutter.include_docs %}
# Documentation Rules

.PHONY: poetry-install-docs
poetry-install-docs:
	${MAKE} -s check-poetry
	${GLOBAL_POETRY} install --only docs --ansi


.PHONY: install-docs
install-docs:
	${MAKE} -s poetry-install-docs

.PHONY: view-docs
view-docs:
	${MAKE} -s install-docs
	${GLOBAL_POETRY} run mkdocs serve

./site:
	${MAKE} -s install-docs
	${GLOBAL_POETRY} run mkdocs build

.PHONY: build-docs
build-docs:
	${MAKE} -s ./site
{% if not cookiecutter.is_project_only_local %}
.PHONY: deploy-docs
deploy-docs:
	${MAKE} -s install-docs
	${GLOBAL_POETRY} run mkdocs gh-deploy
	rm -r -f ./site
{% endif -%}
{% endif -%}
