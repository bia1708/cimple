#!/bin/bash

npm install --global node@latest
npm install --global smee-client

tunnel=$(curl -X GET https://smee.io/new | awk '{print $5}')
echo $tunnel

smee --url $tunnel --path /github-webhook/ --port 8080