import json
import os

from pelican import signals
from pelican.utils import (get_relative_path,
                           path_to_url, set_date_tzinfo)

from jinja2 import Markup


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'as_json'):
            return obj.as_json()
        else:
            return json.JSONEncoder.default(self, obj)


class Base(object):
    def as_json(self):
        return self.__dict__


class Author(Base):
    def __init__(self, name, url=None, avatar=None):
        self.name = name
        self.url = url
        self.avatar = avatar

    @classmethod
    def from_pelican_author(cls, json_feed_generator, author):
        author_url = json_feed_generator.settings.get('AUTHOR_URL').format(slug=author.slug)
        return cls(
            author.name,
            json_feed_generator.build_url(author_url),
            None
        )


class Item(Base):
    def __init__(self,
                 item_id,
                 content_html,
                 url=None,
                 external_url=None,
                 title=None,
                 content_text=None,
                 summary=None,
                 image=None,
                 banner_image=None,
                 date_published=None,
                 date_modified=None,
                 author=None,
                 tags=None):
        self.id = item_id
        self.url = url
        self.external_url = external_url
        self.title = title
        self.content_html = content_html
        self.content_text = content_text
        self.summary = summary
        self.image = image
        self.banner_image = banner_image
        self.date_published = date_published
        self.date_modified = date_modified
        self.author = author
        self.tags = tags

    def __repr__(self):
        return '<Item id=%s>' % (self.id)

    @classmethod
    def from_article(cls, json_feed_generator, article):
        title = Markup(article.title).striptags()
        summary = article._summary if hasattr(article, '_summary') else None
        item_url = json_feed_generator.build_url(article.url)
        return cls(
            item_id=item_url,
            url=item_url,
            title=title,
            content_html=article.content,
            summary=summary,
            date_published=set_date_tzinfo(
                article.date, json_feed_generator.settings.get('TIMEZONE', None)).isoformat(),
            date_modified=set_date_tzinfo(
                article.modified, json_feed_generator.settings.get('TIMEZONE', None)
                ).isoformat() if hasattr(article, 'modified') else None,
            author=Author.from_pelican_author(json_feed_generator, getattr(article, 'author', '')),
            tags=[tag.name for tag in article.tags] if hasattr(article, 'tags') else None
        )


class Items(list):
    @classmethod
    def from_generator(cls, json_feed_generator):
        self = cls()
        for article in json_feed_generator.articles:
            self.append(Item.from_article(json_feed_generator, article))
        return self

    def as_json(self):
        return self


class JsonFeed(Base):
    def __init__(self,
                 author,
                 description,
                 favicon,
                 feed_url,
                 home_page_url,
                 title,
                 user_comment,
                 version,
                 items):
        self.author = author
        self.description = description
        self.favicon = favicon
        self.feed_url = feed_url
        self.home_page_url = home_page_url
        self.items = items
        self.title = title
        self.user_comment = user_comment
        self.version = version

    @classmethod
    def from_generator(cls, json_feed_generator):
        return cls(
            author=Author(json_feed_generator.settings.get('AUTHOR')),
            description=None,
            feed_url=json_feed_generator.feed_url,
            home_page_url=json_feed_generator.site_url,
            title=json_feed_generator.settings.get('SITENAME'),
            user_comment=None,
            version='https://jsonfeed.org/version/1',
            items=Items.from_generator(json_feed_generator),
            favicon=json_feed_generator.settings.get('SITE_FAVICON', None)
        )


class JsonFeedGenerator(object):
    def __init__(self, article_generator):
        self.articles = article_generator.articles
        self.settings = article_generator.settings
        self.context = article_generator.context
        self.generator = article_generator

        self.path = 'feed.json'

        self.site_url = article_generator.context.get('SITEURL',
                                                      path_to_url(get_relative_path(self.path)))

        self.feed_domain = self.context.get('FEED_DOMAIN')
        self.feed_url = '{}/{}'.format(self.feed_domain, self.path)

    def build_url(self, path):
        return "%s/%s" % (self.site_url, path)

    def write_feed(self):
        complete_path = os.path.join(self.generator.output_path, self.path)
        try:
            os.makedirs(os.path.dirname(complete_path))
        except Exception:
            pass

        with open(complete_path, 'w') as f:
            json.dump(JsonFeed.from_generator(self), f, cls=JSONEncoder)


def get_generators(article_generator, writer):
    json_feed_generator = JsonFeedGenerator(article_generator)
    json_feed_generator.write_feed()


def register():
    signals.article_writer_finalized.connect(get_generators)
