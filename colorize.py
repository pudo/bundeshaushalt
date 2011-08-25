#coding: utf-8
import sys
from csv import DictReader, DictWriter, field_size_limit
from pprint import pprint
from collections import defaultdict

# color range generator:    
def hex_to_tuple(val, alpha=False):
    if isinstance(val,basestring):
        val = val[1:]
        if len(val) == 8:
            alpha = True
        val = int(val,16)
    if alpha:
        t = ((val>>24)&0xFF,((val>>16)&0xFF),((val>>8)&0xFF),(val&0xFF))
    else:
        t = (((val>>16)&0xFF),((val>>8)&0xFF),(val&0xFF))
    return [int(n) for n in t[:3]]
    
def tuple_to_hex(tup):
    return "#" + "%02x%02x%02x" % (int(tup[0]), int(tup[1]), int(tup[2]))

def _color_range(color, slices, var=70.0):
    slice_value = lambda n: ((var*2)/slices)*n
    color_part = lambda c, n: max(0, min(255, (c-var)+slice_value(n)))
    cv = hex_to_tuple(color)
    for n in range(slices):
        yield tuple_to_hex((color_part(cv[0], n), 
                            color_part(cv[1], n), 
                            color_part(cv[2], n)))

def process_file(infile, outfile, key_column, color_column, subkey_column, subcolor_column):
    field_size_limit(100000000)
    infile = open(infile, 'rb')
    children = defaultdict(set)
    key_colors = {}
    incsv = DictReader(infile)
    for row in incsv:
        key = row.get(key_column)
        key_colors[key] = row.get(color_column)
        children[key].add(row.get(subkey_column))
    pprint(children)
    pprint(key_colors)
    sub_colors = dict()
    for key in children.keys():
        gen = _color_range(key_colors.get(key), len(children[key]))
        for sub, col in zip(children[key], gen):
            sub_colors[(key, sub)] = col
    pprint(sub_colors)
    infile.seek(0)
    outfile = open(outfile, 'wb')
    incsv = DictReader(infile)
    headers = list(incsv.fieldnames) + [subcolor_column]
    outcsv = DictWriter(outfile, headers)
    outcsv.writerow(dict(zip(headers, headers)))
    for row in incsv:
         ks = (row.get(key_column), row.get(subkey_column))
         row[subcolor_column] = sub_colors[ks]
         #pprint(row)
         outcsv.writerow(row)
    outfile.close()
    infile.close()

if __name__ == '__main__':
    fn = sys.argv[1]
    process_file(fn, fn + "c1", "ep_id", "ep_color", "kp_id", "kp_color")
    process_file(fn + "c1", fn + "c2", "ep_id", "ep_color", "tgr_id", "tgr_color")
    process_file(fn + "c2", fn + "c3", "ep_id", "ep_color", "id", "color")
    process_file(fn + "c3", fn + "c4", "hauptfunktion_id", "hauptfunktion_color", 
            "oberfunktion_id", "oberfunktion_color")
    process_file(fn + "c4", fn + "c5", "oberfunktion_id", "oberfunktion_color", 
            "funktion_id", "funktion_color")
    process_file(fn + "c5", fn + "c6", "hauptgruppe_id", "hauptgruppe_color", 
            "obergruppe_id", "obergruppe_color")
    process_file(fn + "c6", fn + "colorized", "obergruppe_id", "obergruppe_color", 
            "gruppe_id", "gruppe_color")

