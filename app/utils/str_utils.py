import random
import time

from app.utils.auth_utils import md5


def style_change(old):
    chars = ['_' + c.lower() if c.isupper() else c for c in old]
    return ''.join(chars)


def phone_mask(phone):
    if not phone:
        return phone
    return phone[:3] + '****' + phone[-4:]


def email_mask(email):
    if '@' not in email:
        return email
    return email[:3] + '****' + email[email.rindex('@'):]


def random_upper(x):
    return x if random.randint(0, 1) else x.upper()


def random_hash():
    """
        生成当前时间的md5 hash值
    :return:
    """
    return md5(str(time.time()))


def str_random_upper(s=None):
    """
        随机将字符串某个字符提升为大写
    :param s: 需要处理的数据，默认为 random_hash()
    :return:
    """
    if not s:
        s = random_hash()
    return ''.join(random_upper(c) for c in s)


if __name__ == '__main__':
    print(str_random_upper('helloworld!'))
