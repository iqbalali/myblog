#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from configs.pelicanconf import *

TESTING=False
LOAD_CONTENT_CACHE = True

SITEURL = 'http://staging.ryanmo.co'
EXTRA_PATH_METADATA = {}
STATIC_PATHS = [
    'images',
    'downloads',
    'json'
]
RELATIVE_URLS = False

FEEDPRESS_RSS = None
FEED_ALL_RSS = None
CATEGORY_FEED_RSS = None
TAG_FEED_RSS = None
