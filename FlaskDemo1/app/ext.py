# from flask_caching import Cache
from flask_cache import Cache
from flask_mail import Mail
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
# cache = Cache(config={'CACHE_TYPE': 'redis'})

cache = Cache(config= {'CACHE_TYPE': 'redis',
  'CACHE_REDIS_HOST': '127.0.0.1', # redis ip
  'CACHE_REDIS_PORT': 6379,  # port
  'CACHE_REDIS_DB': '6',   # 使用的redis db
  'CACHE_REDIS_PASSWORD': ''},with_jinja2_ext=False )

mail = Mail()

def init_ext(app):
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    mail.init_app(app)
