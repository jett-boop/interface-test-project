import datetime
import logging
import logging.handlers
import os
import time

from conf import setting

log_path = setting.FILE_PATH['LOG']
if not os.path.exists(log_path): os.makedirs(log_path)
logfile_name = log_path + f"\\test.{time.strftime('%Y%m%d')}.log"\

class GetLogger:
    logger = None

    @classmethod
    def get_logger(cls):
        """
        单例获取logger对象
        :return:
        """
        if cls.logger is None:

            cls._clear_overdue_logs(log_path)

            cls.logger = logging.getLogger(__name__)
            cls.logger.setLevel(setting.LOG_LEVEL)

            fmt = (
                "%(levelname)s - %(asctime)s - "
                "%(filename)s:%(lineno)d "
                "- [%(module)s:%(funcName)s] - %(message)s"
            )
            formatter = logging.Formatter(fmt)

            fh = logging.handlers.RotatingFileHandler(
                filename=logfile_name,
                maxBytes=5 * 1024 * 1024,
                backupCount=7,
                encoding="utf-8"
            )
            fh.setLevel(setting.LOG_LEVEL)
            fh.setFormatter(formatter)

            sh = logging.StreamHandler()
            sh.setLevel(setting.STREAM_LEVEL)
            sh.setFormatter(formatter)

            cls.logger.addHandler(fh)
            cls.logger.addHandler(sh)

        return cls.logger

    @staticmethod
    def _clear_overdue_logs(log_dir, days=30):
        """
        处理过期日志文件
        :param log_dir: 日志路径
        :param days: 日志存放时间
        :return:
        :getmtime: 获取文件最后一次被修改的时间
        """
        now = datetime.datetime.now().timestamp()
        expire_time = now - days * 24 * 60 * 60

        for file in os.listdir(log_dir):
            file_path = os.path.join(log_dir, file)
            if os.path.isfile(file_path):
                if os.path.getmtime(file_path) < expire_time:
                    os.remove(file_path)