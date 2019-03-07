import random
from functools import wraps

from app import app
from app.config import CACHE_GLOBAL_PREFIX
from app.utils.redis_helper import redis_manage


class CachePrefix:
    API_ADDRESS_BASE_LOC = 'address/baseLoc/'
    API_VER_CODE = 'verCode/'
    API_SALT = 'salt/'
    API_SID = 'sid/'
    API_TASK_DEVICE = 'taskDevice/'
    API_FREE_REGISTER = 'free/'
    API_DEVICE_UPGRADE = 'dUpgrade/'

    DB_VERSION_COUNT = 'versionCount/'
    DB_CDC_COUNT = 'cdcCount/'
    DB_VERSION_LIST = 'dvList/'
    DB_VERSION_ITEM = 'dvItem/'
    DB_DEVICE_CMD = 'deviceCmd/'
    DB_QR_GEN = 'qrGen/'
    DB_DEVICE = 'device/'
    DB_DEVICE_COUNT = 'deviceCount/'
    DB_DEVICE_CITY_LIST = 'deviceCityList/'
    DB_DEVICE_TYPE_MAP = 'deviceTypeMap/'
    DB_DEVICE_CHAN_CITY_LIST = 'deviceChanCityList/'
    DB_DEVICE_TYPE = 'deviceType/'
    DB_DEVICE_TYPE_AUTH = 'deviceTypeAuth/'
    DB_DEVICE_DEFINE = 'deviceDefine/'
    DB_DEVICE_CHANNEL = 'deviceChannel/'
    DB_DEVICE_CHANNEL_LIST = 'dcList/'
    DB_DEVICE_CHANNEL_MAP = 'dcMap/'
    DB_DEVICE_TYPE_DICT = 'deviceTypeDict/'
    DB_DEVICE_ALIAS = 'deviceAlias/'
    DB_CHAN_DEVICE_TYPE = 'chanDeviceType/'
    DB_USER_CMD = 'udCmd/'
    DB_USER_CMD_LIST = 'udCmdList/'
    DB_DEVICE_CHAN_BIND = 'deviceChanBind/'
    DB_MONITOR_LIST = 'monitorList/'
    DB_MONITOR_NEW_LIST = 'monitorNewList/'
    DB_DEVICE_DISCOUNT = 'deviceDiscount/'
    DB_DEVICE_ACTION = 'deviceAction/'
    DB_ORDER = 'order/'
    DB_ORDER_COUNT = 'orderCount/'
    DB_USER_LOGIN = 'userLogin/'
    DB_DEVICE_AGENT = 'deviceAgent/'
    DB_PERMISSION = 'permission/'
    DB_PERMISSION_LIST = 'permissionList/'
    DB_PERMISSION_BIND = 'permissionBind/'
    DB_ALARM_TODAY = 'alarmToday/'
    DB_CHAN_AGENT = 'deviceChanAgent/'
    DB_LOC_PROVINCE = 'locProvince/'
    DB_LOC_CITY = 'locCity/'
    DB_TAG = 'tag/'
    DB_DEVICE_TASK = 'task/'
    DB_DEVICE_BUFF = 'buff/'
    DB_GAME_ORDER = 'orderGame/'
    DB_WX_CONFIG = 'wxCfg/'
    DB_HX_PAY_ORDER = 'hxOrderId/'
    DB_WX_CODE = 'wxCode/'
    DB_CONFIG_LOG = 'configLog/'
    DB_TOTAL_INCOME = 'totalIncome/'
    DB_TODAY_INCOME = 'todayIncome/'
    DB_ALL_INCOME = 'allIncome/'
    DB_MONTH_INCOME = 'monthIncome/'
    DB_ALL_FANS = 'allFans/'
    DB_TODAY_FANS = 'todayFans/'
    DB_GRID_INFO = 'gridInfo/'
    DB_PLAYABLE = 'playable/'
    DB_PCD = 'pcd/'
    DB_DEVICE_START = 'deviceStart/'
    DB_GRID_ID_START = 'gridIdStart/'
    DB_CHAN_MONITOR_LIST = 'chanMonitorList/'


def api_cache(prefix='tm/', ignore_first=True, timeout=60, name='', noneable=False, random_timeout=None):
    def decorator(func):
        @wraps(func)
        def wrapper_fun(*args, **kwargs):

            none_flag = '!#$ None $#!'
            key_time = random_timeout[0] + random.randint(0, random_timeout[1]) if random_timeout else timeout
            pos_key = '/'.join([str(arg) for arg in args[1 if ignore_first else 0:]])
            kwargs_key = '/'.join([str(kwargs[key]) for key in kwargs])
            cache_key = CACHE_GLOBAL_PREFIX + prefix + pos_key + ('/' + kwargs_key if pos_key else kwargs_key)

            if name:
                cache_key += name

            cache = app.flask_cache.get(cache_key)
            if noneable and type(cache) is str and cache == none_flag:
                return
            if cache:
                return cache

            exe_res = func(*args, **kwargs)

            if exe_res is not None:
                app.flask_cache.set(cache_key, exe_res, timeout=key_time)
            elif noneable:
                app.flask_cache.set(cache_key, none_flag, timeout=key_time)
            return exe_res
        return wrapper_fun
    return decorator


def clear_api_cache(prefix='tm/', *args, **kwargs):

    pos_key = '/'.join([str(arg) for arg in args])
    kwargs_key = '/'.join([str(kwargs[key]) for key in kwargs])
    cache_key = CACHE_GLOBAL_PREFIX + prefix + pos_key + ('/' + kwargs_key if pos_key else kwargs_key)

    app.flask_cache.delete(cache_key)


def clear_cache_fuzzy(*fuzzy_keys):

    if not fuzzy_keys:
        return

    pool = redis_manage.get_redis_pool()
    pipe = pool.pipeline()
    for fk in fuzzy_keys:
        pipe.keys('flask_cache_{}{}*'.format(CACHE_GLOBAL_PREFIX, fk))

    find = pipe.execute()
    for line in find:
        for k in line:
            pipe.delete(k.decode())
    pipe.execute()


def get(cache_key):
    return app.flask_cache.get(CACHE_GLOBAL_PREFIX + cache_key)


def save(cache_key, data, timeout=50):
    return app.flask_cache.set(CACHE_GLOBAL_PREFIX + cache_key, data, timeout=timeout)


def remove(cache_key):
    return app.flask_cache.delete(CACHE_GLOBAL_PREFIX + cache_key)


if __name__ == '__main__':
    clear_cache_fuzzy(CachePrefix.DB_DEVICE_CHANNEL_LIST, CachePrefix.DB_DEVICE_CHANNEL_MAP)
