import allure
import pytest

from base.generate_id import m_id, c_id
from base.request_api import RequestApi
from common.yaml_handler import YamlHandler
from conf.setting import YAML_FILE_PATH

@allure.epic("电商系统")
@allure.feature(next(m_id) + '电子商务管理系统（业务场景）')
class TestProductOrderScenario:

    @allure.story(next(c_id) + "商品列表到下单支付流程")
    @pytest.mark.parametrize('base_info,test_case', YamlHandler.get_testcase_yaml(YAML_FILE_PATH['PRODUCT_ORDER_SCENARIO_YAML_PATH']))
    def test_add_user(self, base_info, test_case):
        RequestApi().api_request(base_info, test_case)