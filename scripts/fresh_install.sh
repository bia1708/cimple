#!/bin/bash

username=$1
password=$2

sudo apt update
sudo apt install java-11-openjdk
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo apt install jenkins

sudo systemctl daemon reload
sudo systemctl enable jenkins

sudo systemctl start jenkins &