import csv
import os

from conf.setting import DIR_BASE
from base.get_logger import GetLogger

logs = GetLogger.get_logger()

def read_csv_data(filename):
    try:
        with open(os.path.join(DIR_BASE, 'data/csv_data', filename), 'r', encoding='utf-8') as f:
            return list(csv.reader(f))
    except Exception as e:
        logs.error(e)


if __name__ == '__main__':
    print(read_csv_data('test_data.csv'))