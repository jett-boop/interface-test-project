import allure
import pytest

from common.get_logger import GetLogger
from common.read_yaml import get_testcase_yaml
from conf.setting import YAML_FILE_PATH

logs = GetLogger.get_logger()

@pytest.fixture(autouse=True)
def start_test_and_end():
    logs.info('-------------接口测试开始--------------')
    yield
    logs.info('-------------接口测试结束--------------')

@pytest.fixture(scope='session', autouse=True)
@allure.story("登录")
def system_login():
    try:
        api_info = get_testcase_yaml(YAML_FILE_PATH['LOGIN_NAME_YAML_PATH'])

    except Exception as e:
        logs.error(f'登录接口出现异常，导致后续接口无法继续运行，请检查程序！，{e}')
        exit()