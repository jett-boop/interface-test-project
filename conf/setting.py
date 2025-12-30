import logging
import os

DIR_BASE = os.path.dirname(os.path.dirname(__file__))

LOG_LEVEL = logging.DEBUG
STREAM_LEVEL = logging.DEBUG

# 接口超时时间，单位/s
API_TIMEOUT = 60

# 是否发送钉钉消息
dd_msg = False

FILE_PATH = {
    'LOG': os.path.join(DIR_BASE, 'logs'),
    'CONFIG': os.path.join(DIR_BASE, 'conf/config.ini'),
    'EXTRACT': os.path.join(DIR_BASE, 'data/extract.yaml'),
}

YAML_FILE_PATH = {
    'LOGIN_NAME_YAML_PATH': './data/login/login_name.yaml',
    'ADD_USER_YAML_PATH': './data/user_manage/add_user.yaml',
    'UPDATE_USER_YAML_PATH': './data/user_manage/update_user.yaml',
    'DELETE_USER_YAML_PATH': './data/user_manage/delete_user.yaml',
    'QUERY_USER_YAML_PATH': './data/user_manage/query_user.yaml',
}