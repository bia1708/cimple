#!/bin/bash

username=$1
token=$2
jnlp=$3
url=$4

echo "<com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl> \
  <scope>GLOBAL</scope>
  <id>jenkins_token</id>
  <username>$username</username>
  <password>$token</password>
  <description>Jenkins API token for $username</description>
  <usernameSecret>false</usernameSecret>
</com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl>" \
 | java -jar $jnlp -auth $username:$token -s $url  \
   create-credentials-by-xml system::system::jenkins _