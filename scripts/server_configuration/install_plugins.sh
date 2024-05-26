#!/bin/bash
set -e

username=$1
pat=$2
jnlp=$3
url=$4

# Check user is authenticated
java -jar "$jnlp" -s "$url" -auth "$username:$pat" who-am-i

# Install all plugins needed by cimple. These are found in plugins.txt
file=$(find . -name "plugins.txt")
while IFS= read -r line
do
  echo "$line"
  java -jar "$jnlp" -s "$url" -auth "$username:$pat" -webSocket install-plugin "$line" -deploy </dev/null
done < "$file"

# Restart so that plugins can take effect
java -jar "$jnlp" -s "$url" -auth "$username:$pat" restart
