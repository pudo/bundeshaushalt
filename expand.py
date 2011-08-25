#coding: utf-8
import sys
from csv import DictReader, DictWriter, field_size_limit
from datautil.normalization.table_based import Normalizer
from pprint import pprint

FPL_DOC = "tljXl8WXu4oyTRCJ7YIaQDg"
GPL_DOC = "tNbpClFqMRHmPwVwHajj4DA"

EXTRA_FIELDS = ['ep_color',
    'hauptgruppe_id', 'hauptgruppe_label', 'hauptgruppe_color', 'hauptgruppe_desc',
    'obergruppe_id', 'obergruppe_label', 'obergruppe_color', 'obergruppe_desc',
    'gruppe_id', 'gruppe_label', 'gruppe_color', 'gruppe_desc',
    'hauptfunktion_id', 'hauptfunktion_label', 'hauptfunktion_color', 'hauptfunktion_desc',
    'oberfunktion_id', 'oberfunktion_label', 'oberfunktion_color', 'oberfunktion_desc',
    'funktion_id', 'funktion_label', 'funktion_color', 'funktion_desc',
    ]

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

def for_row(row):
    def _classify(normalizer, name, id):
        row[name + "_id"] = id
        values = normalizer.lookup(id)
        if not values:
            return
        label = values.get('name')
        if label:
            row[name + "_label"] = label.encode('utf-8')
        else:
            row[name + "_label"] = ""
        row[name + "_color"] = values.get('color', '')
        description = values.get('description')
        if description:
            row[name + "_desc"] = description.encode('utf-8')
        else: 
            row[name + "_desc"] = ""
    gpl = get_normalizer(GPL_DOC, 'Gruppierungsplan')
    fpl = get_normalizer(FPL_DOC, 'Funktionenplan')
    id = row['id']
    _classify(gpl, 'hauptgruppe', id[4:5] + "00")
    _classify(gpl, 'obergruppe', id[4:5] + "0")
    _classify(gpl, 'gruppe', id[4:7])
    _classify(fpl, 'hauptfunktion', id[10:11] + "00")
    _classify(fpl, 'oberfunktion', id[10:12] + "0")
    _classify(fpl, 'funktion', id[10:13])
    row['ep_color'] = EP_COLORS[row['ep_id']]
    #pprint(row)
    return row

def process_file(infile, outfile):
    field_size_limit(100000000)
    infile = open(infile, 'rb')
    outfile = open(outfile, 'wb')
    incsv = DictReader(infile)
    headers = list(incsv.fieldnames) + EXTRA_FIELDS
    outcsv = DictWriter(outfile, headers)
    outcsv.writerow(dict(zip(headers, headers)))
    print headers
    for row in incsv:
         outcsv.writerow(for_row(row))
    outfile.close()
    infile.close()

if __name__ == '__main__':
    assert len(sys.argv)==3, "Need 2 arguments: infile, outfile!"
    process_file(sys.argv[1], sys.argv[2])
