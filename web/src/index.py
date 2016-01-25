#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
import ConfigParser
from myapp import baseApp
from rms   import RMS
from flask import Flask, render_template, g

from flask.ext.socketio import SocketIO, emit
from logging.handlers import RotatingFileHandler

import datetime
import json
import logging
import time

from carreralib import ControlUnit
import redis

r = redis.Redis(host = '127.0.0.1', port = 6379)

app = Flask(
    __name__,
    static_folder = baseApp.config.get("WebServer", "StaticDir"),
    static_url_path = "/static",
    template_folder = baseApp.config.get("WebServer", "TemplateDir")
)
socketio = SocketIO(app)
log = logging.getLogger(__name__)

#cu = ControlUnit(baseApp.config.get("Serial", "Device"))
#rms = RMS(cu)

@app.route('/')
def index():
    page = open('../templates/index.html').read()
    page = page.replace(
        "__WS__", "ws://%s:%s/ws" % (
        baseApp.config.get("WebServer", "Host"),
        baseApp.config.getint("WebServer", "Port"))
    )
    return page

@socketio.on('connect', namespace='/ws')
def connect():
    log.info("Client connected to the server. ")

@socketio.on('send:request', namespace='/ws')
def request(message):
    #print "RMS: >>>>> %s" % rms
    #data = rms.cu.request()
    #if isinstance(data, ControlUnit.Status):
    #    #log.info("Handle Status %s " % str(data))
    #    rms.handleStatus(data)
    #elif isinstance(data, ControlUnit.Timer):
    #    #print data
    #    #log.info("Handle Timer %s " % str(data))
    #    rms.handleTimer(data)
    data = r.get('drivers')
    #data = rms.getData()
    #print data
    emit('init', data, broadcast = True)

@socketio.on('send:start', namespace='/ws')
def sendStart(message):
    log.info("Handle Start ... ")
    r.set("start", 1)
    #rms.cu.start()

@socketio.on('send:reset', namespace='/ws')
def reset(message):
    log.info("Handle Reset ... %s" % message)
    r.set("reset", 1)
    #rms.reset()

@socketio.on('disconnect', namespace='/ws')
def disconnect():
    log.info("Client disconnected from the server clients connected")

if __name__ == '__main__':
    app.debug = bool(baseApp.config.getint("Log", "AppDebug"))


    handler = RotatingFileHandler(baseApp.config.get("Log", "LogFile"), maxBytes = 10000, backupCount = 1)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s %(name)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    logging.basicConfig(level = logging.INFO)

    socketio.run(
        app,
        baseApp.config.get("WebServer", "Host"),
        baseApp.config.getint("WebServer", "Port"),
        debug = bool(baseApp.config.getint("Log", "AppDebug"))
    )
