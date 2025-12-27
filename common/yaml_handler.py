import os

import yaml
from common.get_logger import GetLogger

logs = GetLogger.get_logger()


class YamlHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f'{self.file_path} 不存在')

        with open(self.file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def write(self, data, mode='w'):
        with open(self.file_path, mode, encoding='utf-8') as f:
            yaml.dump(
                data,
                f,
                allow_unicode=True,
                sort_keys=False
            )


