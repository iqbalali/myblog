from pelican import signals

from bs4 import BeautifulSoup

import logging
logger = logging.getLogger(__name__)


def add_footnote_class(li):
    li['class'] = 'footnote'
    return li


def content_object_init(instance):

    if instance._content is not None:
        content = instance._content
        soup = BeautifulSoup(content, "html.parser")
        footnote_content = soup.find('div', attrs={'class': 'footnote'})

        if footnote_content:
            footnote_content['class'] = 'footnotes'
            map(add_footnote_class, footnote_content.findAll('li'))
        instance._content = soup.decode()


def register():
    signals.content_object_init.connect(content_object_init)
