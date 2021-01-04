#!/usr/bin/env bash

SERVICE_TARGET=busy-light-slack-status.service

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

systemctl stop ${SERVICE_TARGET}
systemctl disable ${SERVICE_TARGET}
shred /etc/systemd/system/${SERVICE_TARGET} && rm $_
shred /etc/systemd/system/${SERVICE_TARGET}.d/override.conf && rm $_
rmdir /etc/systemd/system/${SERVICE_TARGET}.d
