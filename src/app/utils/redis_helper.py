import redis
import logging

from app.config import CACHE_REDIS_HOST, CACHE_REDIS_PORT, CACHE_REDIS_PASSWORD


class CrawlerRedis:
    __redisPool = None

    def __init__(self, db=0):
        try:
            r = redis.ConnectionPool(host=CACHE_REDIS_HOST, port=CACHE_REDIS_PORT, password=CACHE_REDIS_PASSWORD, db=db)
            self.__redisPool = redis.Redis(connection_pool=r)
        except Exception as e:
            logging.error('init redis error: ' + str(e))

    def get_redis_pool(self):
        return self.__redisPool


redis_manage = CrawlerRedis()
device_stat_redis = CrawlerRedis(db=2)
cmd_stat_redis = CrawlerRedis(db=3)
game_order_redis = CrawlerRedis(db=4)
