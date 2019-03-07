from flask import Blueprint


def init_app_br(app):
    from app.api.views import view_demo

    api = Blueprint('api', __name__)
    view_demo.api.register(api)

    app.register_blueprint(api, url_prefix='/api')

    from app.api.v2 import view_demo
    v2 = Blueprint('api/v2', __name__)
    view_demo.api.register(v2)
    app.register_blueprint(v2, url_prefix='/api/v2')


