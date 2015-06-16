#coding: utf-8
import sys
from pprint import pprint
from collections import defaultdict

import sqlaload as sl

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
    if color is None:
        color = '#cccccc'
    slice_value = lambda n: ((var*2)/slices)*n
    color_part = lambda c, n: max(0, min(255, (c-var)+slice_value(n)))
    cv = hex_to_tuple(color)
    for n in range(slices):
        yield tuple_to_hex((color_part(cv[0], n), 
                            color_part(cv[1], n), 
                            color_part(cv[2], n)))

def process(engine, table, key_column, color_column, subkey_column, subcolor_column):
    children = defaultdict(set)
    key_colors = {}
    for row in sl.all(engine, table):
        key = row.get(key_column)
        key_colors[key] = row.get(color_column)
        children[key].add(row.get(subkey_column))
    sub_colors = dict()
    for key in children.keys():
        gen = _color_range(key_colors.get(key), len(children[key]))
        for sub, col in zip(children[key], gen):
            sub_colors[(key, sub)] = col
    for row in sl.all(engine, table):
         ks = (row.get(key_column), row.get(subkey_column))
         row[subcolor_column] = sub_colors[ks]
         #pprint(row)
         sl.upsert(engine, table, row, ['id'])

if __name__ == '__main__':
    assert len(sys.argv)==2, "Need argument: engine-url!"
    engine = sl.connect(sys.argv[1])
    table = sl.get_table(engine, 'bund')

    process(engine, table, "ep_id", "ep_color", "kp_id", "kp_color")
    process(engine, table, "ep_id", "ep_color", "tgr_id", "tgr_color")
    process(engine, table, "ep_id", "ep_color", "id", "color")
    process(engine, table, "hauptfunktion_id", "hauptfunktion_color", 
            "oberfunktion_id", "oberfunktion_color")
    process(engine, table, "oberfunktion_id", "oberfunktion_color", 
            "funktion_id", "funktion_color")
    process(engine, table, "hauptgruppe_id", "hauptgruppe_color", 
            "obergruppe_id", "obergruppe_color")
    process(engine, table, "obergruppe_id", "obergruppe_color", 
            "gruppe_id", "gruppe_color")

