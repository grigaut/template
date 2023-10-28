GLOBAL_PYTHON := $(shell command -v python 2> /dev/null)
GLOBAL_POETRY := $(shell command -v poetry 2> /dev/null)

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

# Poetry Targets

.PHONY: check-poetry
check-poetry: pyproject.toml
	@echo -e "  ${CONSTRUCTION} ${PURPLE}Checking Poetry Configuration...${NOCOLOR} ${CONSTRUCTION}"
	@if [ -z ${GLOBAL_POETRY} ]; then echo -e "Poetry is not installed on your global python. Use 'make install-poetry' to install Poetry on your global python."; exit 2 ;fi
	@${GLOBAL_POETRY} lock --no-update --ansi
	@echo -e "  ${VALID} ${GREEN}Valid Configuration${NOCOLOR} ${VALID}"

.PHONY: install-poetry
install-poetry:
	@echo -e "  ${CONSTRUCTION} ${PURPLE}Installing Poetry...${NOCOLOR} ${CONSTRUCTION}"
	@curl -sSL https://install.python-poetry.org | ${GLOBAL_PYTHON}
	@echo -e "  ${VALID} ${GREEN}Successful Installation of Poetry${NOCOLOR} ${VALID}"

.PHONY: poetry-install
poetry-install:
	@echo -e "  ${CONSTRUCTION} ${PURPLE}Installing Main Dependencies...${NOCOLOR} ${CONSTRUCTION}"
	@${MAKE} -s check-poetry
	@${GLOBAL_POETRY} install --only main --ansi
	@echo -e "  ${VALID} ${GREEN}Successful Installation of Main Dependencies${NOCOLOR} ${VALID}"

.PHONY: install
install:
	@${MAKE} -s poetry-install

# Development Rules

.PHONY: poetry-install-dev
poetry-install-dev:
	@echo -e "  ${CONSTRUCTION} ${PURPLE}Installing All Dependencies...${NOCOLOR} ${CONSTRUCTION}"
	@${MAKE} -s check-poetry
	@${GLOBAL_POETRY} install --ansi
	@echo -e "  ${VALID} ${GREEN}Successful Installation of All Dependencies${NOCOLOR} ${VALID}"

{% if not cookiecutter.is_project_only_local -%}
.PHONY: hooks_install
hooks-install: .pre-commit-config.yaml
	@echo -e "  ${CONSTRUCTION} ${PURPLE}Installing Pre-Commit Hooks...${NOCOLOR} ${CONSTRUCTION}"
	@${GLOBAL_POETRY} run pre-commit install
	@echo -e "  ${VALID} ${GREEN}Successful Installation of Hooks${NOCOLOR} ${VALID}"
{% endif -%}

.PHONY: install-dev
install-dev:
	@${MAKE} -s poetry-install-dev
{% if not cookiecutter.is_project_only_local -%}
	@${MAKE} -s hooks-install
{% endif -%}
{% if cookiecutter.include_tests %}
# Test Rules

.PHONY: tests
tests:
	@echo -e "  ${CONSTRUCTION} ${PURPLE}Running Tests...${NOCOLOR} ${CONSTRUCTION}"
	@${MAKE} -s install-dev
	@${GLOBAL_POETRY} run pytest
	@echo -e "  ${VALID} ${GREEN}Tests Completed${NOCOLOR} ${VALID}"
{% endif %}
{% if cookiecutter.include_docs %}
# Documentation Rules

.PHONY: poetry-install-docs
poetry-install-docs:
	@echo -e "  ${CONSTRUCTION} ${PURPLE}Installing Docs Dependencies...${NOCOLOR} ${CONSTRUCTION}"
	@${MAKE} -s check-poetry
	@${GLOBAL_POETRY} install --only docs --ansi
	@echo -e "  ${VALID} ${GREEN}Successful Installation of Docs Dependencies${NOCOLOR} ${VALID}"


.PHONY: install-docs
install-docs:
	@${MAKE} -s poetry-install-docs

.PHONY: view-docs
view-docs:
	@echo -e "  ${CONSTRUCTION} ${PURPLE}Serving Docs On Local Port...${NOCOLOR} ${CONSTRUCTION}"
	@${MAKE} -s install-docs
	@${GLOBAL_POETRY} run mkdocs serve

./site:
	@echo -e "  ${CONSTRUCTION} ${PURPLE}Building Local Docs Folder...${NOCOLOR} ${CONSTRUCTION}"
	@${MAKE} -s install-docs
	@${GLOBAL_POETRY} run mkdocs build
	@echo -e "  ${VALID} ${GREEN}Build Completed${NOCOLOR} ${VALID}"

.PHONY: build-docs
build-docs:
	@${MAKE} -s ./site
{% if not cookiecutter.is_project_only_local %}
.PHONY: deploy-docs
deploy-docs:
	@echo -e "  ${CONSTRUCTION} ${PURPLE}Deploying Docs To Github...${NOCOLOR} ${CONSTRUCTION}"
	@${MAKE} -s install-docs
	@${GLOBAL_POETRY} run mkdocs gh-deploy
	@echo -e "  ${VALID} ${GREEN}Successful Deployment${NOCOLOR} ${VALID}"
	rm -r -f ./site
{% endif -%}
{% endif -%}
