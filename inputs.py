#!/usr/bin/env python

from threading import Thread, Event
import struct
import sys
import socket
import keyboard

keymap = {
    ",": "comma",
    ".": "dot",
    ";": "colon",
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send(msg):
    sock.sendto(msg, ("127.0.0.1", 11031))

def out(event):
    m = "key", "key_" + keymap.get(event.name, event.name), {"up": 0, "down": 1}[event.event_type], event.scan_code, event.time
    send(" ".join([str(x) for x in m]) + "\n")

def mousewait(f):
    buf = f.read(3);
    button = ord( buf[0] );
    bLeft = button & 0x1;
    bMiddle = int(( button & 0x4 ) > 0);
    bRight = int(( button & 0x2 ) > 0);
    x,y = struct.unpack( "bb", buf[1:] );
    m = "mouse", bLeft, bMiddle, bRight, x, y
    send(" ".join([str(x) for x in m]) + "\n")

def mouse(exit):
    f = open("/dev/input/mice", "rb");
    while not exit.is_set():
        mousewait(f)

exit = Event()

t = Thread(target=mouse, args=(exit,))
t.start()

keyboard.hook(out)
try:
    keyboard.wait()
except KeyboardInterrupt:
    exit.set()
    sys.exit()
