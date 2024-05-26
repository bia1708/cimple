#!/bin/bash
set -e

username=$1
pat=$2
url=$3

# Disable script security and setup wizard
systemctl stop jenkins
sed -i 's/Environment="JAVA_OPTS=-Djava.awt.headless=true"/Environment="JAVA_OPTS=-Djava.awt.headless=true -Djenkins.install.runSetupWizard=false -Dpermissive-script-security.enabled=no_security"/' /lib/systemd/system/jenkins.service

# Restart service for changes to take effect
systemctl daemon-reload
systemctl enable jenkins
systemctl start jenkins

# Disable job dsl script approval
curl --user "$username:$pat" --data-urlencode \
  "script=$(< ./scripts/server_configuration/security.groovy)" "$url"/scriptText

# Setup the url of the server to not be localhost, which it is by default
curl --user "$username:$pat" --data-urlencode \
  "script=$(< ./scripts/server_configuration/url_config.groovy)" "$url"/scriptText
