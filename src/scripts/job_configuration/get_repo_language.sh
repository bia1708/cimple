#!/bin/bash

username=$1
repo=$2

repo_name=$(echo $repo | awk -F'/' '{print $5}' | awk -F'.' '{print $1}')  # Get only repo name from repo link

repo_owner=$(echo $repo | awk -F'/' '{print $4}')

# Get primary language from repo (i.e. cimple's would be Python)
language=`gh api repos/$repo_owner/$repo_name/languages | jq 'to_entries | max_by(.value) | .key'`
echo "language:$language"