#!/bin/sh
# usage: scripts/push3.sh "commit message"  — commits everything and pushes to the 3 working branches
cd "$(dirname "$0")/.." || exit 1
git add -A && git commit -q -m "$1" -m "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_016fMLBc5QfN7Mz3ft8jbkgQ" || exit 1
for r in claude/epic-feynman-hp7irm main claude/keydrive-prototype-baseline-olwhnt; do git push -q origin HEAD:$r 2>&1 | tail -1; done
git log --oneline -1
