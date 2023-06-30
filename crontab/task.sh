#!/bin/bash

# print date and time
echo "Current date and time: $(date)"

cd /app/

# run bot
echo "Running bot..."

# run script and pass env variables
./.venv/bin/python ./src/main_bot.py
