#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Wonseok Choi'
SITENAME = u'Svperbeast Blog'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Seoul'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social widget
SOCIAL = (
    ('github', 'http://github.com/svperbeast'),
    )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# need to clone pelican-themes into 'themes/'
THEME = 'themes/pelican-themes/bootstrap2'

# need to clone pelican-plugins into 'plugins/'
PLUGIN_PATHS = ['plugins/pelican-plugins']
PLUGINS = ['autopages', 'tag_cloud']

DISQUS_SITENAME = 'svperbeast-blog'

GOOGLE_ANALYTICS_ID = ''
GOOGLE_ANALYTICS_SITENAME = ''
