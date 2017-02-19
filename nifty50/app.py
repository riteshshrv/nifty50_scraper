#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import cherrypy
from cherrypy.process.plugins import BackgroundTask

from redis import StrictRedis

from .settings import CONFIG
from .utils import abs_file_path
from .job import ScrapeNifty50

__all__ = ['NseVisualizer']


class NseVisualizer(object):
    """
    NSE Visualizer
    """
    def __init__(self):
        self.scrapper = ScrapeNifty50()
        self.db = StrictRedis(
            CONFIG['REDIS_HOST'], CONFIG['REDIS_PORT'], CONFIG['REDIS_DB']
        )
        self.start_scheduled_job()

    def start_scheduled_job(self):
        """
        Scrape every 5 minutes in background and on a different thread
        """
        background_job = BackgroundTask(
            5 * 60, self.scrapper.persist, bus=cherrypy.engine
        )
        background_job.start()

    @cherrypy.expose
    def index(self):
        return file(abs_file_path('templates/index.html'))

    @cherrypy.expose
    def get(self, timestamp=None):
        """
        Find and return data for given timestamp
        """
        try:
            timestamp = int(float(timestamp))
        except TypeError:
            key = 'data'
        else:
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
