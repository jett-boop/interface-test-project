import configparser

from conf import setting
from base.get_logger import GetLogger

logs = GetLogger.get_logger()

class ConfigHandler:
    """
    读取config.ini文件
    """
    def __init__(self):
        self.__file_path = setting.FILE_PATH['CONFIG']
        self.conf = configparser.ConfigParser()
        try:
            self.conf.read(self.__file_path, encoding='utf-8')
        except Exception as e:
            logs.exception(f"读取配置文件失败: {e}")

    def get_section_for_data(self, section, option):
        """
        :param section: ini文件头部值
        :param option:头部值下面的选项
        :return:
        """
        try:
            return self.conf.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError):
            logs.error(f"配置缺失 [{section}] {option}")
            raise

    def get_section_api_env1(self):
        return self.get_section_for_data("api_env1", "host")
