"""
Related posts plugin for Pelican
================================

Adds related_posts variable to article's context
"""

import json
import os

from pelican import signals
from collections import Counter


class RelatedPosts(object):
    def __init__(self, generator):
        self.generator = generator
        self.settings = generator.settings
        self.related_posts = {}

        self.contentpath = self.settings.get('PATH')
        self.siteurl = self.settings.get('SITEURL')
        self.output_path = os.path.join(self.contentpath, 'json')
        self.file_name = '/related_articles.json'

    def write_json_to_file(self):
        self._ensure_path()
        with open(self.output_path + self.file_name, 'w') as f:
            json.dump(dict(data=self.related_posts), f, indent=4)

    def _ensure_path(self):
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

    def add_related_posts(self):
        # get the max number of entries from settings
        # or fall back to default (5)
        numentries = self.generator.settings.get('RELATED_POSTS_MAX', 5)
        for article in self.generator.articles:
            # set priority in case of forced related posts
            if hasattr(article, 'related_posts'):
                # split slugs
                related_posts = article.related_posts.split(',')
                posts = []
                # get related articles
                for slug in related_posts:
                    i = 0
                    for a in self.generator.articles:
                        if i >= numentries:  # break in case there are max related psots
                            break
                        if a.slug == slug:
                            posts.append(a)
                            i += 1

                article.related_posts = posts
                self.related_posts[article.slug] = map(self._create_article_dict, posts)
            else:
                # no tag, no relation
                if not hasattr(article, 'tags'):
                    continue

                # score = number of common tags
                scores = Counter()
                for tag in article.tags:
                    scores += Counter(self.generator.tags[tag])

                # remove itself
                scores.pop(article)

                article.related_posts = [other for other, count
                                         in scores.most_common(numentries)]

                self.related_posts[article.slug] = map(self._create_article_dict,
                                                       [other for other, count
                                                        in scores.most_common(numentries)])
        self.write_json_to_file()

    def _create_article_dict(self, article):
        return {
            'title': article.title,
            'url': '{}/{}'.format(self.siteurl, article.url),
            'slug': article.slug,
        }


def get_generator(generator):
    related_posts = RelatedPosts(generator)
    related_posts.add_related_posts()


def register():
    signals.article_generator_finalized.connect(get_generator)
