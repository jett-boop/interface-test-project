import pymysql

from common.config_handler import ConfigHandler
from base.get_logger import GetLogger

logs = GetLogger.get_logger()
conf = ConfigHandler()

class MysqlHandler:
    def __init__(self):
        mysql_conf = {
            'host': conf.get_section_mysql('host'),
            'port': int(conf.get_section_mysql('port')),
            'user': conf.get_section_mysql('username'),
            'password': conf.get_section_mysql('password'),
            'database': conf.get_section_mysql('database')
        }

        try:
            self.conn = pymysql.connect(**mysql_conf, charset='utf8')
            # cursor=pymysql.cursors.DictCursor,将数据库表字段显示，以key-value形式展示
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            logs.info("""成功连接到mysql---
                    host：{host}
                    port：{port}
                    db：{database}
                    """.format(**mysql_conf))
        except Exception as e:
            logs.error(f"except:{e}")
            raise

    def close(self):
        if self.conn and self.cursor:
            self.cursor.close()
            self.conn.close()
        return True

    def query_all(self, sql):
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            logs.error(e)
            raise
        finally:
            self.close()

    def delete(self, sql):
        try:
            rows = self.cursor.execute(sql)
            self.conn.commit()
            logs.info(f'删除成功，影响行数: {rows}')
            return rows
        except Exception as e:
            self.conn.rollback()
            logs.error(e)
            raise
        finally:
            self.close()
