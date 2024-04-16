#!/bin/bash

repo=$1
jenkins_cli=$2
url=$3
username=$4
pat=$5

repo_name=$(echo $repo | awk -F'/' '{print $5}' | awk -F'.' '{print $1}')  # Get only repo name from repo link

if [ ! -d /var/lib/jenkins/workspace ]; then
  mkdir /var/lib/jenkins/workspace
  chown -R jenkins:jenkins /var/lib/jenkins/workspace
fi

if [ ! -d /var/lib/jenkins/workspace/seeder ]; then
  mkdir /var/lib/jenkins/workspace/seeder
  chown -R jenkins:jenkins /var/lib/jenkins/workspace/seeder
fi

if [ ! -d /var/lib/jenkins/workspace/$repo_name ]; then
  mkdir /var/lib/jenkins/workspace/$repo_name
  chown -R jenkins:jenkins /var/lib/jenkins/workspace/$repo_name
fi

language=$(cat ../artifacts/properties_file.props | grep "LANGUAGE" | awk -F'=' '{ print $2 }' | sed 's/"//g')
if [ ${language,,} == "python" ]; then
  cp scripts/job_configuration/generate_job_python.groovy /var/lib/jenkins/workspace/seeder/generate_job.groovy
fi

# Remove this in the end
cp scripts/job_configuration/generate_job_python.groovy /var/lib/jenkins/workspace/seeder/generate_job.groovy

cp ../artifacts/properties_file.props /var/lib/jenkins/workspace/$repo_name
chown -R jenkins:jenkins /var/lib/jenkins/workspace/$repo_name
chown -R jenkins:jenkins /var/lib/jenkins/workspace/seeder

existing_jobs=$(java -jar $jenkins_cli -auth $username:$pat -s $url list-jobs)

if [ "$(echo $existing_jobs | grep "seeder")" == "" ]; then
  jenkins-jobs --conf ../artifacts/jenkins_jobs.ini update ./scripts/job_configuration/seeder.yml
fi

# Run seeder to generate job
java -jar $jenkins_cli -auth $username:$pat -s $url build seeder -p REPO=$repo -p REPO_NAME=$repo_name -f

# First run of the job
java -jar $jenkins_cli -auth $username:$pat -s $url build $repo_name -f