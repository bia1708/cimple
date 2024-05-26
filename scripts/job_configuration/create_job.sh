#!/bin/bash

repo=$1
jenkins_cli=$2
url=$3
username=$4
pat=$5

repo_name=$(echo "$repo" | awk -F'/' '{print $5}' | awk -F'.' '{print $1}')  # Get only repo name from repo link

# Use jenkins-job-builder with newly generated .ini file and yaml script to (re)generate seeder pipeline
# By this point, seeder pipline code is loaded with the right script for the given type of project
jenkins-jobs --conf ./artifacts/jenkins_jobs.ini update ./scripts/job_configuration/seeder.yml

# Run seeder to generate job
java -jar "$jenkins_cli" -auth "$username":"$pat" -s "$url" build seeder -p REPO="$repo" -p REPO_NAME="$repo_name" -f

# First run of the job
java -jar "$jenkins_cli" -auth "$username":"$pat" -s "$url" build "$repo_name" -f