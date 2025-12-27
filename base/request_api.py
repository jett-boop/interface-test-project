import json
from json import JSONDecodeError

import jsonpath

from base.base_request import BaseRequest
from common.assertions import Assertions
from common.reflection_handler import ReflectionHandler
from common.yaml_handler import YamlHandler
from conf.config_handler import ConfigHandler
from common.get_logger import GetLogger

logs = GetLogger.get_logger()

class RequestApi:
    def __init__(self):
        self.conf = ConfigHandler()
        self.request = BaseRequest()
        self.asserts = Assertions()


    def api_request(self, base_info, test_case):
        """
        接口请求
        :param base_info: yaml文件里面的baseInfo
        :param test_case: yaml文件里面的testCase
        :return:
        """
        try:
            request_meta = self._build_request_meta(base_info)
            case_name, test_case, validation, extract, extract_list = self._prepare_test_case(test_case)


            result = self._send_request(request_meta, case_name, test_case)
            self._handle_response(result, validation, extract, extract_list)
        except Exception as e:
            raise e

    @staticmethod
    def _replace_load(data):
        """
        热加载
        :param data:
        :return:
        """
        str_data = data
        if not isinstance(data, str):
            str_data = json.dumps(data, ensure_ascii=False)

        for i in range(str_data.count('${')):
            if '${' in str_data and '}' in str_data:
                start_index = str_data.index('$')
                end_index = str_data.index('}', start_index)
                ref_all_params = str_data[start_index:end_index + 1]
                # 取出yaml文件的函数名
                func_name = ref_all_params[2:ref_all_params.index("(")]
                # 取出函数里面的参数
                func_params = ref_all_params[ref_all_params.index("(") + 1:ref_all_params.index(")")]
                # 传入替换的参数获取对应的值,类的反射----getattr,setattr,del....
                extract_data = getattr(ReflectionHandler(), func_name)(*func_params.split(',') if func_params else "")

                if extract_data and isinstance(extract_data, list):
                    extract_data = ','.join(e for e in extract_data)
                str_data = str_data.replace(ref_all_params, str(extract_data))

        # 还原数据
        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data
        return data

    def _build_request_meta(self, base_info):
        """
        构建请求数据
        :param base_info:
        :return:
        """
        url_host = self.conf.get_section_api_env1()
        return {
            "api_name": base_info['api_name'],
            "url": url_host + base_info['url'],
            "method": base_info['method'],
            "header": self._replace_load(base_info['header']),
            "cookies": self._parse_cookie(base_info.get('cookies'))
        }

    def _parse_cookie(self, cookies):
        """
        提取cookie
        :param cookies:
        :return:
        """
        if not cookies:
            return None
        return eval(self._replace_load(cookies))

    def _prepare_test_case(self, test_case):
        """
        准备测试用例
        :param test_case:
        :return:
        """
        case = test_case.copy()

        case_name = case.pop('case_name')
        validation = json.loads(self._replace_load(case.pop('validation')))

        extract = case.pop('extract', None)
        extract_list = case.pop('extract_list', None)

        for k in ('data', 'json', 'params'):
            if k in case:
                case[k] = self._replace_load(case[k])

        return case_name, case, validation, extract, extract_list

    def _send_request(self, meta, case_name, case):
        return self.request.base_request(
            name=meta['api_name'],
            url=meta['url'],
            case_name=case_name,
            header=meta['header'],
            method=meta['method'],
            cookies=meta['cookies'],
            **case
        )

    def _handle_response(self, res, validation, extract, extract_list):
        try:
            result = json.loads(res.text)
            if extract:
                self._extract_data(extract, res.text)
            if extract_list:
                self._extract_data_list(extract_list, res.text)

            self.asserts.assert_result(validation, result, res.status_code)
        except JSONDecodeError as js:
            logs.error('系统异常或接口未请求！')
            raise js
        except Exception as e:
            logs.error(e)
            raise e

    @staticmethod
    def _extract_data(testcase_extract, response):
        """
        提取接口返回值，json提取，提取结果以列表形式返回
        :param testcase_extract:
        :param response:
        :return:
        """
        try:
            for key, value in testcase_extract.items():
                if '$' in value:
                    extract_json = jsonpath.jsonpath(json.loads(response), value)[0]
                    if extract_json:
                        extract_data = {key: extract_json}
                        logs.info('提取接口的返回值：', extract_data)
                    else:
                        extract_data = {key: '未提取到数据，请检查接口返回值是否为空！'}
                    YamlHandler.write_extract_yaml_data(extract_data)
        except:
            logs.error('接口返回值提取异常，请检查yaml文件extract表达式是否正确！')

    @staticmethod
    def _extract_data_list(testcase_extracts, response):
        """
        提取接口多个返回值，json提取，提取结果以列表形式返回
        :param testcase_extracts:
        :param response:
        :return:
        """
        try:
            for key, value in testcase_extracts.items():
                if '$' in value:
                    extracts_json = jsonpath.jsonpath(json.loads(response), value)
                    if extracts_json:
                        extracts_data = {key: extracts_json}
                        logs.info('提取接口的返回值：', extracts_data)
                    else:
                        extracts_data = {key: '未提取到数据，请检查接口返回值是否为空！'}
                    YamlHandler.write_extract_yaml_data(extracts_data)
        except:
            logs.error('接口返回值提取异常，请检查yaml文件extract_list表达式是否正确！')