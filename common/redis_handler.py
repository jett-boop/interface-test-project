import redis
from redis.cluster import RedisCluster
from common.config_handler import ConfigHandler
from base.get_logger import GetLogger

logs = GetLogger.get_logger()
conf = ConfigHandler()


class RedisHandler:
    def __init__(self):
        redis_conf = {
            'host': conf.get_section_redis('host'),
            'port': conf.get_section_redis('port'),
            'username': conf.get_section_redis('username'),
            'password': conf.get_section_redis('password'),
            'db': conf.get_section_redis('db')
        }
        nodes_list = []
        redis_nodes_str = conf.get_section_redis('startup_nodes')
        if redis_nodes_str:
            try:
                nodes_str_list = redis_nodes_str.split(',')
                for node_str in nodes_str_list:
                    host, port = node_str.split(':')
                    node_data = {'host': host, 'port': port}
                    nodes_list.append(node_data)
                self.redis_cluster = RedisCluster(startup_nodes=nodes_list, decode_responses=True)
                logs.info(f'连接Redis集群服务，host:{redis_nodes_str}')
            except Exception as e:
                logs.error(f'redis连接失败，{e}')
        elif redis_conf['host'] and redis_conf['port']:
            try:
                pool = redis.ConnectionPool(redis_conf)
                # 使用连接池方式，decode_responses=True可自动转为字符串
                self.redis_cluster = redis.Redis(connection_pool=pool, decode_responses=True)
                logs.info(f'连接Redis--host:{redis_conf["host"]}')
            except Exception as e:
                logs.error(f'redis连接失败，{e}')

    def query(self, key):
        """
        获取Redis里面的数据
        :param key: Redis里面的键
        :return:
        """
        try:
            value = self.redis_cluster.get(key)
            return value
        except Exception as e:
            logs.error(f'从Redis中获取[{key}]失败，失败原因{e}')
            raise

    def set(self, key, value, ex=None):
        """
        设置Redis的值
        :param key: Redis里面的键
        :param value: 需要设置的内容
        :param ex: 过期时间，单位(s)
        :return:
        """
        try:
            return self.redis_cluster.set(name=key, value=value, ex=ex)
        except Exception as e:
            logs.error(f'往Redis中设置[{key}]失败，失败原因{e}')
            raise