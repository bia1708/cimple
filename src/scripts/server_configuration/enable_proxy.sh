#!/bin/bash

# Install nodejs
apt-get install nodejs -y

# Install smee-client
npm install --global smee-client

# Get a new tunnel from smee.io
tunnel=$(curl -X GET https://smee.io/new | awk '{print $5}')
echo "tunnel:$tunnel"

# Create systemd service for smee webhook forwarding
service_script=$'
[Unit]\n
Description=Smee Proxy\n
After=network.target jenkins.service\n
StartLimitIntervalSec=0\n
\n
[Service]\n
Type=simple\n
Restart=always\n
RestartSec=1\n
User=jenkins\n
ExecStart=smee --url $tunnel --path /github-webhook/ --port 8080\n
\n
[Install]\n
WantedBy=multi-user.target'

echo "$service_script" > /etc/systemd/system/smee.service

systemctl daemon-reload
systemctl enable smee.service
systemctl start smee.service