#!/bin/bash

echo "Grabbing env variables..."

# get relevant env variables for contab job
touch /etc/environment
echo "OPENAI_API_KEY=${OPENAI_API_KEY}" > /etc/environment
echo "LINKEDIN_ORG_ID=${LINKEDIN_ORG_ID}" >> /etc/environment
echo "LINKEDIN_ACCESS_TOKEN=${LINKEDIN_ACCESS_TOKEN}" >> /etc/environment

# env >> /etc/environment

# load crontab
crontab crontab

# run cron job in foreground
cron -f