#!/bin/bash
set -e

username=$1
password=$2
url=$3

# Crumb is needed as an additional security measure for token generation
crumb=$(curl -s --cookie-jar "./artifacts/cookie" -u "$username":"$password" "$url/crumbIssuer/api/json" | jq -r '.crumb')

# Token generation
token=$(curl -X POST -H "Jenkins-Crumb:$crumb" "$url/me/descriptorByName/jenkins.security.ApiTokenProperty/generateNewToken" \
    --cookie "./artifacts/cookie" \
    --data 'newTokenName=PAT' \
    --user "$username:$password" | \
    jq -r '.data.tokenValue')

echo "token:$token"
