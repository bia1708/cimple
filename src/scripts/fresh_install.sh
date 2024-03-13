#!/bin/bash

username=$1
password=$2

if [ $(which jenkins) ]; then
	echo "Jenkins already exists on this device."
	exit 1
fi

# Install java
apt update
apt install -y fontconfig openjdk-17-jre

# Install jenkins
wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ > /dev/null
apt update
apt install jenkins

# Disable the setup wizard
java -Djenkins.install.runSetupWizard=false -jar jenkins.war 

# Enable service
systemctl daemon-reload
systemctl enable jenkins

# Start jenkins
systemctl start jenkins &

# Auth for the first time
wget http://localhost:8080/jnlpJars/jenkins-cli.jar -P "../artifacts"
pat=$(cat /var/lib/jenkins/secrets/initialAdminPassword)
#java -jar jenkins-cli.jar -s http://192.168.1.219:8080 -auth admin:$pat

# Create account for the user with given username and password
echo "jenkins.model.Jenkins.instance.securityRealm.createAccount('$username', '$password')" | \
  java -jar ../artifacts/jenkins-cli.jar -auth admin:$pat -s http://localhost:8080/ groovy =
