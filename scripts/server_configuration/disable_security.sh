#!/bin/bash
set -e

username=$1
pat=$2
url=$3

# echo "import javaposse.jobdsl.plugin.GlobalJobDslSecurityConfiguration
# import jenkins.model.GlobalConfiguration
# GlobalConfiguration.all().get(GlobalJobDslSecurityConfiguration.class).useScriptSecurity=false" | \
#   java -jar ../artifacts/jenkins-cli.jar -auth $username:$pat -s $url groovy =

# curl --user "$username:$pat" --data-urlencode \
#   "script=$(< ./scripts/server_configuration/security.groovy)" $url/scriptText

# Disable script security and setup wizard
systemctl stop jenkins
sed -i 's/Environment="JAVA_OPTS=-Djava.awt.headless=true"/Environment="JAVA_OPTS=-Djava.awt.headless=true -Djenkins.install.runSetupWizard=false -Dpermissive-script-security.enabled=no_security"/' /lib/systemd/system/jenkins.service
# curl --user "$username:$pat" -d "script=security.groovy" $url/script

# echo "import javaposse.jobdsl.plugin.GlobalJobDslSecurityConfiguration
# import jenkins.model.GlobalConfiguration
# GlobalConfiguration.all().get(GlobalJobDslSecurityConfiguration.class).useScriptSecurity=false" | \
#   java -jar ../artifacts/jenkins-cli.jar -auth $username:$pat -s $url groovy =

systemctl daemon-reload
systemctl enable jenkins
systemctl start jenkins

curl --user "$username:$pat" --data-urlencode \
  "script=$(< ./scripts/server_configuration/security.groovy)" $url/scriptText

curl --user "$username:$pat" --data-urlencode \
  "script=$(< ./scripts/server_configuration/url_config.groovy)" $url/scriptText

