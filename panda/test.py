import pandas as pd
import numpy as np
import sys

def format_type(str):
    if 'int' in str:
        return 'BIGINT'
    elif 'varchar' in str:
        return 'STRING'
    elif 'datetime' in str:
        return 'DATETIME'
    elif 'double' in str:
        return 'DOUBLE'
    else:
        return 'STRING'

def process(sht, name):
    tem = f'create table if not exists {name}(\n'
    colm = sht.ix[:,['表名称', name, '表中文释义']].values

    for i in colm[1:]:
        tem += i[0] + ' ' + i[1] + ' COMMENT ' + (i[2] or '') + ',\n'

    tem = tem[:-2]
    tem += '):'
    print(tem)
    return tem


def run(name):
    pf = pd.read_excel(name, sheetname=None)

    for i in pf:
        process(pf.get(i), i)

if __name__ == "__main__":

    name = sys.argv[1]
    run(name)