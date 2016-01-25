#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser
import getopt
import sys

options, r = getopt.getopt(sys.argv[1:], 'f', ['configfile='])



class BaseApp:

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        if len(r) == 1 :
            configFile = r[0]
        else:
            configFile = "../conf/config.conf"
        self.config.read(configFile)

baseApp = BaseApp()
