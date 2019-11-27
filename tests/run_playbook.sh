#!/bin/sh

TESTDIR="$( cd "$(dirname "$0")" ; pwd -P )"
. $TESTDIR/utils.sh 

ansible-playbook $PLAYBOOK $@ || exit 1
