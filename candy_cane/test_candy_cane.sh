#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [[ -z "${APP_SCRIPT_URL}" ]]; then
  echo "The environment variable 'APP_SCRIPT_URL' must be set"
  exit 1
fi

while :
do
  for i in {1..3}; do
    candy_cane_file="${DIR}/candy_cane_${i}.json"
    curl -X POST \
      --silent \
      $APP_SCRIPT_URL \
      -H 'Content-Type: application/json' \
      -d @$candy_cane_file > /dev/null
    sleep 0.25
  done
done