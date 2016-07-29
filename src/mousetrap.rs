extern crate libc;
extern crate x11;

pub mod protocol;
use protocol::*;

use std::thread::sleep;
use std::time::Duration;
use std::ptr::null_mut;

use x11::xlib::*;

#[no_mangle]
pub extern fn hide_pointer() {
    let dpy = open_display();

    if dpy == null_mut() {
        panic!("can't open display")
    }

    let default = default_screen(dpy);
    let win: Window = root_window(dpy, default);

    let mask = ButtonPressMask | PointerMotionMask;
    let umask = mask as u32;
    let mut event: XEvent = init_xevent();
    let cursor = null_cursor(dpy, win);

    while !grab_pointer(dpy, win, false, cursor, umask) {
        sleep(Duration::new(1, 0));
    }

    replay_events(dpy, mask, &mut event);
    close_display(dpy);
}
