#!/bin/sh

TESTDIR="$( cd "$(dirname "$0")" || . ; pwd -P )"
# shellcheck source=./utils.sh
. "$TESTDIR/utils.sh" 

ansible-playbook -vvv -i "$INV_FILE" "$PLAYBOOK" --syntax-check || exit 1
