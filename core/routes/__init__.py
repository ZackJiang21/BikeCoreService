from .user import user_blueprint
from .bike import bike_blueprint
from .report import report_blueprint


def init_app(app):
    app.register_blueprint(user_blueprint, url_prefix='/api')
    app.register_blueprint(bike_blueprint, url_prefix='/api')
    app.register_blueprint(report_blueprint, url_prefix='/api')
