# mousetrap

A utility that hides the mouse after a specified interval of time has elapsed
without activity.

### What is this?

This is a small utility for linux desktops that hide the mouse during periods
of inactivity. When the user does need to use the mouse again, the mouse pointer will be unhidden so that normal use can resume. Some users tend to get distracted when reading or working with a mouse pointer that sits over the content. This is very similar to programs like `hhp`, `hhpc`, `unclutter`, etc.

The process flow of `mousetrap` is as follows:

1. There is no activity for user-specified amount of time (i.e. 6 seconds)
2. Mouse is hidden
3. Mouse is used, and subsequently unhidden
4. Go back to step 1

If there is activity (i.e. click or movement) before the amount of time has elapsed in step 1, then the timer is reset and control remains in step 1.

### What's wrong with the others?

The other programs I've encountered had one or more of the following issues:

* Resets the timer on motion, but not on button presses
* Resets the timer on button presses, but not on motion
* Reactivates mouse on click, but does not register the click on the window
* Program predictably fails after a short amount of timer
* Does not work on tiling window managers like mine (Xmonad WM)
* Does not work on tiling window managers at all

The mere presence of any of the above issues is sufficient for me not to use such a program.

### How do I install this?

In order to build this application you need:
* The `Rust` compiler and its build tool, `Cargo` (https://www.rust-lang.org/)
* `Python` >= 3.5 (https://www.python.org)

First, give your user permission to read events from `/dev/input` with:
```
# gpasswd -a user input
```

Next, build and install with:
```
$ ./configure --prefix=/PATH/TO
$ make
$ make install
```

Next, located your device-id by doing and figure out which one is your mouse:
```
$ ls /dev/input/by-id
```
Finally, assuming that the path you installed `mousetrap` to is in your `$PATH`:
```
$ mousetrap -t 10 -d my_device_id
```
`my_device_id` is the filename you've determined corresponds to your mouse, from the previous step.

### Final notes

This was intended to work with my distro (Arch Linux). In theory, it should work with other linux distros as well. If not, I'm sorry. With a little persistence, I'm sure you can modify things to make it work with your distro if any of its idiosyncrasies stand in your way. Pull requests are welcome.

My mouse's device ID happens to be persistent. If your system setup for any reason is given to caprice in this respect, then you may need to look into writing a udev rule to ensure that these attributes remain consistent.

I'm sorry if there are too many steps or dependencies, but I only rewrote things to work where others (in my opinion) failed.
