#!/bin/bash

username=$1
repo=$2

rm -rf ../artifacts/$repo
# Check if requirements.txt exists
requirements=$(gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  /repos/$username/$repo/contents/requirements.txt)
exit_code=$?

# If requirements.txt doesn't exist, we have to ask the user for input.
echo "requirements:$exit_code"

#TODO: maybe check which type of packages these are (apt, pip, whatever else)
# if [ $exit_code -eq 0 ]; then
#   echo "requirements.txt found! Downloading file for parsing..."
#   url=$(echo $requirements | jq -r '.download_url')
#   echo $url
#   wget -O "../artifacts/$repo/requirements.txt" $url
# fi

# Check if readme exists
readme=$(gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  /repos/$username/$repo/readme)
exit_code=$?
echo "readme:$exit_code"

# If readme exists, parse it for build instructions/requirements
if [ $exit_code -eq 0 ]; then
  echo "README found! Downloading file for parsing..."
  url=$(echo $readme | jq -r '.download_url')
  wget -O "../artifacts/$repo/readme" $url
  cat ../artifacts/$repo/readme | grep -i requirements > ../artifacts/$repo/readme_requirements.txt
  if [ -z "$(cat ../artifacts/$repo/readme_requirements.txt)" ]; then
    echo "readme_requirements:1"
  else
    echo "readme_requirements:0"
  fi
fi

#TODO: maybe remove downloaded files, since they will be duplicated for the user
