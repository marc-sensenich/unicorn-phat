#!/usr/bin/env python3

import argparse
import re
import signal
import time
from os import getenv

from requests import Session
from requests.adapters import HTTPAdapter

HAS_UNICORNHAT = True

try:
    import unicornhat
except ImportError:
    HAS_UNICORNHAT = False


class SlackUser:
    BUSY_STATUS_REGEX = r"In a meeting|In a call"

    def __init__(self, slack_token):
        self.slack_token = slack_token
        self.session = Session()
        self.session.mount('https://slack.com', HTTPAdapter(max_retries=3))

    def _get_slack_user_profile(self):
        request_data = {
            'token': self.slack_token
        }
        resp = self.session.post('https://slack.com/api/users.profile.get', data=request_data)
        return resp.json()

    def is_busy(self):
        user_profile = self._get_slack_user_profile()
        status_text = user_profile.get('profile', {}).get('status_text', '')
        return bool(re.match(self.BUSY_STATUS_REGEX, status_text, re.MULTILINE | re.IGNORECASE))


def stop_signal(signal, frame):
    if HAS_UNICORNHAT:
        unicornhat.off()
    exit(0)


def main():
    argument_parser = argparse.ArgumentParser(
        description="Use a Unicorn pHAT to designate busy status based on a user's Slack status")
    argument_parser.add_argument('--delay', type=int,
                                 help='Delay between checking the Slack API for busy status in seconds', default=10)
    argument_parser.add_argument('--slack-token', type=str,
                                 help='The Slack user token with the OAuth scope user.profiles.get. Can be set from the environment variable SLACK_TOKEN.',
                                 default=getenv('SLACK_TOKEN', None))
    argument_parser.add_argument('--busy-color', type=int, choices=range(0, 256),
                                 help="The RGB color to set when you're busy, must be between 0 and 255", metavar='255',
                                 nargs=3, default=[184, 29, 19])
    argument_parser.add_argument('--free-color', type=int, choices=range(0, 256),
                                 help="The RGB color to set when you're free, must be between 0 and 255", metavar='255',
                                 nargs=3, default=[0, 132, 80])
    args = argument_parser.parse_args()

    signal.signal(signal.SIGINT, stop_signal)
    signal.signal(signal.SIGTERM, stop_signal)

    # Initialize Unicornhat
    if HAS_UNICORNHAT:
        unicornhat.set_layout(unicornhat.PHAT)
        unicornhat.brightness(0.35)

    while True:
        # Get Slack Status Text
        slack_user = SlackUser(args.slack_token)
        if slack_user.is_busy():
            if HAS_UNICORNHAT:
                unicornhat.set_all(*args.busy_color)
                unicornhat.show()
        else:
            if HAS_UNICORNHAT:
                unicornhat.set_all(*args.free_color)
                unicornhat.show()

        time.sleep(args.delay)


if __name__ == '__main__':
    main()
