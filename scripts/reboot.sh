#!/bin/bash
python3 -m venv .venv && . .venv/bin/activate
# git pull origin main
# pip install -r requirements.txt
echo "System will reboot in 30 seconds..." & (sleep 30s && sudo reboot) &
