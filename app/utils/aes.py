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
    s = 'NjgjjX2VVwMr8weFZZx0/k811uDeMYplMcLIYoQmb98rN0CSlWdpTxPrP+dHvK1IujVLzZDEjCKvWFOblJh84tZVTIER9DUeEO67Fxt' \
        'q8IYHUvAuhvxDpg2ZNhojm9xyMW8hZZhM7wyqqRfuSAVYE4y4rWu32pO0xMAWPo6X72WuizoJKXFRkvRBHg+lo14oifUwarOhnBZRuoG' \
        '57jW/+leZ17+md75EbNnv+B8xHO1aMzU7DxzYV82K/G6ZQ8DJKdixBjnVxRfuACKrHW8GcR8hg0XNQWX+FWbJTsYtcKWfYumcXbXJrB' \
        'W0+he+nTyrPOaLJXOeiFi+M4cHTNsXPae81i8rrxqGsjEHoRe0GeRtvxgNMEQJQS59mIOSkSQ/EunuorZeMFUVNDofeA7NPzbMOFiSR' \
        'Uzp7Fwyb5q6Oa+uW8WSwcb+YfL/xIH+zP3Rb4fpdqKCchaPCzWIZrT8na6Xaf40DJ2NoMrhuECzb2aqlfyBpLrjPX/+x6LP08C7uA' \
        'OvXmHMxpFC3+Cc9hfoGKMRyKokmT+2IjfmtBWzRRSe2EPHaD6EobueBgxkWucdHvEar2d16+Un1qvhO3wIJVC6IXHCnAjVlVxPDOCN8' \
        'uKfQ8OdMtbdfVaPS//reqeA9qt4nIit8incwPR15rql0Hzkf8enDSwvU0Fj+LdUYmdxqsH6ps4D7f+gBZcK6+hZQIuFrPb6B1xxz+Ml' \
        'KJptVeUyShqGf+kMoI5O9GtswDsSYNOtDKgt2kfym2GL2kPI6+jhJugJeASJj9kROVQRoH96XSochEt1Z8k2B5tmtM9dPuVwus2eJb0' \
        'abiQz1HZkEUKOFe1Aljt1B80FKSdfm7nEuQsDcusLCmOvWAqJjpWUabGaHQy5KbD2I+V6zjQH1Qc1fh8ACDFp7D7X9rEcs6M8APTrYF' \
        '1WF5O3aBFuJvH6N/c3/6PWw9E+zlPqq03cy6mCnShzClWwXNhCMCenvRKHcygJYI2EsrDz5qSQ31PA6gS/RlijxllHKAJp9r9wbruq' \
        'XHrAqmlJS8nL4nmYIAeSUtjouFKDRMCpNm2A20ik3V+vC83XtZrIkZed51ss'

    mch_key = md5('1234567890')
    print('key: ', mch_key)
    aes = AesCrypter(mch_key)
    # print(aes.decrypt(s))
    res = aes.encrypt(b'{"cmd":3800, "msg":"request", "extend": null, "digital": 0}').decode(encoding='utf-8')
    print(res)
    print(aes.decrypt(res))
