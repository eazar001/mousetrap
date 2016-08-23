#!/usr/bin/env python

import threading
import argparse
import os
import sys
from threading import Event
from Xlib.display import Display
from Xlib import X
from Xlib.ext import record
from Xlib.protocol import rq

"""
Much of this application was derived from the example code that can be found at
https://github.com/python-xlib/python-xlib/blob/master/examples/record_demo.py

The event recording code in that script has been refitted for mousetrap's specific purposes
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t",
                        "--timeout",
                        help="specify a timeout interval between 1 and infinity",
                        type=int,
                        required=True)

    args = parser.parse_args()

    display = Display()

    if not display.has_extension('XFIXES'):
        if display.query_extension('XFIXES') is None:
            print('XFIXES extension not supported', file=sys.stderr)
            return 1

    xfixes_version = display.xfixes_query_version()
    print('Found XFIXES version %s.%s' % (
        xfixes_version.major_version,
        xfixes_version.minor_version,
    ), file=sys.stderr)

    screen = display.screen()

    mouse = Mouse(display, screen, args.timeout)
    mouse.start()

    run_sensor(mouse)

def run_sensor(mouse):
    record_dpy = Display()

    # Check if the extension is present
    if not record_dpy.has_extension("RECORD"):
        print("RECORD extension not found")
        sys.exit(1)

    r = record_dpy.record_get_version(0, 0)
    print("RECORD extension version %d.%d" % (r.major_version, r.minor_version))


    # Create a recording context; we only want key and mouse events
    ctx = record_dpy.record_create_context(
        0,
        [record.AllClients],
        [{
                'core_requests': (0, 0),
                'core_replies': (0, 0),
                'ext_requests': (0, 0, 0, 0),
                'ext_replies': (0, 0, 0, 0),
                'delivered_events': (0, 0),
                'device_events': (X.ButtonPress, X.MotionNotify),
                'errors': (0, 0),
                'client_started': False,
                'client_died': False,
        }])

    # Enable the context; this only returns after a call to record_disable_context,
    # while calling the callback function in the meantime
    record_dpy.record_enable_context(ctx, record_callback(record_dpy, mouse))

    # Finally free the context
    record_dpy.record_free_context(ctx)

def record_callback(record_dpy, mouse):
    def rc(reply):
        if reply.category != record.FromServer:
            return
        if reply.client_swapped:
            print("* received swapped protocol data, cowardly ignored")
            return
        if not len(reply.data) or reply.data[0] < 2:
            # not an event
            return

        data = reply.data

        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data,
                                                                 record_dpy.display,
                                                                 None,
                                                                 None)

            if event.type == X.ButtonPress:
                mouse.activity.set()
            elif event.type == X.MotionNotify:
                mouse.activity.set()

    return rc

class Mouse:
    def __init__(self, display, screen, timeout):
        self.activity = Event()
        self.timeout = timeout
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
                self.activity.clear()
            else:
                screen.root.xfixes_hide_cursor()
                display.sync()
                self.activity.wait()
                self.activity.clear()

                screen.root.xfixes_show_cursor()
                display.sync()


if __name__ == "__main__":
    main()
