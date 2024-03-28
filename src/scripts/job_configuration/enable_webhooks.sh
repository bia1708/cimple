#!/bin/bash

repo=$1
username=$2
url=$3

gh extension install cli/gh-webhook

repo_name=$(echo $repo | awk -F'/' '{print $5}' | awk -F'.' '{print $1}')  # Get only repo name from repo link
gh webhook forward --repo=$username/$repo_name --events=push --url=$url
