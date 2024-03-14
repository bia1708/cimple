#!/bin/bash

# Install smee dependencies (one time)
packages=$(npm list)
# if [ echo $packages | grep]
npm install --global node@latest
npm install --global smee-client

tunnel=$(curl -X GET https://smee.io/new | awk '{print $5}')
echo "tunnel:$tunnel"


smee --url $tunnel --path /github-webhook/ --port 8080