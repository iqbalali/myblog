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
                          'relative paths for the include statement.'],
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
    '''
    This provides an "include" function for Markdown, similar to that found in
    LaTeX (also the C pre-processor and Fortran). The syntax is {!filename!},
    which will be replaced by the contents of filename. Any such statements in
    filename will also be replaced. This replacement is done prior to any other
    Markdown processing. All file-names are evaluated relative to the location
    from which Markdown is being called.
    '''
    def __init__(self, md, config):
        super(IncludePreprocessor, self).__init__(md)
        self.base_path = config['base_path']
        self.encoding = config['encoding']

    def run(self, lines):
        for line in lines:
            loc = lines.index(line)
            m = INC_SYNTAX.search(line)

            if m:
                filename = m.group(1)
                filename = os.path.expanduser(filename)
                if not os.path.isabs(filename):
                    filename = os.path.normpath(
                        os.path.join(self.base_path, filename)
                    )
                try:
                    with open(filename, 'r', encoding=self.encoding) as r:
                        text = r.readlines()
                except Exception as e:
                    log.warning('Could not find file {}. Error: {}'.format(filename, e))
                    lines[loc] = INC_SYNTAX.sub('', line)
                    continue
                # poor man's 'strip the newlines off the end'
                for i in range(len(text)):
                    text[i] = text[i][0:-1]
                text = ["\t%s" % line for line in text]
                lines = lines[:loc] + text + lines[loc + 1:]
        return lines


def makeExtension(*args, **kwargs):
    return MarkdownInclude(kwargs)
