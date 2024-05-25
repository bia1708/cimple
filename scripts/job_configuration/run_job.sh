#!/bin/bash

jenkins_cli=$1
username=$2
pat=$3
url=$4
job=$5

java -jar $jenkins_cli -auth $username:$pat -s $url build $job
