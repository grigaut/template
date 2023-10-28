GLOBAL_PYENV := $(shell command -v pyenv 2> /dev/null)

PURPLE:=\e[0;35m
GREEN:=\e[0;32m
NOCOLOR:=\033[0m
CONSTRUCTION:=\U1F6A7
VALID:=\U2705

# Verbose

.PHONY: _setting-message
_setting-message:
	@echo -e "  ${CONSTRUCTION} ${PURPLE}$(message)${NOCOLOR} ${CONSTRUCTION}"

.PHONY: _completed-message
_completed-message:
	@echo -e "  ${VALID} ${GREEN}$(message)${NOCOLOR} ${VALID}"

test:
	@${MAKE} -s _setting-message message="test test"
	@${MAKE} -s _completed-message message="test test"