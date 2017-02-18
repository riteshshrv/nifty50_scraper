#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from redis import StrictRedis

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import TimeoutException

from .settings import CONFIG
from .exceptions import ResourceNotFound

# TODO: Might have to use "pyvirtualdisplay" or "xvfb" for headless browser


class ScrapeNifty50(object):
    """
    Class to scrape "Nifty 50" table values
    """
    URL = 'https://www.nseindia.com/live_market/dynaContent/live_analysis/top_gainers_losers.htm'  # noqa
    GAINERS_TABLE_ID = 'topGainers'
    LOSERS_TABLE_ID = 'topLosers'
    GAINERS_TAB_ID = 'tab7'
    LOSERS_TAB_ID = 'tab8'

    def __init__(self, *args, **kwargs):
        self.browser = self._get_browser()
        self.parser = BeautifulSoup
        self.db = StrictRedis(
            CONFIG['REDIS_HOST'], CONFIG['REDIS_PORT'], CONFIG['REDIS_DB']
        )

    def _get_browser(self):
        """
        Initialize Chrome webdriver and point to NSE page
        """
        wd = webdriver.Chrome()
        wd.get(self.URL)
        return wd

    def _get_page_source_with(self, element_id):
        """
        Make sure the requested element is available and return a parser
        (BeautifulSoup) object
        """
        try:
            # 3 seconds is ample time for visibility
            WebDriverWait(self.browser, 3).until(
                EC.visibility_of_element_located((By.ID, element_id))
            )
        except TimeoutException:
            raise ResourceNotFound(
                'Element with ID %s was not found' % element_id
            )
        else:
            html_page = self.browser.page_source
            return self.parser(html_page)

    def get_gainers(self):
        """
        Scrape for Nifty50 gainers
        """
        # Make sure to click gainers tab as data is only availabe for
        # currently active tab
        self.browser.find_element_by_id(self.GAINERS_TAB_ID).click()
        gainers_table = self._get_page_source_with(self.GAINERS_TABLE_ID).find(
            'table', {'id': self.GAINERS_TABLE_ID}
        )
        # TODO: Implement and use descriptor to store this data as encoded
        # json into db (Redis)
        return gainers_table

    def get_losers(self):
        """
        Scrape for Nifty50 losers
        """
        # Make sure to click losers tab as data is only availabe for
        # currently active tab
        self.browser.find_element_by_id(self.LOSERS_TAB_ID).click()
        losers_table = self._get_page_source_with(self.LOSERS_TABLE_ID).find(
            'table', {'id': self.LOSERS_TABLE_ID}
        )
        # TODO: Implement and use descriptor to store this data as encoded
        # json into db (Redis)
        return losers_table
