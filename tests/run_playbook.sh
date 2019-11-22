#!/bin/sh

TESTDIR="$( cd "$(dirname "$0")" ; pwd -P )"
. $TESTDIR/utils.sh 

ansible-playbook -i $INV_FILE $PLAYBOOK $@ || exit 1
