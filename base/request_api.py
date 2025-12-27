import json

from conf.config_handler import ConfigHandler

class RequestApi:
    def __init__(self):
        self.conf = ConfigHandler()


    def api_request(self, base_info, test_case):
        """
        接口请求
        :param base_info: yaml文件里面的baseInfo
        :param test_case: yaml文件里面的testCase
        :return:
        """
        request_meta = self._build_request_meta(base_info)
        case_name, test_case, validation, extract, extract_list = self._prepare_test_case(test_case)


        res = self._send_request(request_meta, case_name, test_case)
        self._handle_response(res, validation, extract, extract_list)

    def replace_load(self, data):
        """
        热加载
        :param data:
        :return:
        """
        str_data = data
        if not isinstance(data, str):
            str_data = json.dumps(data, ensure_ascii=False)




    def _build_request_meta(self, base_info):
        """
        构建请求数据
        :param base_info:
        :return:
        """
        url_host = self.conf.get_section_for_data('api_envi', 'host')
        return {
            "api_name": base_info['api_name'],
            "url": url_host + base_info['url'],
            "method": base_info['method'],
            "header": self.replace_load(base_info['header']),
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
        return eval(self.replace_load(cookies))

    def _prepare_test_case(self, test_case):
        """
        准备测试用例
        :param test_case:
        :return:
        """
        case = test_case.copy()

        case_name = case.pop('case_name')
        validation = json.loads(self.replace_load(case.pop('validation')))

        extract = case.pop('extract', None)
        extract_list = case.pop('extract_list', None)

        for k in ('data', 'json', 'params'):
            if k in case:
                case[k] = self.replace_load(case[k])

        return case_name, case, validation, extract, extract_list

    def _send_request(self, meta, case_name, case):
        return self.run.run_main(
            name=meta['api_name'],
            url=meta['url'],
            case_name=case_name,
            header=meta['header'],
            method=meta['method'],
            cookies=meta['cookies'],
            **case
        )

    def _handle_response(self, res, validation, extract, extract_list):
        res_json = res.json()
        if extract:
            self.extract_data(extract, res.text)
        if extract_list:
            self.extract_data_list(extract_list, res.text)

        self.asserts.assert_result(validation, res_json, res.status_code)


