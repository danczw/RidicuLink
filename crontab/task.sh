#!/bin/bash

echo "$(date '+%Y-%m-%d %H:%M:%S.%6N'): Running task.sh"

# set working directory
cd /app/

# run bot
./.venv/bin/python ./src/main_bot.py >> ./task.log 2>&1