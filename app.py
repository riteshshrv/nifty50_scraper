#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cherrypy

from nifty50 import NseVisualizer
from nifty50.utils import abs_file_path


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
