#coding: utf-8
import sys
import csv
import sqlaload as sl
from pprint import pprint

from scrape import UNIQUE_COLUMNS

FPL_DOC = "tljXl8WXu4oyTRCJ7YIaQDg"
GPL_DOC = "tNbpClFqMRHmPwVwHajj4DA"

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

def load_csv_keys(file_name, key):
    with open(file_name, 'r') as fh:
        reader = csv.DictReader(fh)
        data = list(reader)
        r = [(d.get(key), d) for d in data]
        return dict(r)

def for_row(row, fpl, gpl):
    row_id = row.get('titel_id')
    def _classify(normalizer, name, id):
        row[name + "_id"] = id
        values = normalizer.get(id)
        if not values:
            return
        label = values.get('Name')
        if label:
            row[name + "_label"] = label.decode('utf-8').strip()
        else:
            row[name + "_label"] = ""
        row[name + "_color"] = values.get('Color', '')
        description = values.get('Description')
        if description:
            row[name + "_description"] = description.decode('utf-8').strip()
        else: 
            row[name + "_description"] = ""
    _classify(gpl, 'hauptgruppe', row_id[4:5] + "00")
    _classify(gpl, 'obergruppe', row_id[4:5] + "0")
    _classify(gpl, 'gruppe', row_id[4:7])
    _classify(fpl, 'hauptfunktion', row_id[10:11] + "00")
    _classify(fpl, 'oberfunktion', row_id[10:12] + "0")
    _classify(fpl, 'funktion', row_id[10:13])
    row['ep_color'] = EP_COLORS[row_id[:2]]
    #pprint(row)
    return row

def process(engine, table):
    gpl = load_csv_keys('gruppierungsplan.csv', 'ID')
    fpl = load_csv_keys('funktionenplan.csv', 'ID')
    for row in sl.all(engine, table):
        sl.upsert(engine, table, for_row(row, fpl, gpl), ['id'])

if __name__ == '__main__':
    assert len(sys.argv)==2, "Need argument: engine-url!"
    engine = sl.connect(sys.argv[1])
    table = sl.get_table(engine, 'bund')
    process(engine, table)
