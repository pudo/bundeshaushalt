import os
import json
import dataset
from util import engine, table, data_dir
from util import DIMENSIONS
from pprint import pprint

LEVELS = {
    'einzelplan': range(1, 3),
    'funktion': range(1, 4),
    'gruppe': range(1, 4)
}

Q = """SELECT %(dim)s_%(level)s_address AS address, %(dim)s_%(level)s_title AS title,
              flow, year, SUM(value) AS value
              FROM %(table)s
              WHERE %(filter)s
              GROUP BY %(dim)s_%(level)s_address, %(dim)s_%(level)s_title, flow, year
              ORDER BY %(dim)s_%(level)s_address DESC; """


def save_json(dimension, address, obj):
    prefix = data_dir()
    path = os.path.join(prefix, dimension, address + '.json')
    if not os.path.isdir(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, 'wb') as fh:
        json.dump(obj, fh)


def collect(dimension, entries):
    collected = []
    for entry in entries:
        prev = collected[-1] if len(collected) else None
        if prev is None or prev['address'] != entry['address']:
            collected.append({
                'dimension': dimension,
                'address': entry['address'],
                'title': entry['title'],
                'values': {'einnahmen': {}, 'ausgaben': {}}
            })
        collected[-1]['values'][entry['flow']][entry['year']] = entry['value']
    return collected


def generate_children(dimension, level, address):
    children = []
    if level == LEVELS[dimension][-1]:
        q = """SELECT address, title, flow, year, value
                FROM %(table)s
                WHERE %(dim)s_%(level)s_address = '%(address)s'"""
        q = q % {
            'table': table.table.name,
            'dim': dimension,
            'level': level,
            'address': address
        }
        for entry in collect('titel', engine.query(q)):
            children.append(entry)
    else:
        if address is not None:
            filter_ = '%s_%s_address = "%s"' % (dimension, level, address)
        else:
            filter_ = '1=1'
        qp = {'dim': dimension,
              'level': level+1,
              'table': table.table.name,
              'filter': filter_}
        for entry in collect(dimension, engine.query(Q % qp)):
            children.append(entry)
    return children


def generate_drilldowns():
    for dimension in DIMENSIONS:
        index = {
            'dimension': dimension,
            'children': generate_children(dimension, 0, None)
        }
        save_json(dimension, 'index', index)
        for level in LEVELS[dimension]:
            qp = {'dim': dimension,
                  'level': level,
                  'table': table.table.name,
                  'filter': '1=1'}
            for entry in collect(dimension, engine.query(Q % qp)):
                entry['children'] = generate_children(dimension, level, entry['address'])
                #pprint(entry)
                save_json(dimension, entry['address'], entry)


def generate_title_data():
    prefix = data_dir()
    file_name = 'titles/{{einzelplan_1_address}}/{{einzelplan_2_address}}/{{address}}.json'
    dataset.freeze(table.all(), format='json', filename=file_name, prefix=prefix)


if __name__ == '__main__':
    #generate_drilldowns()
    generate_title_data()
