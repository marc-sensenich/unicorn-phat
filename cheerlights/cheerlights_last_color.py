#!/usr/bin/env python3

import urllib.request
from time import sleep
from typing import List

HAS_UNICORNHAT = True

try:
    import unicornhat
except ImportError:
    HAS_UNICORNHAT = False

CHEERLIGHTS_COLORS = {
    "red": (255, 0, 0),
    "green": (0, 128, 0),
    "blue": (0, 0, 255),
    "cyan": (0, 255, 255),
    "white": (255, 255, 255),
    "oldlace": (253, 245, 230),
    "purple": (128, 0, 128),
    "magenta": (255, 0, 255),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
    "pink": (255, 192, 203),
}


def cheerlights_text_to_rgb(cheerlights_text: str) -> List[int]:
    return CHEERLIGHTS_COLORS.get(cheerlights_text, CHEERLIGHTS_COLORS["white"])


def get_cheerlights_text() -> str:
    with urllib.request.urlopen('http://api.thingspeak.com/channels/1417/field/1/last.txt') as response:
        return response.read().decode('utf-8')


def cheerlights_last_color():
    current_cheerlights_color_text = get_cheerlights_text()
    print(f"The current CheerLights color is {current_cheerlights_color_text}")
    current_cheerlights_rgb = cheerlights_text_to_rgb(current_cheerlights_color_text)
    if HAS_UNICORNHAT:
        unicornhat.set_all(current_cheerlights_rgb)
        unicornhat.show()
    sleep(5)


def stop():
    """
    Signal handler to turn off the Unicorn pHAT
    """
    if HAS_UNICORNHAT:
        unicornhat.off()


if __name__ == '__main__':
    print('Press Ctrl-C to exit the program')
    if HAS_UNICORNHAT:
        unicornhat.set_layout(unicornhat.PHAT)
        unicornhat.brightness(0.4)

    try:
        while True:
            cheerlights_last_color()
    except KeyboardInterrupt:
        stop()
