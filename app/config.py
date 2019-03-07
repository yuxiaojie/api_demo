import os

import time
from werkzeug.security import generate_password_hash

VERSION_CODE = 1
VERSION_STRING = '2.0.0'

DEBUG = False
APP_SECRET = 'xxxxxxxxx'

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_RECORD_QUERIES = False
SQLALCHEMY_POOL_SIZE = 20
SQLALCHEMY_MAX_OVERFLOW = 30

CELERY_IGNORE_RESULT = True
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
CELERY_TIMEZONE = 'Asia/Shanghai'

# flask缓存配置信息
CACHE_GLOBAL_PREFIX = 'api/'
CACHE_TYPE = 'redis'
CACHE_DEFAULT_TIMEOUT = 120
REDIS_LIST_EXPIRE_TIME = 60 * 60 * 24 * 6


env = os.environ.get('SERVER_ENV', 'dev-mac')
HOST_ID = os.environ.get('HOST_ID', '000')

SESSION_COOKIE_SECURE = True
COORDINATE_CONVERT_FACTOR = 10000000000

MAX_CONTENT_LENGTH = 200 * 1024 * 1024

if env == 'product':
    ENV = 'pro'
    APP_ROOT = '/home/www/flask_demo/'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://api:xxx@127.0.0.1:3306/api_db?charset=utf8mb4'
    LOG_PATH = '/home/log/api'
    CELERY_BROKER_URL = 'redis://:xxxxx@127.0.0.1:6688/1'
    CELERY_RESULT_BACKEND = 'redis://:xxxxx@127.0.0.1:6688/1'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 6688
    CACHE_REDIS_PASSWORD = 'xxxxx'
    CACHE_REDIS_DB = 0


elif 'dev' in env:

    if 'mac' in env:
        LOG_PATH = '~/Documents/log/api'
        APP_ROOT = os.path.abspath('.')
    else:
        LOG_PATH = r'D:\logs\api'
        APP_ROOT = r'D:\workspace\flask_demo'

    ENV = 'dev'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://api:xxx@127.0.0.1:3306/api_db?charset=utf8mb4'
    CELERY_BROKER_URL = 'redis://:xxxxx@127.0.0.1:6688/1'
    CELERY_RESULT_BACKEND = 'redis://:xxxxx@127.0.0.1:6688/1'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 6688
    CACHE_REDIS_PASSWORD = 'xxxxx'
    CACHE_REDIS_DB = 0

else:
    ENV = 'test'
    APP_ROOT = r'/home/www/TissueMachineServer'
    LOG_PATH = '/home/log/api'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://api:xxx@127.0.0.1:3306/api_db?charset=utf8mb4'
    CELERY_BROKER_URL = 'redis://:xxxxx@127.0.0.1:6688/1'
    CELERY_RESULT_BACKEND = 'redis://:xxxxx@127.0.0.1:6688/1'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 6688
    CACHE_REDIS_PASSWORD = 'xxxxx'
    CACHE_REDIS_DB = 0

if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)


def in_product():
    return env == 'product'


def in_test():
    return env == 'test'


def in_develop():
    return 'dev' in env


if __name__ == '__main__':
    print(generate_password_hash(str(time.time())))
    print(os.environ.get('SERVER_ENV', 'test'))
