#!/bin/bash

repo=$1
git_username=$2
git_token=$3
token=$4
username=$5
url=$6
jnlp=$7

echo $git_token > ../artifacts/token.txt
output=$(gh auth login --with-token < ../artifacts/token.txt 2>&1 | grep error)
rm ../artifacts/token.txt
#gh extension install cli/gh-webhook

repo_name=$(echo $repo | awk -F'/' '{print $5}' | awk -F'.' '{print $1}')  # Get only repo name from repo link
webhook_url=$(systemctl status smee.service | grep -i forwarding | cut -d " " -f 7)  # Get smee url from service output
gh api /repos/$git_username/$repo_name/hooks \
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
#gh webhook forward --repo=$git_username/$repo_name --events=push --url=$url

echo "<com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl> \
  <scope>GLOBAL</scope>
  <id>jenkins_token</id>
  <username>$username</username>
  <password>$token</password>
  <description>jenkins_api_token</description>
  <usernameSecret>false</usernameSecret>
</com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl>" \
 | java -jar ../artifacts/jenkins-cli.jar -auth $username:$token -s http://localhost:8080/  \
   create-credentials-by-xml system::system::jenkins _

java -jar $jnlp -auth $username:$token -s $url \
delete-credentials system::system::jenkins _ gh_token

echo "<org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl> \
  <scope>GLOBAL</scope>
  <id>gh_token</id>
  <secret>$git_token</secret>
  <description>gh_token</description>
</org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl>" \
 | java -jar ../artifacts/jenkins-cli.jar -auth $username:$token -s http://localhost:8080/  \
   create-credentials-by-xml system::system::jenkins _

curl --user "$username:$token" --data-urlencode \
  "script=$(< ./scripts/job_configuration/add_server.groovy)" $url/scriptText

# echo "<?xml version='1.1' encoding='UTF-8'?>
# <github-plugin-configuration plugin="github@1.37.3">
#   <configs>
#     <github-server-config>
#       <name>GITHUB_SERVER</name>
#       <apiUrl>https://api.github.com</apiUrl>
#       <manageHooks>false</manageHooks>
#       <credentialsId>gh_token</credentialsId>
#       <clientCacheSize>20</clientCacheSize>
#     </github-server-config>
#   </configs>
# </github-plugin-configuration>" > /var/lib/jenkins/github-plugin-configuration.xml

# curl -X POST -u $username:$token $url/createItem?name=GITHUB_SERVER --data-urlencode "json={\"\": \"0\", \"credentialsId\": \"gh_token\", \"gitHubWebUri\": \"https://github.com\", \"gitHubApiUri\": \"https://api.github.com\", \"clientID\": \"\", \"clientSecret\": \"\", \"triggerScanOrganisationFolder\": \"true\"}"
