#!/bin/bash

username=$1
pat=$2
jnlp=$3
url=$4

jobs=$(java -jar $jnlp -s $url -auth $username:$pat list-jobs)

if [ "$jobs" == "" ]; then
    echo "None"
    exit 0
fi

echo "$jobs" | while read -r job; do
    job_url="$url/job/$job"
    job_status="$job_url/lastBuild/api/json"
    curl $job_url
done
