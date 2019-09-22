
class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:rock1204@127.0.0.1:3306/python920'

    # 邮箱配置
    MAIL_SERVER = 'smtp.163.com'
    MAIL_USERNAME = 'zhengxueyong12@163.com'
    MAIL_PASSWORD = 'rock1204'


config = {
    'develop': DevelopConfig,
    'default': DevelopConfig
}

def init_settings(app, env_name):
    app.config.from_object(config.get(env_name))