#!/bin/bash
. .venv/bin/activate
set -a && . ./.env && set +a

if hostname -I 2>/dev/null; then
  # display URL for access to the local server.
  echo local IP address : http://localhost:8000
  echo host IP address : http://$(hostname -I) | awk -F' ' '{print $1}'
else
  # on some systems, hostname -I doesn't work. show below message instead.
  echo local IP address : http://localhost:8000
  echo host IP address : failed to get host address. please check IP address manually.
fi

python -m http.server 8000
