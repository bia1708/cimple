#!/bin/bash
set -e

username=$1
git_repo=$2

# This should maybe be moved to another script, only for GitHub status enablement
# if [ "$(echo $git_repo | grep /$username/)" == "" ]; then
#     echo "Repo doesn't belong to the given user."
#     exit 1
# fi

# This will return non-zero code if the repository doesnt exist
git ls-remote "$git_repo" -q
