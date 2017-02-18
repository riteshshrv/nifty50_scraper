#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from redis import StrictRedis
from selenium import webdriver

from .settings import CONFIG

# TODO: Might have to use "pyvirtualdisplay" or "xvfb" for headless browser


class ScrapeNifty50(object):
    """
    Class to scrape "Nifty 50" table values
    """
    URL = 'https://www.nseindia.com/live_market/dynaContent/live_analysis/top_gainers_losers.htm'  # noqa
    GAINERS_TABLE_ID = 'topGainers'
    LOSERS_TABLE_ID = 'topLosers'

    def __init__(self, *args, **kwargs):
        self.browser = webdriver.Chrome()
        self.parser = BeautifulSoup
        self.db = StrictRedis(
            CONFIG['REDIS_HOST'], CONFIG['REDIS_PORT'], CONFIG['REDIS_DB']
        )

    def get_gainers(self):
        """
        Scrape for Nifty50 gainers
        """
        pass

    def get_losers(self):
        """
        Scrape for Nifty50 losers
        """
        pass
