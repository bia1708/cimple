#!/bin/bash

git_token=$1
git_username=$2
repo=$3
username=$4
token=$5
jnlp=$6
url=$7
CRUMB=./aritfacts/cookie

repo_name=$(echo "$repo" | awk -F'/' '{print $5}' | awk -F'.' '{print $1}')  # Get only repo name from repo link

# Authenticate to gh
echo "$git_token" > ./artifacts/token.txt
output=$(gh auth login --with-token < ./artifacts/token.txt 2>&1 | grep error)
rm ./artifacts/token.txt

if [ -n "$output" ]; then
    echo "Authentication error. Please check your git credentials and try again."
    exit 1
fi

gh auth status

# Try to delete credential before adding a new one with the same name
java -jar "$jnlp" -auth "$username":"$token" -s "$url" \
delete-credentials system::system::jenkins _ git_pat_"$repo_name"

# Add github username and token as jenkins global credentials
echo "<com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl> \
  <scope>GLOBAL</scope>
  <id>git_pat_$repo_name</id>
  <username>$git_username</username>
  <password>$git_token</password>
  <description>git_pat_for_$repo_name</description>
  <usernameSecret>false</usernameSecret>
</com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl>" \
 | java -jar  "$jnlp" -auth "$username":"$token" -s "$url"  \
   create-credentials-by-xml system::system::jenkins _
