#!/bin/bash

username=$1
token=$2
jnlp=$3
url=$4

# Add user's jenkins API token for jenkins as jenkins credentials
# I know, jenkinception here, but this is needed for wget-ting the console output in the
# Post-Actions stage of "GitHub status" jobs
echo "<com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl> \
  <scope>GLOBAL</scope>
  <id>jenkins_token</id>
  <username>$username</username>
  <password>$token</password>
  <description>Jenkins API token for $username</description>
  <usernameSecret>false</usernameSecret>
</com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl>" \
 | java -jar "$jnlp" -auth "$username":"$token" -s "$url"  \
   create-credentials-by-xml system::system::jenkins _