import base64
import hashlib

from app import app

MATCH = 1
NOT_FIND = -1
TIME_OUT = -2
MISMATCH = -3


def b64decode(content):
    return base64.b64decode(content).decode()


def b64encode(content):
    return base64.b64encode(content.encode()).decode()


def md5(src, upper=False):

    """
        md5加密
    :param src: 原始内容
    :param upper: 结果大小写
    :return:
    """

    md5_tool = hashlib.md5()
    md5_tool.update(src.encode(encoding='utf_8'))

    if upper:
        return md5_tool.hexdigest().upper()
    else:
        return md5_tool.hexdigest()


def sha1(src, upper=False):
    tool = hashlib.sha1()
    tool.update(src.encode('utf-8'))

    if upper:
        return tool.hexdigest().upper()
    else:
        return tool.hexdigest()


def sha256(src, upper=False):
    tool = hashlib.sha256()
    tool.update(src.encode('utf-8'))
    if upper:
        return tool.hexdigest().upper()
    else:
        return tool.hexdigest()


def check_ver_code(phone, edit_ver_code):

    """
        检查验证码
    :param phone: 用户手机号码
    :param edit_ver_code: 输入的验证码
    :return:
    """

    cache_key = 'ver_code/' + phone
    ver_code = app.flask_cache.get(cache_key)

    if not ver_code:
        return NOT_FIND

    if ver_code != edit_ver_code.upper():
        return MISMATCH

    app.flask_cache.cache.delete(cache_key)
    return MATCH


def hash_code(data):
    print('md5: ', md5(data))
    print('sha1: ', sha1(data))
    print('sha256: ', sha256(data))
