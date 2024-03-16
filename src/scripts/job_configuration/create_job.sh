#!/bin/bash

username=$1
pat=$2
jenkins_cli=$3
url=$4

# Get job template
java -jar $jenkins_cli -s $url -auth $username:$pat get-job template > template.xml