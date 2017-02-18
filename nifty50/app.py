#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import cherrypy
from redis import StrictRedis

from .settings import CONFIG
from .utils import abs_file_path

__all__ = ['NseVisualizer']


class NseVisualizer(object):
    """
    NSE Visualizer
    """
    def __init__(self):
        self.db = StrictRedis(
            CONFIG['REDIS_HOST'], CONFIG['REDIS_PORT'], CONFIG['REDIS_DB']
        )

    @cherrypy.expose
    def index(self):
        return file("index.html")

    @cherrypy.expose
    def get(self, timestamp=None):
        """
        Find and return data for given timestamp
        """
        try:
            timestamp = int(timestamp)
        except TypeError:
            timestamp = 0

        key = 'data:%s' % timestamp
        data = self.db.hgetall(key)

        return json.dumps(data)


if __name__ == '__main__':
    """
    Start CherryPy Engine
    """
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
