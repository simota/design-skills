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
	@echo "make hooks     install the pre-commit hook (leaves other hooks alone)"
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

# A two-line shim in git's own hooks directory that runs the tracked hook, so
# the hook never goes stale. Not core.hooksPath: that switches off every other
# hook the contributor has. `--git-path` also finds the right place in a
# worktree, where `.git` is a file. Only a file that is exactly this shim is
# ours to rewrite; any other pre-commit is left alone and the target fails,
# because nothing was installed. Whether someone else's script really runs the
# rules — not only mentions them, and is executable — is not something a text
# match can tell, so it is not guessed at.
#
# A core.hooksPath set by anyone else is refused: --git-path follows it, and a
# shim written into a global hooks directory would run in every repository on
# the machine. The shim itself exits 0 where the tracked hook does not exist —
# an orphan branch, or a checkout from before it was added.
#
# Two earlier installs are ours as well and are replaced: the one-line exec
# shim, and the copy the first `make hooks` made (013f05b), which checks the
# working tree rather than what is staged. A symlink in the slot is never ours —
# writing through one, dangling or not, lands outside .git.
hooks:
	@chmod +x design-tools/githooks/pre-commit
	@if [ "$$(git config --get core.hooksPath)" = "design-tools/githooks" ]; then \
		if git config --unset core.hooksPath; then \
			echo "removed core.hooksPath set by an earlier make hooks"; fi; fi
	@if [ -n "$$(git config --get core.hooksPath)" ]; then \
		echo "core.hooksPath is $$(git config --get core.hooksPath); not installing there. Add to its pre-commit:"; \
		echo '  h="$$(git rev-parse --show-toplevel)/design-tools/githooks/pre-commit"; [ ! -f "$$h" ] || "$$h" || exit 1'; exit 1; fi
	@hook="$$(git rev-parse --git-path hooks)/pre-commit"; \
	shim='#!/bin/sh\nh="$$(git rev-parse --show-toplevel)/design-tools/githooks/pre-commit"\n[ -f "$$h" ] || exit 0\nexec "$$h" "$$@"\n'; \
	old='#!/bin/sh\nexec "$$(git rev-parse --show-toplevel)/design-tools/githooks/pre-commit" "$$@"\n'; \
	copied='#!/bin/sh\n# Budgets enforced by a mechanism rather than by remembering.\n# Install with: make hooks\nset -e\npython3 "$$(git rev-parse --show-toplevel)/design-tools/validate.py"\npython3 "$$(git rev-parse --show-toplevel)/design-tools/figures_check.py"\n'; \
	if [ -L "$$hook" ] || { [ -e "$$hook" ] && [ "$$(cat "$$hook")" != "$$(printf "$$shim")" ] \
			&& [ "$$(cat "$$hook")" != "$$(printf "$$old")" ] \
			&& [ "$$(cat "$$hook")" != "$$(printf "$$copied")" ]; }; then \
		echo "$$hook is not ours, so it is left as it is and nothing was installed."; \
		echo "Make sure it is executable and runs the rules, e.g.:"; \
		echo '  "$$(git rev-parse --show-toplevel)/design-tools/githooks/pre-commit" || exit 1'; exit 1; fi; \
	mkdir -p "$$(dirname "$$hook")"; \
	printf "$$shim" > "$$hook"; \
	chmod +x "$$hook"; \
	echo "pre-commit installed at $$hook"

# A skill is a directory holding a SKILL.md, under skills/ where the plugin
# format expects it. The prefix alone is not the test: design-registry/ and
# design-tools/ share it and must never be installed.
SKILL_DIRS := $(patsubst %/SKILL.md,%,$(wildcard skills/design-*/SKILL.md))

# `link` replaces a link that resolves nowhere — a moved checkout leaves one, and
# it serves no host as it is — but never a live link into another checkout.
# `unlink` removes only links into this checkout, dangling or not, so a link it
# did not make survives even while its target is unmounted.

link:
	@failed=0; for dir in $(HOST_DIRS); do \
		case " $(EXPLICIT) " in *" $$dir "*) ;; *) \
			if [ ! -d "$$(dirname "$$dir")" ]; then echo "skip $$dir (host not installed here)"; continue; fi;; esac; \
		mkdir -p "$$dir" || { failed=1; continue; }; \
		echo "$$dir"; \
		for path in $(SKILL_DIRS); do \
			name=$$(basename "$$path"); target="$$dir/$$name"; \
			if [ -e "$$target" ] && [ ! -L "$$target" ]; then \
				echo "  skip $$name (a real path is already there)"; \
			elif [ -L "$$target" ] && [ -e "$$target" ] && [ "$$(readlink "$$target")" != "$(REPO)/$$path" ]; then \
				echo "  skip $$name (linked to $$(readlink "$$target"), not this repo)"; \
			else \
				if ln -sfn "$(REPO)/$$path" "$$target"; then echo "  link $$name"; \
				else failed=1; fi; \
			fi; \
		done; \
	done; exit $$failed

unlink:
	@failed=0; for dir in $(HOST_DIRS); do \
		[ -d "$$dir" ] || continue; \
		echo "$$dir"; \
		for path in $(SKILL_DIRS); do \
			name=$$(basename "$$path"); target="$$dir/$$name"; \
			if [ -L "$$target" ] && [ "$$(readlink "$$target")" = "$(REPO)/$$path" ]; then \
				if rm "$$target"; then echo "  unlink $$name"; else failed=1; fi; fi; \
		done; \
	done; exit $$failed

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
