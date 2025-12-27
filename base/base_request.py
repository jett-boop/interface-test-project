import json

import pytest

from common.get_logger import GetLogger
import requests
from urllib3.exceptions import InsecureRequestWarning
import urllib3

from common.yaml_handler import YamlHandler
from conf import setting

logs = GetLogger.get_logger()

class BaseRequest:

    @staticmethod
    def _send_request(**kwargs):
        """
        发请求，复用cookie
        :param kwargs:
        :return:
        """

        session = requests.session()
        result = None
        cookie = {}
        try:
            result = session.request(**kwargs)
            set_cookie = requests.utils.dict_from_cookiejar(result.cookies)
            if set_cookie:
                cookie['Cookie'] = set_cookie
                YamlHandler.write_yaml_data(cookie)
                logs.info("cookie：%s" % cookie)
            logs.info("接口返回信息：%s" % result.text.strip() if result.text else result)
        except requests.exceptions.ConnectionError:
            logs.error("ConnectionError--连接异常")
            pytest.fail("接口请求异常，可能是request的连接数过多或请求速度过快导致程序报错！")
        except requests.exceptions.HTTPError:
            logs.error("HTTPError--http异常")
        except requests.exceptions.RequestException as e:
            logs.error(e)
            pytest.fail("请求异常，请检查系统或数据是否正常！")
        return result

    def base_request(self, name, url, case_name, header, method, cookies=None, **kwargs):
        """
        接口请求
        :param name: 接口名
        :param url: 接口地址
        :param case_name: 测试用例
        :param header:请求头
        :param method:请求方法
        :param cookies：默认为空
        :param kwargs: 请求参数，根据yaml文件的参数类型
        :return:
        """

        try:
            # 收集报告日志
            logs.info('接口名称：%s' % name)
            logs.info('请求地址：%s' % url)
            logs.info('请求方式：%s' % method)
            logs.info('测试用例名称：%s' % case_name)
            logs.info('请求头：%s' % header)
            logs.info('Cookie：%s' % cookies)
            if "data" in kwargs.keys():
                logs.info("请求参数：%s" % kwargs)
            elif "json" in kwargs.keys():
                logs.info("请求参数：%s" % kwargs)
            elif "params" in kwargs.keys():
                logs.info("请求参数：%s" % kwargs)
        except Exception as e:
            logs.error(e)

        urllib3.disable_warnings(InsecureRequestWarning)
        response = self._send_request(method=method,
                                     url=url,
                                     headers=header,
                                     cookies=cookies,
                                     timeout=setting.API_TIMEOUT,
                                     verify=False,
                                     **kwargs)
        return response