#!/bin/bash

repo=$1
git_username=$2
git_token=$3
token=$4
username=$5
url=$6
jnlp=$7

# Authenticate to gh
echo "$git_token" > ./artifacts/token.txt
output=$(gh auth login --with-token < ./artifacts/token.txt 2>&1 | grep error)
rm ./artifacts/token.txt

repo_name=$(echo "$repo" | awk -F'/' '{print $5}' | awk -F'.' '{print $1}')  # Get only repo name from repo link
webhook_url=$(systemctl status smee.service | grep -i forwarding | cut -d " " -f 7)  # Get smee url from service output

# Attempt to create new webhook for the given repo with the given smee url. If the hook already exists, nothing happens
gh api /repos/"$git_username"/"$repo_name"/hooks \
   --input - <<< '{
  "name": "web",
  "active": true,
  "events": [
    "push"
  ],
  "config": {
    "url": "'"$webhook_url"'",
    "content_type": "json"
  }
}'

# Try to delete any credentials that have been stored for the given repo
java -jar "$jnlp" -auth "$username":"$token" -s "$url" \
delete-credentials system::system::jenkins _ gh_token

# Create new credentials for the given repo
echo "<org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl> \
  <scope>GLOBAL</scope>
  <id>gh_token</id>
  <secret>$git_token</secret>
  <description>gh_token</description>
</org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl>" \
 | java -jar ./artifacts/jenkins-cli.jar -auth "$username":"$token" -s http://localhost:8080/  \
   create-credentials-by-xml system::system::jenkins _

# Try to create github server using current git credentials
curl --user "$username:$token" --data-urlencode \
  "script=$(< ./scripts/job_configuration/add_server.groovy)" "$url"/scriptText
