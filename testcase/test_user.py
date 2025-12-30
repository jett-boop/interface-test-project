import allure
import pytest

from base.generate_id import m_id, c_id
from base.request_api import RequestApi
from common.yaml_handler import YamlHandler
from conf.setting import YAML_FILE_PATH

@allure.feature(next(m_id) + '用户管理模块（单接口）')
class TestUserManager:

    @allure.story(next(c_id) + "新增用户")
    @pytest.mark.order(1)
    @pytest.mark.parametrize('base_info,test_case', YamlHandler.get_testcase_yaml(YAML_FILE_PATH['ADD_USER_YAML_PATH']))
    def test_add_user(self, base_info, test_case):
        RequestApi().api_request(base_info, test_case)

    @allure.story(next(c_id) + "修改用户")
    @pytest.mark.order(2)
    @pytest.mark.parametrize('base_info,test_case',YamlHandler.get_testcase_yaml(YAML_FILE_PATH['UPDATE_USER_YAML_PATH']))
    def test_update_user(self, base_info, test_case):
        RequestApi().api_request(base_info, test_case)

    @allure.story(next(c_id) + "删除用户")
    @pytest.mark.order(3)
    @pytest.mark.parametrize('base_info,test_case',YamlHandler.get_testcase_yaml(YAML_FILE_PATH['DELETE_USER_YAML_PATH']))
    def test_delete_user(self, base_info, test_case):
        RequestApi().api_request(base_info, test_case)

    @allure.story(next(c_id) + "查询用户")
    @pytest.mark.order(4)
    @pytest.mark.parametrize('base_info,test_case',YamlHandler.get_testcase_yaml(YAML_FILE_PATH['QUERY_USER_YAML_PATH']))
    def test_query_user(self, base_info, test_case):
        RequestApi().api_request(base_info, test_case)