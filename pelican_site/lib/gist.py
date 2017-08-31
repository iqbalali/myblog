# Idea based on https://github.com/cmacmackin/markdown-include/blob/master/markdown_include/include.py

import re
import os.path
from codecs import open
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

import logging

log = logging.getLogger(__name__)

INC_SYNTAX = re.compile(r'\{!\s*(.+?)\s*!\}')


class MarkdownInclude(Extension):
    def __init__(self, configs={}):
        self.config = {
            'base_path': ['.', 'Default location from which to evaluate '
                          'from the default path.'],
            'source_path': ['.', 'Default location from which to evaluate '
                            'relative paths from the file.'],
            'encoding': ['utf-8', 'Encoding of the files used by the include '
                         'statement.']
        }
        for key, value in configs.items():
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add(
            'include', IncludePreprocessor(md, self.getConfigs()), '_begin'
        )


class IncludePreprocessor(Preprocessor):
    def __init__(self, md, config):
        super(IncludePreprocessor, self).__init__(md)
        self.base_path = config['base_path']
        self.source_path = config['source_path']
        self.encoding = config['encoding']

    def run(self, lines):
        for line in lines:
            loc = lines.index(line)
            m = INC_SYNTAX.search(line)

            if m:
                filename = m.group(1)
                if filename.startswith('/'):
                    dir_to_file = self.base_path
                    filename = filename[1:]
                else:
                    dir_to_file = self.source_path

                filename = os.path.expanduser(filename)
                if not os.path.isabs(filename):
                    filename = os.path.abspath(
                        os.path.join(dir_to_file, filename)
                    )
                try:
                    with open(filename, 'r', encoding=self.encoding) as r:
                        text = r.readlines()
                except Exception as e:
                    log.warning('Could not find file {}. Error: {}'.format(filename, e))
                    # lines[loc] = INC_SYNTAX.sub('', line) # to remove
                    continue

                # indent text
                text = ["\t%s" % line.rstrip('\n') for line in text]
                lines = lines[:loc] + text + lines[loc + 1:]
        return lines


def makeExtension(*args, **kwargs):
    return MarkdownInclude(kwargs)
