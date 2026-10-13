#!/bin/sh
# usage: lab_ship.sh <lab> <module:fn> <prev module:fn> <slug> "<title>" "<summary>" "<keywords>" <ledger.md>
cd "$(dirname "$0")/../.." || exit 1
export NODE_PATH=$(npm root -g)
lab=$1
python3 scripts/page-kit/build.py $lab "$2" $([ "$3" = "-" ] && echo "" || echo "$3") >/dev/null || exit 1
python3 scripts/page-kit/lab_ledger.py $lab "$8"
python3 scripts/page-kit/lab_wire.py $lab "$4" "$5" "$6" "$7" >/dev/null
node scripts/check-site.js $lab | tail -6
node scripts/diagram-lint.js http://localhost:5931 $lab/concepts/$4.html | tail -2
node scripts/layout-check.js http://localhost:5931 $lab/index.html $lab/concepts/$4.html web/index.html design/index.html index.html | tail -4
