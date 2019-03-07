import logging
import os
from logging.handlers import WatchedFileHandler

from app.config import LOG_PATH


api_logger = None


def init(app):

    info_log = os.path.join(LOG_PATH, 'api.log')
    handler = logging.handlers.WatchedFileHandler(info_log, encoding='utf-8')
    handler.setLevel(logging.INFO)
    logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(logging_format)

    global api_logger
    api_logger = logging.getLogger('mFileLogger')
    api_logger.addHandler(handler)
    api_logger.setLevel(logging.INFO)
