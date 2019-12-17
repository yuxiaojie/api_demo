from Crypto.Cipher import AES
import base64

from app.utils.auth_utils import md5


def pkcs7padding(data):
    bs = AES.block_size
    padding = bs - len(data) % bs
    padding_text = chr(padding) * padding
    return data + padding_text.encode()


def pkcs7unpadding(data):
    lengt = len(data)
    unpadding = data[lengt - 1] if type(data[lengt - 1]) is int else ord(data[lengt - 1])
    return data[0:lengt-unpadding]


def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += '=' * (4 - missing_padding)
    return base64.b64decode(data)


class AesCrypter(object):

    def __init__(self, key):
        self.key = key.encode()

    def encrypt(self, data):
        """
            AES 加密， 加密模式ECB，填充：pkcs7padding，密钥长度：256
        :param data:
        :return:
        """
        data = pkcs7padding(data)
        cipher = AES.new(self.key, AES.MODE_ECB)
        encrypted = cipher.encrypt(data)
        return base64.b64encode(encrypted)

    def decrypt(self, data):
        data = base64.b64decode(data)
        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted = cipher.decrypt(data)
        decrypted = pkcs7unpadding(decrypted)
        return decrypted.decode()


if __name__ == '__main__':

    mch_key = md5('1234567890')
    print('key: ', mch_key)
    aes = AesCrypter(mch_key)
    # print(aes.decrypt(s))
    res = aes.encrypt(b'{"cmd":3800, "msg":"request", "extend": null, "digital": 0}').decode(encoding='utf-8')
    print(res)
    print(aes.decrypt(res))
