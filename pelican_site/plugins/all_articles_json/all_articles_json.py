import os
import json
from pelican import signals

"""
Createa  file called "all_articles.json" that looks like

    {
        full_url : "",
        short_url : "",
        title : "",
        slug : "",
    }


"""


class ArticlesJson(object):

    def __init__(self, generators, *args, **kwargs):
        self.articles = generators.articles
        self.settings = generators.settings

        self.contentpath = self.settings.get('PATH')
        self.siteurl = self.settings.get('SITEURL')
        self.output_path = os.path.join(self.contentpath, 'json')
        self.to_json = {'articles': []}
        self.file_name = '/all_articles.json'

    def write_json_to_file(self):
        self._ensure_path()
        with open(self.output_path + self.file_name, 'w') as f:
            json.dump(self.to_json, f, indent=4)

    def _ensure_path(self):
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

    def generate_output(self):
        for article in self.articles:
            self.to_json['articles'].append(
                dict(
                    full_url="%s/%s/" % (self.siteurl, article.url),
                    short_url="%s" % (article.url),
                    title=article.metadata.get('title'),
                    slug=article.slug,
                )
            )
        self.write_json_to_file()


def get_generators(generators):
    output = ArticlesJson(generators)
    output.generate_output()


def register():
    signals.article_generator_finalized.connect(get_generators)
