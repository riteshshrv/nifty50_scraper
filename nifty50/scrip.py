#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


__all__ = ['Scrip']


class Scrip(object):
    """
    An object that implements a descriptor for scrip
    """
    FIELDS = [
        'symbol', 'ltp', 'percent_change', 'traded_qty', 'value',
        'open', 'high', 'low', 'previous_close', 'latest_ex_date'
    ]

    def __init__(self, bs4_tr):
        self.values = [td.text for td in bs4_tr.find_all('td')[:-1]]
        self.data = self._get_fields_dict()

    def _get_fields_dict(self):
        """
        Covert to key-value pairs
        """
        data = {key: value for key, value in zip(self.FIELDS, self.values)}
        return data

    @property
    def json(self):
        return json.dumps(self.data)

    def pretty(self):
        pattern = '{symbol} @ {ltp}'
        return pattern.format(**self.data)

    def __str__(self):
        return self.pretty()

    def __repr__(self):
        return self.pretty()
