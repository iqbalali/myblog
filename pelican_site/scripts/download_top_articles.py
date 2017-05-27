import datetime
import os
import requests
import json
import operator
import sys


def remove_index(entry):
    if entry['label'] and entry['label'].endswith('/index'):
        entry[u'short_url'] = entry['label'].replace('/index', '')
    else:
        entry[u'short_url'] = entry['label']
    return entry


def get_article_info(article):
    return {
        'title': article.get('title'),
        'url': article.get('full_url'),
        'slug': article.get('slug'),
    }

# TODO for later
# def deduplicate_entries(sorting_key, url_intersection, data):
#     for article in data:
#         check_dups = filter(lambda x: sorting_key(x) in url_intersection, data)
#     return max(check_dups, key=lambda c: c['nb_hits'])


def main(args):
    if len(args) > 1 and args[-1] == 'testing':
        blog_path = os.path.join(
            os.path.join(os.path.dirname(__file__), os.pardir),
            'content',
        )
    else:
        blog_path = '/var/www/ryanssite'
    today = datetime.datetime.today()
    first_of_month = today.replace(day=1)

    if today.day < 5:
        period = first_of_month.replace(month=(first_of_month.month - 1) or 12)
    else:
        period = first_of_month

    piwik_url = 'https://ryanmo.co/pa/index.php'
    json_path = os.path.join(blog_path, 'json')

    with open(os.path.join(json_path, 'all_articles.json')) as f:
        all_articles = json.loads(f.read()).get('articles')

    payload = {
        'module': 'API',
        'method': 'Actions.getPageUrls',
        'format': 'JSON',
        'idSite': '1',
        'period': 'month',
        'date': period.strftime('%Y-%m-%d'),
        'flat': '1',
        'segment': 'pageUrl!@.html',
        'token_auth': '461c89e005b33b58266ba073c26b6714',
        'filter_limit': '100',
    }

    req = requests.get(piwik_url, params=payload)

    data = json.loads(req.text)

    data = [entry for entry in data if entry['url'] != 'http://ryanmo.co/']

    data = map(remove_index, data)

    all_articles_urls = [article['short_url'] for article in all_articles]
    all_data_urls = [article['short_url'] for article in data]

    url_intersection = list(set(all_data_urls) & set(all_articles_urls))

    common_articles = [article for article in all_articles
                       if article['short_url'] in url_intersection]

    sorting_key = operator.itemgetter("short_url")

    # get rid of items in data that aren't in the url_intersection
    def short_url_in_data(data_item):
        return any(url in data_item['short_url'] for url in url_intersection)

    data[:] = [data_item for data_item in data if short_url_in_data(data_item)]

    for i, j in zip(
            sorted(common_articles, key=sorting_key),
            sorted(data, key=sorting_key)):
        j.update(i)

    sort_by_hits = sorted(data, key=lambda entry: entry['nb_hits'], reverse=True)
    top_five_articles = sort_by_hits[:5]

    to_ret = dict(
        period=period.strftime('%Y-%m-%d'),
        articles=map(get_article_info, top_five_articles)
        )

    with open(os.path.join(json_path, 'top_articles.json'), 'w') as w:
        json.dump(to_ret, w)

if __name__ == '__main__':
    main(sys.argv)
