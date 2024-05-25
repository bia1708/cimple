#!/bin/bash
set -e

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

echo $jnlp $url $username $pat
java -jar $jnlp -s $url -auth $username:$pat restart
