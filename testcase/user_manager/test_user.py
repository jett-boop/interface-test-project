import pytest

from base.request_api import RequestApi
from common.yaml_handler import YamlHandler
from conf.setting import YAML_FILE_PATH


class TestUserManager:

    # 测试用例执行顺序设置
    @pytest.mark.order(1)
    # 参数化，yaml数据驱动
    @pytest.mark.parametrize('base_info,test_case', YamlHandler.get_testcase_yaml(YAML_FILE_PATH['ADD_USER_YAML_PATH']))
    def test_add_user(self, base_info, test_case):
        RequestApi().api_request(base_info, test_case)

    @pytest.mark.order(2)
    @pytest.mark.parametrize('base_info,test_case',YamlHandler.get_testcase_yaml(YAML_FILE_PATH['UPDATE_USER_YAML_PATH']))
    def test_update_user(self, base_info, test_case):
        RequestApi().api_request(base_info, test_case)

    @pytest.mark.order(3)
    @pytest.mark.parametrize('base_info,test_case',YamlHandler.get_testcase_yaml(YAML_FILE_PATH['DELETE_USER_YAML_PATH']))
    def test_delete_user(self, base_info, test_case):
        RequestApi().api_request(base_info, test_case)

    @pytest.mark.order(4)
    @pytest.mark.parametrize('base_info,test_case',YamlHandler.get_testcase_yaml(YAML_FILE_PATH['QUERY_USER_YAML_PATH']))
    def test_query_user(self, base_info, test_case):
        RequestApi().api_request(base_info, test_case)