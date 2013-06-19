import os
from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from config import basedir

rondo = Flask(__name__)
rondo.config.from_object('config')
db = SQLAlchemy(rondo)
lm = LoginManager()
lm.init_app(rondo)
lm.login_view = 'login'
oid = OpenID(rondo, os.path.join(basedir, 'tmp'))
	
from rondo import views, models

if not rondo.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/rondo.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    rondo.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    rondo.logger.addHandler(file_handler)
    rondo.logger.info('rondo event manager')


if __name__ == '__main__':
	login_manager.init_app(app)
	app.run()