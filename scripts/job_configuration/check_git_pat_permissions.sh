#!/bin/bash
set -e

git_token=$1

# Get token permissions using GitHub API
permissions=$(curl -sS -f -I -H "Authorization: token $git_token" https://api.github.com | grep -i x-oauth-scopes)

# Check for Gist permissions
if [ "$(echo "$permissions" | grep -i gist)" == "" ]; then
    echo "No Gist permissions"
    exit 142
fi

# Check for repo:hook permissions
if [ "$(echo "$permissions" | grep -i repo_hook)" == "" ]; then
    echo "No Hook permissions"
    exit 242
fi

echo "Token verified"
exit 0