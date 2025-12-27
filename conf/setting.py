import logging
import os

DIR_BASE = os.path.dirname(os.path.dirname(__file__))

LOG_LEVEL = logging.DEBUG
STREAM_LEVEL = logging.DEBUG

FILE_PATH = {
    'LOG': os.path.join(DIR_BASE, 'logs'),
    'CONFIG': os.path.join(DIR_BASE, 'conf/config.ini'),
}

YAML_FILE_PATH = {
    'LOGIN_NAME_YAML_PATH': './data/loginName.yaml'
}