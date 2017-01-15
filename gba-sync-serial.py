#!/usr/bin/env python

import serial
import socket
from sys import argv

ser = serial.Serial('/dev/serial0', baudrate=38400)    
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print "Connected:", ser

message = [0, 0, 0]
while True:
  i = 0
  while i < 3:
    data = ord(ser.read(1)) # read a byte
    if data >> 7 != 0:  
      i = 0      # status byte!   this is the beginning of a midi message!
    message[i] = data
    i += 1
    if i == 2 and message[0] >> 4 == 12:  # program change: don't wait for a
      message[2] = 0                      # third byte: it has only 2 bytes
      i = 3

  messagetype = message[0] >> 4
  messagechannel = (message[0] & 15) + 1
  note = message[1] if len(message) > 1 else None
  velocity = message[2] if len(message) > 2 else None

  #if messagetype == 9:    # Note on
  #  print 'Note on'
  #elif messagetype == 8:  # Note off
  #  print 'Note off'            
  #elif messagetype == 12: # Program change
  #  print 'Program change'
  #else:
  #  print "message", messagetype, messagechannel, note, velocity

  if "--debug" in argv:
    print "message", messagetype, messagechannel, note, velocity
  
  sock.sendto(" ".join([hex(x) for x in message]) + ";\n", ("127.0.0.1", 42242))

