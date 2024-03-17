#!/bin/bash

username=$1
repo=$2

# Check if readme exists
gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  /repos/$username/$repo/readme

exit_code=$?

if [ $exit_code -eq 1 ]; then
    echo "The provided repository doesn't have a README."
fi