#!/bin/bash

git_token=$1

echo $git_token > ../artifacts/token.txt
output=$(gh auth login --with-token < ../artifacts/token.txt 2>&1 | grep error)
rm ../artifacts/token.txt

if [ ! -z "$output" ]; then
    echo "Authentication error. Please check your git credentials and try again."
    exit 1
fi

gh auth status