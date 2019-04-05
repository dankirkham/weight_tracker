import os
from flask import Flask


def create_app(test_config=None):
    # Create and Configure App
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'weight_tracker.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import measurements
    app.register_blueprint(measurements.bp)
    app.add_url_rule('/', endpoint='index')

    # simple hellow world page
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app