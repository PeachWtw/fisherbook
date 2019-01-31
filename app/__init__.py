from flask import Flask
# from app.web import web
from app.model.base import db
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()
def create_app():
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_object('app.setting')
    app.config.from_pyfile('secure.py') #用Flask()创建应用时设置了instance_relative_config=True，app.config.from_pyfile()将查看在instance文件夹的特殊文件。
    # app.register_blueprint(web)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或者注册'
    register_blueprint(app)
    mail.init_app(app)
    with app.app_context():
        db.create_all()

    return app


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)