import os

from flask import Flask, redirect


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'checkIn.sqlite')
    )

    if not test_config:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 确保实例文件夹存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return redirect('/face')

    from checkIn import db
    db.init_app(app)

    from checkIn import auth, user, face
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(face.bp)
    app.add_url_rule('/', endpoint='index')

    return app
