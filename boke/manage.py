import redis
from flask import Flask
from flask_script import Manager
from flask_session import Session

from back.models import db
from back.views import back_blueprint
from web.views import  web_blueprint

app = Flask(__name__)
# 第三步: 注册蓝图，可以使用蓝图blue管理路由了
app.register_blueprint(blueprint=back_blueprint, url_prefix='/back')
app.register_blueprint(blueprint=web_blueprint, url_prefix='/web')
# 配置数据库连接信息
# dialect+driver://username:password@host:port/database
# mysql+pymysql://root:123456@127.0.0.1:3306/szflask1
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rock1204@127.0.0.1:3306/blog'
app.config['SQLALCHEMY_TRACK_MODIFACTIONS'] =False
app.config['SESSION_TYPE']='redis'
app.config['SESSION_REDIS']=redis.Redis(host='127.0.0.1',port=6379)

app.secret_key='ffddffdfdfdfdfd434334'
Session(app)
db.init_app(app)

if __name__ == '__main__':
    manage = Manager(app)
    manage.run()



