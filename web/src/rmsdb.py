#!/usr/bin/env python
# -*- coding: utf-8 -*-
from carreralib import ControlUnit
from carreralib.connection import TimeoutError

import ConfigParser
from myapp import baseApp
from time import sleep

import json
import logging
import redis

r = redis.Redis(host = '127.0.0.1', port = 6379)
log = logging.getLogger(__name__)

def posgetter(driver):
    return (-driver.laps, driver.time)

def formattime(time, longfmt = False):
    if time is None:
        return 'n/a'
    s = time // 1000
    ms = time % 1000

    if not longfmt:
        return '%d.%03d' % (s, ms)
    elif s < 3600:
        return '%d:%02d.%03d' % (s // 60, s % 60, ms)
    else:
        return '%d:%02d:%02d.%03d' % (s // 3600, (s // 60) % 60, s % 60, ms)

class Driver(object):
    def __init__(self, num):
        self.num = num
        self.time = None
        self.laptime = None
        self.bestlap = None
        self.laps = 0
        self.pits = 0
        self.fuel = 0
        self.pit = False

    def newlap(self, timer):
        if self.time is not None:
            self.laptime = timer.timestamp - self.time
            if not self.bestlap or self.laptime < self.bestlap:
                self.bestlap = self.laptime
            self.laps += 1
        self.time = timer.timestamp

class RMS(object):

    def __init__(self, cu):
        self.cu = cu
        self.reset()

    def update(self):
        data = self.getData()
        r.set('drivers', data)

        start = r.get("start")
        if start == "1":
            self.cu.start()
            r.set("start", 0)

        reset = r.get("reset")
        if reset == "1":
            self.reset()
            r.set("reset", 0)

    def getData(self):
        rows = list()
        drivers = [driver for driver in self.drivers if driver.time]
        for pos, driver in enumerate(sorted(drivers, key=posgetter), start=1):
            if pos == 1:
                leader = driver
                t = formattime(driver.time - self.start, True)
            elif driver.laps == leader.laps:
                t = '+%ss' % formattime(driver.time - leader.time)
            else:
                gap = leader.laps - driver.laps
                t = '+%d Lap%s' % (gap, 's' if gap != 1 else '')
            rows.append({
                "pos"     : pos,
                "num"     : driver.num if driver.num < 7 else 'AUT',
                "time"    : t,
                "laps"    : driver.laps,
                "lapTime" : formattime(driver.laptime),
                "bestLap" : formattime(driver.bestlap),
                "fuel"    : driver.fuel / 15.0,
                "pit"     : driver.pits
            })
        return json.dumps({
            "rows" : rows,
            "start" : self.status.start,
            "mode" : self.status.mode
        })

    def run(self):
        while True:
            sleep(0.1)
            try:
                data = self.cu.request()
                #if data == last:
                #    continue
                if isinstance(data, ControlUnit.Status):
                    self.handleStatus(data)
                elif isinstance(data, ControlUnit.Timer):
                    self.handleTimer(data)
                else:
                    pass
                last = data
            except TimeoutError, e:
                raise
            #except IOError as e:
            #    if e.errno != errno.EINTR:
            #        raise
            self.update()

    def reset(self):
        self.drivers = []
        for num in range(1, 9):
            d = Driver(num)
            self.drivers.append(d)
        self.maxlaps = 0
        self.start = None
        # discard remaining timer messages
        status = self.cu.request()
        while not isinstance(status, ControlUnit.Status):
            status = self.cu.request()
        self.status = status
        # reset cu timer
        #self.cu.reset()
        # reset position tower
        #self.cu.clrpos()

    def handleStatus(self, status):
        for driver, fuel in zip(self.drivers, status.fuel):
            driver.fuel = fuel
        for driver, pit in zip(self.drivers, status.pit):
            if pit and not driver.pit:
                driver.pits += 1
            driver.pit = pit
        self.status = status

    def handleTimer(self, timer):
        driver = self.drivers[timer.address]
        driver.newlap(timer)
        if self.maxlaps < driver.laps:
            self.maxlaps = driver.laps
            # position tower only handles 250 laps
            self.cu.setlap(self.maxlaps % 250)
        if self.start is None:
            self.start = timer.timestamp

def createInstance():
    cu = ControlUnit(baseApp.config.get("Serial", "Device"), timeout=3)
    return RMS(cu)

from time import sleep
if __name__ == "__main__":
    rms = createInstance()
    while True:
        try:
            rms.run()
        except TimeoutError:
            sleep(3)
            #print "Timeout error"
            rms = createInstance()

