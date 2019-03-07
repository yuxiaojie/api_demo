# encoding=utf-8
import base64
import hashlib
from Crypto.Cipher import DES3

import time

# from app import app
from app import app

MATCH = 1
NOT_FIND = -1
TIME_OUT = -2
MISMATCH = -3

BS = DES3.block_size


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


def pad(s):
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode()


def unpad(s):
    return s[0:-ord(s[-1])]


class Prpcrypt(object):
    def __init__(self, key, iv):
        self.key = key
        self.mode = DES3.MODE_CBC
        self.iv = iv.encode()

    def encrypt(self, text):
        text = pad(text.encode())
        cryptor = DES3.new(self.key, self.mode, self.iv)
        x = len(text) % 8
        if x != 0:
            text = text + '\0' * (8 - x)
        # print(text)
        self.ciphertext = cryptor.encrypt(text)
        return base64.standard_b64encode(self.ciphertext).decode("utf-8")

    def decrypt(self, text):
        cryptor = DES3.new(self.key, self.mode, self.iv)
        de_text = base64.standard_b64decode(text.encode())
        plain_text = cryptor.decrypt(de_text)
        st = str(plain_text.decode('utf-8', 'ignore')).rstrip('\0')
        out = unpad(st)
        return out


def hash_code(data):
    print('md5: ', md5(data))
    print('sha1: ', sha1(data))
    print('sha256: ', sha256(data))


if __name__ == '__main__':
    pc = Prpcrypt('OWJjQbOBkOt3MjtGRWPGYcgP', 'LScJ5bkE')
    # # print(sha1(''))
    # # print(md5('123456'))
    # e = pc.encrypt("华永星")  # 加密内容
    d = pc.decrypt('6A7Jsw3jPH+q+vigThqvpmtblLTWmu00s00VySK3Yhu/cT0lwJZZTDO4Ka2W/x7LO0fAQOlLAq0mhCP5s68y0RDzsTgFNcDsftgNS8SVj+uzeNGn8+vOUrrTxz+nBRJ6EjCMVVl924Ivux0p5gwE11feJi8ifvT1E2i7xboqNcdrIypNtzxMzHcClC6PuPC70WBU4tp+MP52tuez/X4CyqhxIQdKNDbrT7lEqEUQ9c3SY/V/UkxdzQmSVTqSYAK5YS4KOOmPy/w+Ql4bP+RUw8f07XC5uLKxdzPiB71hOx12lXvsqqU2qHyVreLW+bpq3hMal6TTpVZv5Nkg9SHG5v4EpQexyTzahgfa3RwnYapj19RHTbP00sfrRJdA97aX')
    print(d)
    # print("加密后%s,解密后%s" % (e, d))

    # hash_code('10004304' + '17')
    # print(sha1('jsapi_ticket=kgt8ON7yVITDhtdwci0qeW9NRvqUmgG_qWPadGfUN2F4NAQ8EEwdbmWSpN4trP1jPAR8D2hFNX42QaSLIyFDKg&noncestr=15887dc079e4f088bc84da1439be387f&timestamp=1543836951&url=http://tmp.beesmartnet.com/static/platform/index.html'))
    # print(sha1('ddddd'))
