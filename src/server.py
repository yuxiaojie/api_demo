import os
import time

from flask import request, render_template
from flask_cors import CORS

from app import init_app_br
from app.api.api_response import get_json_data
from app.api.api_base import get_docs
from app.app import create_app
from app.config import in_product
from app.utils import logger
from db_base import db

app = create_app()

CORS(app, supports_credentials=True)
logger.init(app)
db.init_app(app)
init_app_br(app)


@app.before_request
def call_before_request():

    if not in_product():
        print('Request path: {}, params: {}'.format(request.path, get_json_data()))

    # print('request.headers : ', request.headers)
    if request.method != 'OPTIONS':
        logger.api_logger.info('Request path: %s, params: %s', request.path, get_json_data())


@app.route('/api-json', methods=['GET'])
def api_doc_json():
    return get_docs()


@app.route('/api', methods=['GET'])
def api_doc():
    return render_template('api_doc.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)
