import allure
import pytest

from base.generate_id import m_id, c_id
from base.request_api import RequestApi
from common.yaml_handler import YamlHandler
from conf.setting import YAML_FILE_PATH

@allure.epic("电商系统")
@allure.feature(next(m_id) + '商品管理模块（单接口）')
class TestProductManager:

    @allure.story(next(c_id) + "获取商品列表")
    @pytest.mark.order(1)
    @pytest.mark.parametrize('base_info,test_case', YamlHandler.get_testcase_yaml(YAML_FILE_PATH['GET_PRODUCT_LIST_YAML_PATH']))
    def test_get_product_list(self, base_info, test_case):
        RequestApi().api_request(base_info, test_case)

    @allure.story(next(c_id) + "获取商品详情信息")
    @pytest.mark.order(2)
    @pytest.mark.parametrize('base_info,test_case',YamlHandler.get_testcase_yaml(YAML_FILE_PATH['GET_PRODUCT_DETAIL_YAML_PATH']))
    def test_update_user(self, base_info, test_case):
        RequestApi().api_request(base_info, test_case)

    @allure.story(next(c_id) + "提交订单")
    @pytest.mark.order(3)
    @pytest.mark.parametrize('base_info,test_case',YamlHandler.get_testcase_yaml(YAML_FILE_PATH['COMMIT_ORDER_YAML_PATH']))
    def test_delete_user(self, base_info, test_case):
        RequestApi().api_request(base_info, test_case)

    @allure.story(next(c_id) + "订单支付")
    @pytest.mark.order(4)
    @pytest.mark.parametrize('base_info,test_case',YamlHandler.get_testcase_yaml(YAML_FILE_PATH['ORDER_PAY_YAML_PATH']))
    def test_query_user(self, base_info, test_case):
        RequestApi().api_request(base_info, test_case)