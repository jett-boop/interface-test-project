import os
import traceback

import yaml

from base.get_logger import GetLogger
from conf.setting import FILE_PATH

logs = GetLogger.get_logger()


class YamlHandler:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f'{self.file_path} 不存在')

        with open(self.file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def write(self, data, mode='w'):
        with open(self.file_path, mode, encoding='utf-8') as f:
            yaml.dump(
                data,
                f,
                allow_unicode=True,
                sort_keys=False
            )

    @staticmethod
    def get_testcase_yaml(file):
        """
        提取测试用例
        :param file:
        :return:
        """

        testcase_list = []
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

                if not data:
                    logs.error(f"[{file}] YAML 文件为空或解析失败")
                    return []

                if not isinstance(data, list):
                    logs.error(f"[{file}] YAML 最外层必须是 list")
                    return []

                for item in data:
                    if not isinstance(item, dict):
                        logs.error(f"[{file}] 用例结构非法（非 dict）：{item}")
                        continue

                    if "baseInfo" not in item or "testCase" not in item:
                        logs.error(f"[{file}] 用例缺少 baseInfo 或 testCase，非法用例：{item}")
                        continue

                    base_info = item.get("baseInfo")
                    test_cases = item.get("testCase")

                    if not base_info or not test_cases:
                        logs.error(f"[{file}] baseInfo 或 testCase 为空：{item}")
                        continue

                    for tc in test_cases:
                        testcase_list.append((base_info, tc))

                return testcase_list

        except UnicodeDecodeError:
            logs.error(f"[{file}] 文件编码错误，请使用 UTF-8")
        except FileNotFoundError:
            logs.error(f"[{file}] 文件未找到")
        except Exception as e:
            logs.error(f"[{file}] 解析用例失败：{e}")

    @staticmethod
    def get_extract_yaml(node_name, second_node_name=None):
        """
        用于读取extract的变量值
        :param node_name:一级节点
        :param second_node_name:二级节点
        :return:
        """

        if os.path.exists(FILE_PATH['EXTRACT']):
            pass
        else:
            logs.error('extract.yaml不存在')
            file = open(FILE_PATH['EXTRACT'], 'w')
            file.close()
            logs.info('extract.yaml创建成功！')
        try:
            with open(FILE_PATH['EXTRACT'], 'r', encoding='utf-8') as rf:
                extract_data = yaml.safe_load(rf)
                if second_node_name is None:
                    return extract_data[node_name]
                else:
                    return extract_data[node_name][second_node_name]
        except KeyError as e:
            raise KeyError(
                f"extract.yaml 中不存在节点：{node_name}"
                + (f".{second_node_name}" if second_node_name else "")
            ) from e

    @staticmethod
    def write_extract_yaml_data(value):
        """
        写入数据需为dict，allow_unicode=True表示写入中文，sort_keys按顺序写入
        写入YAML文件数据,主要用于接口关联
        规则：
        1. 若 key 不存在 → 写入
        2. 若 key 存在且 value 相同 → 不处理
        3. 若 key 存在但 value 不同 → 覆盖
        :param value: 写入数据，必须用dict
        :return:
        """

        file_path = FILE_PATH['EXTRACT']
        if not os.path.exists(file_path):
            open(file_path, 'w', encoding='utf-8').close()
        try:
            with open(file_path, 'r', encoding='utf-8') as rf:
                origin_data = yaml.safe_load(rf) or {}

            updated = False

            for key, new_value in value.items():
                if key not in origin_data:
                    origin_data[key] = new_value
                    updated = True
                else:
                    if origin_data[key] != new_value:
                        origin_data[key] = new_value
                        updated = True

            if updated:
                with open(file_path, 'w', encoding='utf-8') as wf:
                    yaml.dump(
                        origin_data,
                        wf,
                        allow_unicode=True,
                        sort_keys=False
                    )
        except Exception:
            logs.error(str(traceback.format_exc()))

    @staticmethod
    def clear_extract_yaml_data():
        """
        清空extract.yaml文件数据
        :return:
        """

        with open(FILE_PATH['EXTRACT'], 'w') as f:
            f.truncate()