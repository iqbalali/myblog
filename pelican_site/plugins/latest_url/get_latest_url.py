import os
import json
from pelican import signals

"""
Creates a folder in your Pelican content folder called "json"
and createa  file called "latest_url.json" that looks like

    {
        'url': full url of post
        'title': Title of post
    }


"""

from lib.constants import creds
from yourls import YOURLSClient, YOURLSURLExistsError


class Yourls(object):
    def __init__(self, site_url):
        self.site_url = site_url
        self._client = None

    @property
    def client(self):
        if not self._client:
            self._client = YOURLSClient(self.api_url, signature=creds['YOURLS_TOKEN'])
        return self._client

    @property
    def api_url(self):
        return "%s/s/yourls-api.php" % self.site_url

    def shorten_url(self, url):
        try:
            to_shorten = self.client.shorten(url)
        except YOURLSURLExistsError as exc:
            to_shorten = exc.url
        return to_shorten.shorturl


class GetLatestPost(object):

    def __init__(self, generators, *args, **kwargs):
        self.articles = generators.articles
        self.settings = generators.settings

        self.contentpath = self.settings.get('PATH')
        self.siteurl = self.settings.get('SITEURL')
        self.output_path = os.path.join(self.contentpath, 'json')
        self.to_json = {}

    @property
    def latest_post(self):
        return self.articles[0]

    @property
    def latest_url(self):
        return self.latest_post.url

    def write_json_to_file(self):
        self._ensure_path()
        with open(self.output_path + '/latest_url.json', 'w') as f:
            json.dump(self.to_json, f, indent=4)

    def _ensure_path(self):
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

    def generate_output(self):
        self.to_json = dict(
            url="%s/%s/" % (self.siteurl, self.latest_url),
            title=self.latest_post.metadata.get('title'),
            shortened_url=Yourls(self.siteurl).shorten_url("%s/%s/" % (self.siteurl, self.latest_url))
        )
        self.write_json_to_file()


def get_generators(generators):
    output = GetLatestPost(generators)
    output.generate_output()


def register():
    signals.article_generator_finalized.connect(get_generators)
