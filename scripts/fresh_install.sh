#!/bin/bash

username=$1
password=$2

if [ $(which jenkins) ]; then
	echo "Jenkins already exists on this device."
	exit 1
fi

# Install java
sudo apt update
sudo apt install -y curl fontconfig openjdk-17-jre

# Install jenkins
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update
sudo apt install jenkins

# Enable service
sudo systemctl daemon-reload
sudo systemctl enable jenkins

# Start jenkins
sudo systemctl start jenkins &

# Auth for the first time
sudo wget http://192.168.1.219:8080/jnlpJars/jenkins-cli.jar
pat=$(sudo cat /var/lib/jenkins/secrets/initialAdminPassword)
#java -jar jenkins-cli.jar -s http://192.168.1.219:8080 -auth admin:$pat

echo "jenkins.model.Jenkins.instance.securityRealm.createAccount('\""$username"\"', '\""$password"\"')" | java -jar jenkins-cli.jar -auth admin:$pat -s http://192.168.1.219:8080/ groovy =
