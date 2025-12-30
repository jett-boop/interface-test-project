import time
import pytest

from common.ding_ding_robot import send_dd_msg
from common.yaml_handler import YamlHandler
from conf.setting import dd_msg

@pytest.fixture(scope="session", autouse=True)
def clear_data():
    # 禁用HTTPS告警，ResourceWarning
    # warnings.simplefilter('ignore', ResourceWarning)

    YamlHandler.clear_extract_yaml_data()

def generate_test_summary(terminalreporter):
    """
    生成自动化测试摘要，并计算执行总时长
    :param terminalreporter: pytest 的 terminalreporter 对象
    :return: summary 字符串
    """
    # 记录开始时间（如果没有记录，就现在记录）
    session = terminalreporter._session
    if not hasattr(session, "_start_time"):
        session._start_time = time.time()

    # 这里假设测试已经执行完，统计各类结果
    total = terminalreporter._numcollected
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    error = len(terminalreporter.stats.get('error', []))
    skipped = len(terminalreporter.stats.get('skipped', []))

    # 计算耗时
    duration = time.time() - session._start_time

    summary = f"""
        自动化测试结果，通知如下，请着重关注测试失败的接口，具体执行结果如下：
        测试用例总数：{total}
        测试通过数：{passed}
        测试失败数：{failed}
        错误数量：{error}
        跳过执行数量：{skipped}
        执行总时长：{duration}秒
        """
    print(summary)
    return summary

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """自动收集pytest框架执行的测试结果并打印摘要信息"""
    summary = generate_test_summary(terminalreporter)
    if dd_msg:
        send_dd_msg(summary)