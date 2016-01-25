#!/usr/bin/env python

import serial

#SERIAL = "/dev/tty.usbserial-A90ZBP5L"
SERIAL = "/dev/tty.usbserial-A9IDXBNR"
ser = serial.Serial(SERIAL, 19200, stopbits = 1)


def readData():
    buff = []
    while 1:
        v = ser.read()
        if ord(v) == 10:
            print "". join(buff)
            return
        else:
            buff.append(v)

def readData1():
    print ord(ser.read())

while 1:
    readData1()
