import logging
import os

DIR_BASE = os.path.dirname(os.path.dirname(__file__))

LOG_LEVEL = logging.DEBUG
STREAM_LEVEL = logging.DEBUG

# 接口超时时间，单位/s
API_TIMEOUT = 60

FILE_PATH = {
    'LOG': os.path.join(DIR_BASE, 'logs'),
    'CONFIG': os.path.join(DIR_BASE, 'conf/config.ini'),
    'EXTRACT': os.path.join(DIR_BASE, 'extract.yaml'),
}

YAML_FILE_PATH = {
    'LOGIN_NAME_YAML_PATH': './data/login_name.yaml'
}