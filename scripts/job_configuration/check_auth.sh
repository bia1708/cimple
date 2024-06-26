#!/bin/bash

git_token=$1
username=$2

# Authenticate to gh
echo "$git_token" > artifacts/token.txt
output=$(gh auth login --with-token < artifacts/token.txt 2>&1 | grep error)
rm artifacts/token.txt

if [ -n "$output" ]; then
    echo "Authentication error. Please check your git credentials and try again."
    exit 1
fi

# Check that the given token belongs to the user
user_info=$(curl -H "Authorization: token $git_token" https://api.github.com/user)
if [ "$(echo "$user_info" | grep "\"$username\"")" == "" ]; then
    echo "Username and token don't match!"
    exit 2
fi

# Print auth status to the console for debugging
gh auth status
