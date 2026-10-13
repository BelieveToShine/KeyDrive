#!/bin/sh
# usage: ship.sh <module:fn> <prev module:fn> <slug> "<title>" "<summary>" "<keywords>" <ledger.md> "<commit msg>"
cd "$(dirname "$0")/../../.." || exit 1
export NODE_PATH=$(npm root -g)
python3 scripts/page-kit/build.py cosmos "$1" "$2" >/dev/null || exit 1
python3 scripts/page-kit/cosmos/ledger_add.py "$7"
python3 scripts/page-kit/cosmos/wire_page.py "$3" "$4" "$5" "$6" >/dev/null
node scripts/check-site.js cosmos | tail -6
node scripts/diagram-lint.js http://localhost:5931 cosmos/concepts/$(echo $3).html | tail -2
node scripts/layout-check.js http://localhost:5931 cosmos/index.html cosmos/concepts/$3.html data/index.html index.html | tail -4
