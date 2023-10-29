#!/bin/bash
. .venv/bin/activate
set -a && . ./.env && set +a
python3 ./src/main.py
