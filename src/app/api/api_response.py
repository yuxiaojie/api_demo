import time
from functools import wraps

from flask import jsonify
from flask import request

from app.app import JSONEncoder
from app.config import ENV, in_product
from app.utils import logger

SESSION_UID = 'uid'
SESSION_IS_VER_SAFE = 'chanSafe'


def get_json_data():

    """
        将flask中json和form的参数都打包在一起进行获取
    :return:
    """

    if 'union_json_data' not in request.__dict__:
        json_data = request.get_json() if request.get_json() else {}
        try:
            assert type(json_data) is dict
        except AssertionError:
            json_data = {}
        json_data.update({k: v for k, v in request.values.items()})
        request.__dict__['union_json_data'] = json_data
        return json_data
    else:
        return request.__dict__['union_json_data']


def get_response(message='', error_code=0, data=None):

    """
        响应客户端通用json格式
    :param error_code: 错误代码，默认为0表示成功
    :param message: 响应消息
    :param data: 响应数据
    :return:
    """

    response_map = {
        "errorCode": error_code,
        "message": message,
        "serverTime": int(round(time.time() * 1000)),
        "data": data,
    }

    logger.api_logger.info('response : %s',
                           JSONEncoder().encode({k: v for k, v in response_map.items() if k != 'data'}
                                                if ENV == 'pro' else response_map))
    if not in_product():
        print(response_map)
    return jsonify(response_map)


def get_ip(func):
    """
        获取ip的装饰器，装饰函数需带有ip的参数
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper_fun(*args, **kwargs):
        ip = request.headers['X-Forwarded-For'] if 'X-Forwarded-For' in request.headers else request.remote_addr
        if ',' in ip:
            kwargs['ip'] = ip.split(',')[0]
        else:
            kwargs['ip'] = ip
        return func(*args, **kwargs)
    return wrapper_fun
