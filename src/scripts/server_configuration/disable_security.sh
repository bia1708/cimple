#!/bin/bash

username=$1
pat=$2
url=$3

echo "import javaposse.jobdsl.plugin.GlobalJobDslSecurityConfiguration
import jenkins.model.GlobalConfiguration
GlobalConfiguration.all().get(GlobalJobDslSecurityConfiguration.class).useScriptSecurity=false" | \
  java -jar ../artifacts/jenkins-cli.jar -auth $username:$pat -s $url groovy =

# Disable script security and setup wizard
systemctl stop jenkins
# echo '[Service]\nJAVA_ARGS="-Djava.awt.headless=true -Djenkins.install.runSetupWizard=false  -Dpermissive-script-security.enabled=true"' > /etc/systemd/system/jenkins.service.d/override.conf
sed -i 's/Environment="JAVA_OPTS=-Djava.awt.headless=true"/Environment="JAVA_OPTS=-Djava.awt.headless=true -Djenkins.install.runSetupWizard=false"/' /lib/systemd/system/jenkins.service
# sed -i 's,<useScriptSecurity>true</useScriptSecurity>,<useScriptSecurity>false</useScriptSecurity>,' /var/lib/jenkins/javaposse.jobdsl.plugin.GlobalJobDslSecurityConfiguration.xml

# curl --user "$username:$pat" -d "script=security.groovy" $url/script

# echo "import javaposse.jobdsl.plugin.GlobalJobDslSecurityConfiguration
# import jenkins.model.GlobalConfiguration
# GlobalConfiguration.all().get(GlobalJobDslSecurityConfiguration.class).useScriptSecurity=false" | \
#   java -jar ../artifacts/jenkins-cli.jar -auth $username:$pat -s $url groovy =

systemctl daemon-reload
systemctl enable jenkins
systemctl start jenkins