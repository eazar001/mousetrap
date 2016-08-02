extern crate x11;
use x11::xlib::*;

use std::mem::zeroed;
use std::ptr::null;
use std::os::raw::c_long;

pub fn grab_pointer(dpy: *mut Display,
                    win: Window,
                    owner_events: bool,
                    cursor: Cursor,
                    mask: u32) -> bool {

    let events = if owner_events { 1 } else { 0 };
    let status = unsafe {
        XGrabPointer(dpy, win, events, mask, GrabModeSync, GrabModeAsync, win, cursor, CurrentTime)
    };

    if status == 0 {
        unsafe { XAllowEvents(dpy, SyncPointer, CurrentTime) };
        true
    } else {
        false
    }
}

pub fn ungrab_pointer(dpy: *mut Display) {
    unsafe { XUngrabPointer(dpy, CurrentTime) };
}

pub fn replay_events(dpy: *mut Display, mask: c_long, event: &mut XEvent) {
    mask_event(dpy, mask, event);
    unsafe { XAllowEvents(dpy, ReplayPointer, CurrentTime) };
}

pub fn init_xevent() -> XEvent {
    unsafe { zeroed() }
}

pub fn mask_event(dpy: *mut Display, mask: c_long, event_return: *mut XEvent) {
    unsafe { XMaskEvent(dpy, mask, event_return) };
}

pub fn null_cursor(dpy: *mut Display, dw: Drawable) -> Cursor {
    let mut color: XColor = unsafe { zeroed() };
    let pixmap: Pixmap = unsafe { XCreatePixmap(dpy, dw, 1, 1, 1) };
    let cursor: Cursor = unsafe {
        XCreatePixmapCursor(dpy, pixmap, pixmap, &mut color, &mut color, 0, 0)
    };

    unsafe { XFreePixmap(dpy, pixmap) };
    cursor
}

pub fn free_cursor(dpy: *mut Display, cursor: Cursor) -> i32 {
    unsafe { XFreeCursor(dpy, cursor) }
}

pub fn close_display(display: *mut Display) {
    unsafe { XCloseDisplay(display) };
}

pub fn root_window(display: *mut Display, screen: i32) -> Window {
    unsafe { XRootWindow(display, screen) }
}

pub fn default_screen(display: *mut Display) -> i32 {
    unsafe { XDefaultScreen(display) }
}

pub fn open_display() -> *mut Display {
    unsafe { XOpenDisplay(null()) }
}
