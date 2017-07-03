import os
from pelican import signals
from pelican.readers import Markdown, MarkdownReader
from pelican.utils import pelican_open

from lib.gist import MarkdownInclude


class CustomMarkdownReader(MarkdownReader):

    def read(self, source_path):
        """Parse content and metadata of markdown files.

        Rendering them as jinja templates first.

        """

        self._source_path = source_path
        default_extensions = self.settings['MARKDOWN']['extensions']
        default_extensions.append(
            MarkdownInclude(configs={
                'base_path': self.settings['CONTENT_PATH'],
                'source_path': os.path.dirname(source_path)
            })
        )
        self._md = Markdown(extensions=default_extensions)

        with pelican_open(source_path) as text:
            content = self._md.convert(text)

        if hasattr(self._md, 'Meta'):
            metadata = self._parse_metadata(self._md.Meta)
        else:
            metadata = {}

        return content, metadata


def add_reader(readers):
    for ext in MarkdownReader.file_extensions:
        readers.reader_classes[ext] = CustomMarkdownReader


def register():
    signals.readers_init.connect(add_reader)
