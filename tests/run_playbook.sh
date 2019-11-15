#!/bin/sh

TESTDIR="$( cd "$(dirname "$0")" ; pwd -P )"

DISTS="debian ubuntu fedora"

for DIST in $DISTS
do
  DOCKERFILE="$TESTDIR/docker/Dockerfile.$DIST"
  IMG="ansible-test:$DIST"

  echo "building $DIST with $DOCKERFILE"
  docker build --rm --file=$DOCKERFILE --tag=ansible-test:$DIST . || exit 1

  echo "running $IMG"
  docker run --detach --rm --name $DIST $IMG sleep infinity
done

INV_FILE="$TESTDIR/inventory"
PLAYBOOK="$TESTDIR/playbook.yml"

export ANSIBLE_CONFIG=$TESTDIR/ansible.cfg

ansible-playbook -vvv -i $INV_FILE $PLAYBOOK --syntax-check || exit 1
ansible-playbook -i $INV_FILE $PLAYBOOK || exit 1
