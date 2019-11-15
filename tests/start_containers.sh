#!/bin/sh

TESTDIR="$( cd "$(dirname "$0")" || . ; pwd -P )"
# shellcheck source=./utils.sh
. "$TESTDIR/utils.sh"

start_containers
