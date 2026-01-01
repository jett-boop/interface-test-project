import random
import re
import time

from common.yaml_handler import YamlHandler
from base.get_logger import GetLogger

logs = GetLogger.get_logger()

class ReflectionHandler:
    def get_extract_data(self, extract_key, randoms=None) -> str:
        """
        获取extract.yaml数据，首先判断randoms是否为数字类型，如果不是就获取下一个node节点的数据
        :param extract_key: extract.yaml文件中的key值
        :param randoms: int类型，0：随机读取；-1：读取全部，返回字符串形式；-2：读取全部，返回列表形式；其他根据列表索引取值，取第一个值为1，第二个为2，以此类推;
        :return:
        """

        try:
            data = YamlHandler.get_extract_yaml(extract_key)
            if randoms is not None and re.fullmatch(r'[-+]?\d+', randoms):
                randoms = int(randoms)
                data_value = {
                    randoms: self.get_extract_order_data(data, randoms),
                    0: random.choice(data),
                    -1: ','.join(data),
                    -2: ','.join(data).split(','),
                }
                data = data_value[randoms]
            else:
                data = YamlHandler.get_extract_yaml(extract_key, randoms)
            return data
        except Exception as e:
            logs.error(f"获取 extract.yaml 中的 {extract_key} 失败，原因：{e}")


    @staticmethod
    def get_extract_order_data(data, randoms):
        """
        获取extract.yaml数据，不为0、-1、-2，则按顺序读取文件key的数据
        :param data:
        :param randoms:
        :return:
        """

        if randoms not in [0, -1, -2]:
            return data[randoms - 1]
        return None

    @staticmethod
    def timestamp():
        """获取当前时间戳，10位"""
        t = int(time.time())
        return t