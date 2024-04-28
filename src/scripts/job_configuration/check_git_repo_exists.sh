#!/bin/bash
set -e

username=$1
git_repo=$2

if [ "$(echo $git_repo | grep /$username/)" == "" ]; then
    echo "Repo doesn't belong to the given user."
    exit 1
fi

git ls-remote $git_repo
