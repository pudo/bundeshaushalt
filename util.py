import os
import logging
import dataset

req_log = logging.getLogger('requests')
req_log.setLevel(level=logging.WARN)

_here = os.path.dirname(__file__)
_sqlfile = os.path.join(_here, 'haushalt.sqlite3')

engine = dataset.connect(os.environ.get('DATABASE_URI', 'sqlite:///' + _sqlfile))
table = engine['haushalt']

DIMENSIONS = ['einzelplan', 'gruppe', 'funktion']


def data_dir():
    path = os.path.join(_here, '../dev/data')
    return os.path.realpath(path)
