#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os
import sys
sys.path.append(os.curdir)
from configs.pelicanconf import *


DELETE_OUTPUT_DIRECTORY = True
LOAD_CONTENT_CACHE = False

SITEURL = 'https://ryanmo.co'
RELATIVE_URLS = False

FEEDPRESS_RSS = 'http://feedpress.me/ryanmoco'
FEED_ALL_RSS = 'feed.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'
TAG_FEED_RSS = 'feeds/%s.rss.xml'
RSS_FEED_SUMMARY_ONLY = False

# Social widget
SOCIAL = (
    ('Twitter', 'http://twitter.com/rjames86'),
    ('Github', 'http://www.github.com/rjames86'),
    ('RSS', FEEDPRESS_RSS),
    ('Email', 'mailto:blog@ryanmo.co')
)

PLUGINS.extend([
    'taglist',
    'related_posts',
    'latest_url',
    'search_content_generator',
    'bigfoot_footnotes',
    'all_articles_json',
])
STATIC_PATHS.append('json')

ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}'

# Theme

TESTING = False
DISQUS_SITENAME = 'rjames86'
PIWIK_ANALYTICS = True

# Plugins

# JSON Feed
SITE_FAVICON = SITEURL + '/images/favicon.png'
