import os
from datetime import datetime

from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from werkzeug.routing import BaseConverter

from app.config import APP_SECRET


class JSONEncoder(_JSONEncoder):

    def __init__(self, **kwargs):
        kwargs['ensure_ascii'] = False
        super(JSONEncoder, self).__init__(**kwargs)

    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(o, bytes):
            return o.decode()
        return _JSONEncoder.default(self, o)


class Flask(_Flask):
    json_encoder = JSONEncoder
    jinja_options = dict(
        trim_blocks=True,
        lstrip_blocks=True,
        extensions=[
            'jinja2.ext.autoescape',
            'jinja2.ext.with_',
        ]
    )


class RegexConverter(BaseConverter):

    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]


def create_app(config=None):
    app = Flask(__name__)

    #: load default configuration
    app.config.from_object('app.config')
    app.secret_key = APP_SECRET
    app.project_dir = os.path.dirname(os.path.abspath(__file__))
    app.editor_cfg = {}
    app.url_map.converters['regex'] = RegexConverter

    #: load app sepcified configuration
    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)

    return app
