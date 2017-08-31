from markdown import Markdown
from pelican.utils import pelican_open
import os
from pelican.utils import get_date

MARKDOWN = {
    'extensions': [
        'markdown.extensions.extra',
        'markdown.extensions.footnotes',
        'markdown.extensions.toc',
        'markdown.extensions.meta'
    ],
    'output_format': 'html5',
}

for dirpath, _, filenames in os.walk('/Users/rjames/Dropbox/blogs/ryanmoco/content/posts/Tech'):
    for f in filenames:
        if f.startswith('.'):
            continue
        filename, ext = os.path.splitext(f)
        if ext != '.md':
            continue

        md = Markdown(**MARKDOWN)
        with pelican_open(os.path.join(dirpath, f)) as text:
            content = md.convert(text)
            if hasattr(md, 'Meta'):
                date =  get_date(md.Meta['date'][0]).strftime('%Y-%m-%d')

                # if not os.path.exists(os.path.join(dirpath, date)):
                #     os.mkdir(os.path.join(dirpath, date))
                os.rename(
                    os.path.join(dirpath, f),
                    os.path.join(dirpath, date, f)
                )
