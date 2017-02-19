#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cherrypy

from nifty50 import NseVisualizer
from nifty50.utils import abs_file_path

from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 600))
display.start()


global_conf = {"global": {
    "server.socket_host": '0.0.0.0',
    "server.socket_port": 8000,
}}
cherrypy.config.update(global_conf)
cherrypy.tree.mount(
    NseVisualizer(), "/", {
        "/static": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": abs_file_path('static'),
        }
    }
)
cherrypy.engine.start()
cherrypy.engine.block()


display.stop()
