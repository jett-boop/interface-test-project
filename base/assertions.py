import operator

import jsonpath

from base.get_logger import GetLogger

logs = GetLogger.get_logger()

class Assertions:
    def assert_result(self, expected, response, status_code):
        """
        断言，通过断言all_flag标记，all_flag==0表示测试通过，否则为失败
        :param expected: 预期结果
        :param response: 实际响应结果
        :param status_code: 响应code码
        :return:
        """
        all_flag = 0
        try:
            logs.info("yaml文件预期结果：%s" % expected)
            for yq in expected:
                for key, value in yq.items():
                    if key == "contains":
                        flag = self._contains_assert(value, response, status_code)
                        all_flag = all_flag + flag
                    elif key == "eq":
                        flag = self._equal_assert(value, response)
                        all_flag = all_flag + flag
                    else:
                        logs.error("不支持此种断言方式")

        except Exception as exceptions:
            logs.error('接口断言异常，请检查yaml预期结果值是否正确填写!')
            raise exceptions

        if all_flag == 0:
            logs.info("测试成功")
            assert True
        else:
            logs.error("测试失败")
            assert False

    @staticmethod
    def _contains_assert(expected, response, status_code):
        """
        字符串包含断言模式，断言预期结果的字符串是否包含在接口的响应信息中
        :param expected: 预期结果，yaml文件的预期结果值
        :param response: 接口实际响应结果
        :param status_code: 响应状态码
        :return: 返回结果的状态标识
        """
        # 断言状态标识，0成功，其他失败
        flag = 0
        for assert_key, assert_value in expected.items():
            if assert_key == "status_code":
                if assert_value != status_code:
                    flag += 1
                    logs.error("contains断言失败：接口返回码【%s】不等于【%s】" % (status_code, assert_value))
            else:
                # 递归查找所有 key 名称等于 assert_key 的字段
                response_list = jsonpath.jsonpath(response, "$..%s" % assert_key)
                if isinstance(response_list[0], str):
                    response_list = ''.join(response_list)
                if response_list:
                    assert_value = None if assert_value.upper() == 'NONE' else assert_value
                    if assert_value in response_list:
                        logs.info("字符串包含断言成功：预期结果【%s】,实际结果【%s】" % (assert_value, response_list))
                    else:
                        flag = flag + 1
                        logs.error("响应文本断言失败：预期结果为【%s】,实际结果为【%s】" % (assert_value, response_list))
        return flag

    @staticmethod
    def _equal_assert(expected_results, actual_results):
        """
        相等断言模式
        :param expected_results: 预期结果，yaml文件validation值
        :param actual_results: 接口实际响应结果
        :return:
        """
        flag = 0
        if isinstance(actual_results, dict) and isinstance(expected_results, dict):
            # 找出实际结果与预期结果共同的key
            common_keys = list(expected_results.keys() & actual_results.keys())[0]
            # 根据相同的key去实际结果中获取，并重新生成一个实际结果的字典
            new_actual_results = {common_keys: actual_results[common_keys]}
            eq_assert = operator.eq(new_actual_results, expected_results)
            if eq_assert:
                logs.info(f"相等断言成功：接口实际结果：{new_actual_results}，等于预期结果：" + str(expected_results))
            else:
                flag += 1
                logs.error(f"相等断言失败：接口实际结果{new_actual_results}，不等于预期结果：" + str(expected_results))
        else:
            flag += 1
            raise TypeError('相等断言--类型错误，预期结果和接口实际响应结果必须为字典类型！')
        return flag