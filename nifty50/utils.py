#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


def abs_file_path(rel_path):
    """
    Return full (absolute) file path for given relative path
    """
    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), rel_path
        )
    )
