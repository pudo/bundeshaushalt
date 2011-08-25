#coding: utf-8
import sys
from webstore.client import URL as WebStore
from datautil.normalization.table_based import Normalizer
from pprint import pprint

from scrape import UNIQUE_COLUMNS

FPL_DOC = "tljXl8WXu4oyTRCJ7YIaQDg"
GPL_DOC = "tNbpClFqMRHmPwVwHajj4DA"

GOOGLE_USER = None
GOOGLE_PASS = None

EP_COLORS = {
    "01": "#CA221D",
    "02": "#CA221D",
    "03": "#CA221D",
    "04": "#CA221D",
    "05": "#C22769",
    "06": "#3F93E1",
    "07": "#481B79",
    "08": "#6AAC32",
    "09": "#42928F",
    "10": "#D32645",
    "11": "#CD531C",
    "12": "#EDC92D",
    "14": "#A5B425",
    "15": "#211D79",
    "16": "#449256",
    "17": "#7A2077",
    "19": "#CA221D",
    "20": "#CA221D",
    "23": "#E29826",
    "30": "#44913D",
    "32": "#2458A3",
    "33": "#2458A3",
    "60": "#14388C"
}

def get_normalizer(doc_id, sheet_name, _cache={}):
    global GOOGLE_PASS, GOOGLE_USER
    if GOOGLE_USER is None or GOOGLE_PASS is None:
        GOOGLE_USER = raw_input("Google Username: ")
        GOOGLE_PASS = raw_input("Google Password: ")
    if not (doc_id, sheet_name) in _cache:
        _cache[(doc_id, sheet_name)] = Normalizer(GOOGLE_USER,
            GOOGLE_PASS, doc_id, sheet_name, "id")
    return _cache[(doc_id, sheet_name)]

def for_id(row_id):
    row = {'id': row_id}
    def _classify(normalizer, name, id):
        row[name + "_id"] = id
        values = normalizer.lookup(id)
        if not values:
            return
        label = values.get('name')
        if label:
            row[name + "_label"] = label.encode('utf-8').strip()
        else:
            row[name + "_label"] = ""
        row[name + "_color"] = values.get('color', '')
        description = values.get('description')
        if description:
            row[name + "_desc"] = description.encode('utf-8').strip()
        else: 
            row[name + "_desc"] = ""
    gpl = get_normalizer(GPL_DOC, 'Gruppierungsplan')
    fpl = get_normalizer(FPL_DOC, 'Funktionenplan')
    _classify(gpl, 'hauptgruppe', row_id[4:5] + "00")
    _classify(gpl, 'obergruppe', row_id[4:5] + "0")
    _classify(gpl, 'gruppe', row_id[4:7])
    _classify(fpl, 'hauptfunktion', row_id[10:11] + "00")
    _classify(fpl, 'oberfunktion', row_id[10:12] + "0")
    _classify(fpl, 'funktion', row_id[10:13])
    row['ep_color'] = EP_COLORS[row_id[:2]]
    pprint(row)
    return row

def process_file(table):
    for _id in table.distinct('id'):
        id = _id.get('id')
        table.writerow(for_id(id), 
                 unique_columns=['id'])

if __name__ == '__main__':
    assert len(sys.argv)==2, "Need argument: webstore-url!"
    db, table = WebStore(sys.argv[1], "raw")
    process_file(table)
