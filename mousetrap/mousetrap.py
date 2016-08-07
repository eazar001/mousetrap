#!/usr/bin/env python

import evdev
import threading
import argparse
import os
import sys
import re
from os import readlink
from evdev import InputDevice, categorize, ecodes
from threading import Event
from Xlib.display import Display


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t",
                        "--timeout",
                        help="specify a timeout interval between 1 and infinity",
                        type=int,
                        required=True)

    parser.add_argument("-d",
                        "--device_id",
                        help="specify a device id in /dev/input/by-id",
                        required=True)

    args = parser.parse_args()
    d = readlink('/dev/input/by-id/{}'.format(args.device_id))

    device = evdev.InputDevice(re.sub('../', '/dev/input/', d))

    display = Display()
    if not display.has_extension('XFIXES'):
        if display.query_extension('XFIXES') is None:
            print('XFIXES extension not supported', file=sys.stderr)
            return 1

    xfixes_version = display.xfixes_query_version()
    screen = display.screen()

    mouse = Mouse(display, screen, args.timeout, device)
    mouse.start()

    run_sensor(mouse)

def run_sensor(mouse):
    axis = ecodes.EV_REL
    button = ecodes.EV_KEY

    for event in mouse.device.read_loop():
        type = event.type

        # only true if a mouse button is down
        if type == button and categorize(event).keystate == 1:
            mouse.activity.set()

        # only true when mouse is moved on relative axis
        elif type == axis:
            mouse.activity.set()

class Mouse:
    def __init__(self, display, screen, timeout, device):
        self.activity = Event()
        self.timeout = timeout
        self.device = device
        self.display = display
        self.screen = screen

    def start(self):
        wait = threading.Thread(target=self.wait, args=())
        wait.start()

    def wait(self):
        screen = self.screen
        display = self.display

        while True:
            self.activity.wait(self.timeout)

            if self.activity.isSet():
                self.activity.clear();
            else:
                screen.root.xfixes_hide_cursor()
                display.sync()
                self.activity.wait()

                screen.root.xfixes_show_cursor()
                display.sync()


if __name__ == "__main__":
    main()
