import yaml
from common.get_logger import GetLogger

logs = GetLogger.get_logger()

class TestcaseParser:

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
                        testcase_list.append({"baseInfo": base_info, "testCase": tc})

                return testcase_list

        except UnicodeDecodeError:
            logs.error(f"[{file}] 文件编码错误，请使用 UTF-8")
        except FileNotFoundError:
            logs.error(f"[{file}] 文件未找到")
        except Exception as e:
            logs.error(f"[{file}] 解析用例失败：{e}")
