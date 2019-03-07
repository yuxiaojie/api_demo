import os
import random
import time
from urllib.request import urlopen
import io

import qrcode
from PIL import Image, ImageDraw, ImageFont

from app.config import CDN_SERVER, HOST_ID, APP_ROOT
from app.utils import ali_oss_helper
from app.utils.auth_utils import md5

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
ALLOWED_VIDEO_EXTENSIONS = {'avi', 'rmvb', 'rm', 'asf', 'divx', 'mpg', 'mpeg', 'mpe', 'wmv', 'mp4', 'mkv', 'vob'}


class FileWrap:

    def __init__(self, fp):
        self.data = open(fp, 'rb').read()

    def read(self):
        return self.data


menlo = FileWrap(os.path.join(APP_ROOT, 'app', 'utils', 'Menlo.ttc'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def allowed_video(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_VIDEO_EXTENSIONS


def get_and_save_img(img_url):
    file = io.BytesIO(urlopen(img_url).read())
    return save_img(file)


def _gen_file_name():
    now = str(int(time.time() * 1000))
    return md5(now + HOST_ID) + now


def save_img(img):
    return save_file(img)


def save_file(new_file):
    ext = new_file.filename[new_file.filename.rfind('.'):]
    img_name = _gen_file_name() + ext
    return ali_oss_helper.save_img(img_name, new_file)


def save(file_name, content):
    ext = file_name[file_name.rfind('.'):]
    img_name = _gen_file_name() + ext
    return ali_oss_helper.save_img(img_name, content)


def get_img_url(thumb, img, high=-1, width=-1):

    if not img:
        return img

    if high != -1 and width != -1:
        return CDN_SERVER + img + '?x-oss-process=image/resize,m_fill,h_{},w_{}'.format(high, width)
    if thumb:
        return CDN_SERVER + img + '?x-oss-process=image/resize,m_fill,h_100,w_120'
    else:
        return CDN_SERVER + img


def gen_sn_qr(sn, text='', output=''):
    """
        生成sn码的二维码
    :param sn:  设备sn码，用于显示在二维码下方及图片名称
    :param text: 二维码内容，默认为空字符串则二维码内容为sn码, 如果内容带有{sn}则会自动将文本内容的{sn}填充为sn码
    :param output: 图片输出目录，默认为空表示当前目录
    :return:
    """

    qr = qrcode.QRCode(version=5, box_size=5, border=4)

    if not text:
        text = sn
    elif '{sn}' in text:
        text = text.format(sn=sn)

    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image()
    img = img.convert("RGBA")

    bg = Image.new('RGB', (300, 300), (255, 255, 255))
    bg.paste(img, ((300 - img.width) // 2, 0))

    dr = ImageDraw.Draw(bg)
    font = ImageFont.truetype(menlo, 30)
    dr.text((100, img.height), sn, font=font, fill='#000000')
    bg.save(os.path.join(output if output else '.', sn + '.png'))


def save_cert(chan, local_file_name):

    return ali_oss_helper.save_cert('cert/'+chan, local_file_name)