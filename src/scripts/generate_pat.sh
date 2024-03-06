#!/bin/bash

username=$1
password=$2
url=$3

crumb=$(curl -s --cookie-jar "../artifacts/cookie" -u $username:$password http://localhost:8080/crumbIssuer/api/json | jq -r '.crumb')

token=$(curl -X POST -H "Jenkins-Crumb:$crumb" "http://localhost:8080/me/descriptorByName/jenkins.security.ApiTokenProperty/generateNewToken" \
    --cookie "../artifacts/cookie" \
    --data 'newTokenName=PAT' \
    --user "$username:$password" | \
    jq -r '.data.tokenValue')

echo "token:$token"

