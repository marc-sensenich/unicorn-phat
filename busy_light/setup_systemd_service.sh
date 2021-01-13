#!/usr/bin/env bash

SERVICE_TARGET=busy-light-slack-status.service

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

if [[ -z "${SLACK_TOKEN}" ]]; then
  echo "The environment variable 'SLACK_TOKEN' must be set to a Slack API user token with the users.profile.get OAuth permission"
  exit 1
fi

(cd /etc/systemd/system/ && curl --silent -O https://raw.githubusercontent.com/marc-sensenich/unicorn-phat/busy-light/busy_light/busy-light-slack-status.service)

mkdir -p /etc/systemd/system/${SERVICE_TARGET}.d/

cat <<EOF > /etc/systemd/system/${SERVICE_TARGET}.d/override.conf
[Service]
Environment='SLACK_TOKEN=${SLACK_TOKEN}'
EOF

mkdir -p /usr/local/lib/busy_light
(cd $_ && curl --silent -O https://raw.githubusercontent.com/marc-sensenich/unicorn-phat/busy-light/busy_light/slack_status.py)

systemctl daemon-reload
systemctl enable ${SERVICE_TARGET}
systemctl restart ${SERVICE_TARGET}