# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import logging

from cssmin import cssmin
from scss.compiler import compile_file

from pelican import signals
logger = logging.getLogger(__name__)


def compile_critical(pelican):
    """Add Webassets to Jinja2 extensions in Pelican settings."""
    theme_path = os.path.join(pelican.settings.get('PATH'),
                              os.pardir,
                              'pelican_site',
                              'theme')
    critical_css_path = os.path.join(theme_path,
                                     'static',
                                     'scss',
                                     'critical.scss')
    compiled_css = compile_file(critical_css_path)
    minified_css = cssmin(compiled_css)
    with open(os.path.join(theme_path, 'templates', 'critical.css'), 'w') as f:
        f.write(minified_css)


def register():
    """Plugin registration."""
    signals.initialized.connect(compile_critical)
