#!/bin/bash

# username=$1
# pat=$2
# jenkins_cli=$3
# url=$4
repo=$1

repo_name=$(echo $repo | awk -F'/' '{print $5}' | awk -F'.' '{print $1}')  # Get only repo name from repo link

if [ ! -d /var/lib/jenkins/workspace/seeder/$repo_name ]; then
  mkdir /var/lib/jenkins/workspace/seeder/$repo_name
fi

cp scripts/job_configuration/generate_job.groovy /var/lib/jenkins/workspace/seeder/$repo_name/
cp ../artifacts/properties_file.props /var/lib/jenkins/workspace/seeder/$repo_name  # Maybe I won't need this one anymore

jenkins-jobs --conf ../artifacts/jenkins_jobs.ini update ./scripts/job_configuration/default_job.yml