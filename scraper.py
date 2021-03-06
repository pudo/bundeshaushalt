import os
import re
import dataset
# from pprint import pprint
from collections import defaultdict
import requests

db = os.environ.get('DATABASE_URI', 'sqlite:///data.sqlite')
engine = dataset.connect(db)
table = engine['de_bundeshaushalt']

CLEAN = re.compile('(</?strong>)')
DIMENSIONS = ['einzelplan', 'gruppe', 'funktion']
URL = 'http://www.bundeshaushalt-info.de/rest/%s/soll/%s/%s/%s'


def clean_text(text):
    if text is None:
        return
    return CLEAN.sub('', text).strip()


def tree_scrape(titles, ctx, year, flow, section, address=''):
    url = URL % (year, flow, section, address)
    res = requests.get(url)
    try:
        data = res.json()
    except ValueError:
        print "URL", url
        return
    level = int(data.get('meta').get('levelCur')) + 1

    # pprint(data.get('meta'))

    for child in data.get('childs'):
        if level == 1:
            print [child.get('l')]
        if data.get('meta').get('levelCur') == \
                data.get('meta').get('levelMax'):
            titles[child.get('a')]['value'] = int(child.get('v'))
            titles[child.get('a')]['flexible'] = child.get('f')
            titles[child.get('a')]['title'] = clean_text(child.get('l'))
            titles[child.get('a')]['name'] = clean_text(child.get('t'))
            titles[child.get('a')]['address'] = child.get('a')
            titles[child.get('a')].update(ctx.copy())
        else:
            ctx['%s_%s_address' % (section, level)] = child.get('a')
            ctx['%s_%s_title' % (section, level)] = child.get('l')
            tree_scrape(titles, ctx.copy(), year, flow, section,
                        child.get('a'))


def bundeshaushalt_scrape():
    for year in [2012, 2013, 2014, 2015]:
        titles = defaultdict(dict)
        for flow in ['ausgaben', 'einnahmen']:
            for section in DIMENSIONS:
                ctx = {'year': year, 'flow': flow, 'account': section}
                tree_scrape(titles, ctx, year, flow, section, '')
        # pprint(dict(titles))
        for row in titles.values():
            table.upsert(row, ['year', 'flow', 'address'])


if __name__ == '__main__':
    bundeshaushalt_scrape()
