#!/bin/bash

username=$1
repo=$2

props="../artifacts/properties_file.props"
repo_name=$(echo $repo | awk -F'/' '{print $5}' | awk -F'.' '{print $1}')  # Get only repo name from repo link

# Empty properties file (this is the case for a new repo)
> $props

echo "REPO=$2" >> $props
echo "REPO_NAME=$repo_name" >> $props

# Get primary language from repo (i.e. cimple's would be Python)
language=`gh api repos/$username/$repo_name/languages | jq 'to_entries | max_by(.value) | .key'`
echo "LANGUAGE=$language" >> $props

# Check if requirements.txt exists
requirements=$(gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  /repos/$username/$repo_name/contents/requirements.txt)
req_exit_code=$?

# If requirements.txt doesn't exist, we have to ask the user for input.
#TODO: maybe check which type of packages these are (apt, pip, whatever else) ----> To be done in job MAYBE (requirements stage).
if [ $req_exit_code -eq 0 ]; then
  echo "requirements.txt found!"
  # url=$(echo $requirements | jq -r '.download_url')
  echo "REQUIREMENTS=true" >> $props
  # wget -O "../artifacts/$repo/requirements.txt" $url
else
  echo "REQUIREMENTS=false" >> $props
fi

# Check if readme exists
readme=$(gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  /repos/$username/$repo_name/readme)
readme_exit_code=$?
echo "readme:$readme_exit_code"

# If readme exists, parse it for build instructions
if [ $readme_exit_code -eq 0 ]; then
  echo "README found!"
  url=$(echo $readme | jq -r '.download_url')
  wget -O "../artifacts/readme" $url
  check_instructions=$(cat ../artifacts/readme | grep -Eio "build|instructions|install|run")
  rm ../artifacts/readme
  if [ "$check_instructions" != "" ]; then
    echo "INSTRUCTIONS=true" >> $props
  else
    echo "INSTRUCTIONS=false" >> $props
  fi
fi

# Echo to shell to extract these values in case we need user input
# exit codes: 0 for found, non-zero (1) for not found
echo "requirements:$req_exit_code"
echo "instructions:$readme_exit_code"
