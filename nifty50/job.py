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
from .scrip import Scrip

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

    def get(self, type_='gainers'):
        """
        Common method for fetching data for given table type
        """
        tab_id = getattr(self, '%s_TAB_ID' % type_.upper())
        table_id = getattr(self, '%s_TABLE_ID' % type_.upper())

        # Make sure to click gainers tab as data is only availabe for
        # currently active tab
        self.browser.find_element_by_id(tab_id).click()
        table = self._get_page_source_with(table_id).find(
            'table', {'id': table_id}
        )
        # Skip the table header
        table = table[1:]
        scrips = [Scrip(tr).data for tr in table.find_all('tr')]

        return scrips
