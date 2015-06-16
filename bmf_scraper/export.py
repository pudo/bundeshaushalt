from datetime import datetime
import sqlaload as sl
import sys

def dump_table(engine, table):
    file_name = '%s-%s.csv' % (table.name,
            datetime.utcnow().strftime("%Y-%m-%d"))
    fh = open(file_name, 'wb')
    sl.dump_csv(sl.all(engine, table), fh)

if __name__ == '__main__':
    assert len(sys.argv)==2, "Usage: %s [engine-url]"
    engine = sl.connect(sys.argv[1])
    table = sl.get_table(engine, 'bund')
    dump_table(engine, table)
