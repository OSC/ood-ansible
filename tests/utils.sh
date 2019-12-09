#!/bin/sh

TESTDIR="$( cd "$(dirname "$0")" || . ; pwd -P )"

export TESTDIR=$TESTDIR
export PLAYBOOK="$TESTDIR/playbook.yml"
export ANSIBLE_CONFIG="$TESTDIR/ansible.cfg"

start_containers(){
  DISTS="debian ubuntu fedora centos7"

  for DIST in $DISTS
  do
    DOCKERFILE="$TESTDIR/docker/Dockerfile.$DIST"
    IMG="ansible-test:$DIST"

    echo "building $DIST with $DOCKERFILE"
    docker build --rm --file="$DOCKERFILE" --tag="ansible-test:$DIST" . || exit 1

    echo "running $IMG"
    docker run --detach --rm --name "$DIST" "$IMG" sleep infinity
  done
}
