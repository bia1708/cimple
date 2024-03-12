#!/bin/bash

username=$1
password=$2
url=$3

wget -o wget.log "$url/jnlpJars/jenkins-cli.jar" -P "../artifacts"
filename=$(cat wget.log | grep "Saving to" | awk '{print $3}' | tr -cd '[:print:]')
rm ./wget.log
echo "jnlp:$filename"