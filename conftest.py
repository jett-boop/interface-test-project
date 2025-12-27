import warnings

import pytest

from common.yaml_handler import YamlHandler


@pytest.fixture(scope="session", autouse=True)
def clear_data():
    # 禁用HTTPS告警，ResourceWarning
    # warnings.simplefilter('ignore', ResourceWarning)

    YamlHandler.clear_yaml_data()