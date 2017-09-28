#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os
import sys

from markdown.extensions.codehilite import CodeHiliteExtension

BASE_BLOG_PATH = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))

sys.path.append(os.path.join(BASE_BLOG_PATH, 'pelican_site'))

# Set up some path names
CONTENT_PATH = os.path.join(BASE_BLOG_PATH, 'content')
ALL_POSTS_PATH = os.path.join(CONTENT_PATH, 'posts')
LISTS_PATH = os.path.join(ALL_POSTS_PATH, 'Lists')
IMAGES_PATH = os.path.join(CONTENT_PATH, 'images')
THEME_PATH = os.path.join(BASE_BLOG_PATH, 'pelican_site', 'theme')

# Get a list of all the articles in Lists
# This is so that we can inject the 'list' template automatically for all List posts
LIST_POSTS = [f for f in os.listdir(LISTS_PATH) if not f.startswith('.')]
LIST_METADATA = {'posts/Lists/%s' % post: {'template': 'lists'} for post in LIST_POSTS}

# Basic Settings

AUTHOR = u'Ryan M'
USE_FOLDER_AS_CATEGORY = False
DEFAULT_CATEGORY = 'Tech'
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True
DIRECT_TEMPLATES = ['index', 'categories', 'archives', 'tags', 'feeds']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/.htaccess': {'path': '.htaccess'},
    }
EXTRA_PATH_METADATA.update(LIST_METADATA)
JINJA_ENVIRONMENT = dict(
    comment_start_string='###',
    comment_end_string='/###'
)

# Found at https://github.com/getpelican/pelican/wiki/Tips-n-Tricks
MARKDOWN = {
    'extensions': [
        CodeHiliteExtension([('linenums', False)]),
        'markdown.extensions.extra',
        'markdown.extensions.footnotes',
        'markdown.extensions.toc'
    ],
    'output_format': 'html5',
}

OUTPUT_PATH = os.path.join('/', 'tmp', 'ryanmoco')
PATH = '../../content'
PAGE_PATHS = ['pages']
OUTPUT_SOURCES = True
OUTPUT_SOURCES_EXTENSION = '.txt'
RELATIVE_URLS = True
PLUGIN_PATHS = ['../plugins']
PLUGINS = [
    'taglist',
    'photos',
    'summary',
    'tag_cloud',
    'drafts_page',
    'json_feed',
    'code_replacement'
]
SITENAME = u'ryanmo.co'
SITEURL = 'http://localhost:8000'
STATIC_PATHS = [
    'downloads',
    'extra',
    'images',
    'posts'
]
TIMEZONE = 'America/Los_Angeles'
WITH_FUTURE_DATES = False
CACHE_CONTENT = False
LOAD_CONTENT_CACHE = False

# URL SETTINGS

ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

# Feed Settings

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Pagination

DEFAULT_PAGINATION = 10

# Theme

TESTING = True
THEME = 'theme'
SOCIAL = (
    ('Twitter', 'http://twitter.com/rjames86'),
    ('Github', 'http://www.github.com/rjames86'),
    ('RSS', 'none'),
    ('Email', 'mailto:blog@ryanmo.co')
)
TWITTER_USERNAME = 'rjames86'
TAGLINE = "ryanmo.co"

# Ordering content

REVERSE_CATEGORY_ORDER = True

# Plugins

# JSON Feed
SITE_FAVICON = SITEURL + '/images/favicon.png'
JSON_SHORTEN_URL = True
JSON_CAMPAIGN_PARAM = "JSONFeed"
JSON_FEED = 'feed.json'
JSON_CATEGORY_FEED_RSS = 'feeds/%s.json'
JSON_TAG_FEED_RSS = 'feeds/%s.json'

# Photos plugin config
PHOTO_LIBRARY = CONTENT_PATH + '/gallery_photos'
PHOTO_RESIZE_JOBS = 5
PHOTO_EXIF_AUTOROTATE = True
PHOTO_EXIF_KEEP = True

PHOTO_GALLERY = (1024, 768, 80)
PHOTO_ARTICLE = (760, 506, 80)
PHOTO_THUMB = (384, 288, 60)
