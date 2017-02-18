#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


CONFIG = dict(
    SECRET_KEY=os.environ.get('SECRET', '4r32DE3S3-z22*9'),
    APP_DIR=os.path.abspath(os.path.dirname(__file__)),
    REDIS_HOST=os.environ.get('REDIS_URL', 'localhost'),
    REDIS_PORT=os.environ.get('REDIS_PORT', 6379),
    REDIS_DB=os.environ.get('REDIS_DB', 0),
)
