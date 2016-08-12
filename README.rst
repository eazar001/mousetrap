mousetrap
=========

A utility that hides the mouse after a specified interval of time has elapsed
without activity.

What is this?
-------------

This is a small utility for linux desktops that hides the mouse during periods of inactivity. When the user does need to use the mouse again, the mouse pointer will be unhidden so that normal use can resume. Some users tend to get distracted when reading or working with a mouse pointer that sits over the content. This is very similar to programs like `hhp`, `hhpc`, `unclutter`, etc.

The process flow of `mousetrap` is as follows:

1. There is no activity for user-specified amount of time (i.e. 6 seconds)
2. Mouse is hidden
3. Mouse is used, and subsequently unhidden
4. Go back to step 1

If there is activity (i.e. click or movement) before the amount of time has elapsed in step 1, then the timer is reset and control remains in step 1.

What's wrong with the others?
-----------------------------

The other programs I've encountered had one or more of the following issues:

* Resets the timer on motion, but not on button presses
* Resets the timer on button presses, but not on motion
* Reactivates mouse on click, but does not register the click on the window
* Program predictably fails after a short amount of time
* Does not work on tiling window managers like mine (Xmonad WM)
* Works on tiling window managers, but fails to hide when sitting in between windows

The mere presence of any of the above issues is sufficient for me not to use such a program.

How do I install this?
----------------------

Do you have Arch Linux? Great, if so you can skip the rest of the instructions at the bottom and install it directly from the AUR: https://aur.archlinux.org/packages/mousetrap/

Otherwise, In order to build this application you need to install `Python` >= 3.0 (https://www.python.org)

After the installation, you may proceed to the first step below.

First, install with::

    $ python setup.py install

Then, assuming that the path you installed `mousetrap` to is in your `$PATH`::

    $ mousetrap -t 10


The `-t` flag specifies your preferred idle time, in seconds. All flag options are _absolutely_ mandatory.
