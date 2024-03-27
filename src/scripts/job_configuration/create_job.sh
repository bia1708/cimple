#!/bin/bash

# username=$1
# pat=$2
# jenkins_cli=$3
# url=$4

if [ ! -d /var/lib/jenkins/workspace/generator ]; then
  mkdir /var/lib/jenkins/workspace/generator
fi

cp scripts/job_configuration/job.groovy /var/lib/jenkins/workspace/generator/
cp ../artifacts/properties_file.props /var/lib/jenkins/workspace/unjob/

export REPO=bia
jenkins-jobs --conf ../artifacts/jenkins_jobs.ini update ./scripts/job_configuration/default_job.yml