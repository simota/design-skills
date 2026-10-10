# Wire this repo into a skills directory, and keep it inside its budgets.
#
# The repo is the single source of truth: each design-* directory is symlinked
# individually into every installed CLI's skills directory (claude, codex,
# agy), so each of those directories keeps whatever else it already carries.

REPO       := $(CURDIR)
CLAUDE_DIR ?= $(HOME)/.claude/skills
CODEX_DIR  ?= $(HOME)/.codex/skills
AGY_DIR    ?= $(HOME)/.gemini/antigravity-cli/skills

# Every CLI reading a SKILL.md gets the same working tree. A host is only
# written to when it is installed here, and its own home — the parent of the
# skills directory — is what says so: judging by the skills directory itself
# would skip a host that has one but has never been given a skill.
HOST_DIRS  := $(CLAUDE_DIR) $(CODEX_DIR) $(AGY_DIR)
# A directory named on the command line is wanted whether or not its host's home
# exists yet: `make link CLAUDE_DIR=.claude/skills` in a fresh project.
EXPLICIT   := $(foreach v,CLAUDE_DIR CODEX_DIR AGY_DIR,$(if $(filter command line,$(origin $(v))),$($(v))))

.DEFAULT_GOAL := help
.PHONY: help check validate test figures engines refute render hooks link unlink status

help:
	@echo "make check     validate + figures + test (what CI runs)"
	@echo "make validate  static rules over the corpus"
	@echo "make test      prove every rule still fires"
	@echo "make figures   recompute the numbers the reference layer states"
	@echo "make refute CLAIMS=f.json RUNNING=claude   put each claim to the engines that did not make it"
	@echo "make engines  ask each checker engine for one object; reports what is unreachable"
	@echo "make render    write the delivered blocks back into every SKILL.md"
	@echo "make hooks     install the pre-commit hook"
	@echo "make link      symlink the skills into claude / codex / agy"
	@echo "make unlink    remove those symlinks"
	@echo "make status    show what is linked"

# The order CI runs them in. CI's render-then-diff step is V17 seen from the
# other side: a stale block already fails validate.
check: validate figures test

validate:
	@python3 design-tools/validate.py

test:
	@python3 design-tools/test_validate.py

figures:
	@python3 design-tools/figures_check.py

engines:
	@python3 design-tools/engine.py --selftest

refute:
	@test -n "$(CLAIMS)" && test -n "$(RUNNING)" || { echo "usage: make refute CLAIMS=claims.json RUNNING=<the engine running this>"; exit 2; }
	@python3 design-tools/refute.py --running "$(RUNNING)" "$(CLAIMS)"

render:
	@python3 design-tools/render.py

# Pointed at, not copied: a copy goes stale when the hook changes, and `.git` is
# a file, not a directory, in a worktree.
hooks:
	@chmod +x design-tools/githooks/pre-commit
	@git config core.hooksPath design-tools/githooks
	@echo "pre-commit installed (core.hooksPath = design-tools/githooks)"

# A skill is a directory holding a SKILL.md, under skills/ where the plugin
# format expects it. The prefix alone is not the test: design-registry/ and
# design-tools/ share it and must never be installed.
SKILL_DIRS := $(patsubst %/SKILL.md,%,$(wildcard skills/design-*/SKILL.md))

link:
	@for dir in $(HOST_DIRS); do \
		case " $(EXPLICIT) " in *" $$dir "*) ;; *) \
			if [ ! -d "$$(dirname "$$dir")" ]; then echo "skip $$dir (host not installed here)"; continue; fi;; esac; \
		mkdir -p "$$dir"; \
		echo "$$dir"; \
		for path in $(SKILL_DIRS); do \
			name=$$(basename "$$path"); target="$$dir/$$name"; \
			if [ -e "$$target" ] && [ ! -L "$$target" ]; then \
				echo "  skip $$name (a real path is already there)"; \
			elif [ -L "$$target" ] && [ "$$(readlink "$$target")" != "$(REPO)/$$path" ]; then \
				echo "  skip $$name (linked to $$(readlink "$$target"), not this repo)"; \
			else \
				ln -sfn "$(REPO)/$$path" "$$target"; echo "  link $$name"; \
			fi; \
		done; \
	done

unlink:
	@for dir in $(HOST_DIRS); do \
		[ -d "$$dir" ] || continue; \
		echo "$$dir"; \
		for path in $(SKILL_DIRS); do \
			name=$$(basename "$$path"); target="$$dir/$$name"; \
			if [ -L "$$target" ] && [ "$$(readlink "$$target")" = "$(REPO)/$$path" ]; then \
				rm "$$target"; echo "  unlink $$name"; fi; \
		done; \
	done

status:
	@for dir in $(HOST_DIRS); do \
		echo "$$dir"; \
		for path in $(SKILL_DIRS); do \
			name=$$(basename "$$path"); target="$$dir/$$name"; \
			if [ -L "$$target" ] && [ "$$(readlink "$$target")" = "$(REPO)/$$path" ] && [ -e "$$target" ]; then \
				echo "  linked   $$name"; \
			elif [ -L "$$target" ]; then echo "  other    $$name -> $$(readlink "$$target")"; \
			else echo "  unlinked $$name"; fi; \
		done; \
	done
