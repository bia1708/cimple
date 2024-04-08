#!/bin/bash

username=$1
pat=$2
jnlp=$3
url=$4

java -jar $jnlp -s $url -auth $username:$pat who-am-i

file=$(find . -name "plugins.txt")
while IFS= read -r line
do
  echo "$line"
  java -jar $jnlp -s $url -auth $username:$pat -webSocket install-plugin $line -deploy </dev/null
done < "$file"

java -jar $jnlp -s $url -auth $username:$pat restart

# Disable script security and setup wizard
systemctl stop jenkins
# echo '[Service]\nJAVA_ARGS="-Djava.awt.headless=true -Djenkins.install.runSetupWizard=false  -Dpermissive-script-security.enabled=true"' > /etc/systemd/system/jenkins.service.d/override.conf
sed -i 's/Environment="JAVA_OPTS=-Djava.awt.headless=true"/Environment="JAVA_OPTS=-Djava.awt.headless=true -Djenkins.install.runSetupWizard=false"/' /lib/systemd/system/jenkins.service
sed -i 's,<useScriptSecurity>true</useScriptSecurity>,<useScriptSecurity>false</useScriptSecurity>,' /var/lib/jenkins/javaposse.jobdsl.plugin.GlobalJobDslSecurityConfiguration.xml
systemctl daemon-reload
systemctl enable jenkins
systemctl start jenkins
