#!/bin/bash
python3 -m venv .venv && . .venv/bin/activate
git pull origin main
pip install -r requirements.txt
echo "Successfully upgraded. System will reboot in 20 seconds..."
(sleep 20 && sudo reboot) &
