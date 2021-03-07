import os
from datetime import timedelta


POSTGRES = {
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'pw': os.getenv('POSTGRES_PASSWORD', 'kalix.123'),
    'db': os.getenv('POSTGRES_DB', 'feme'),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', 5432),
}

TEST_POSTGRES = {
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'pw': os.getenv('POSTGRES_PASSWORD', 'kalix.123'),
    'db': os.getenv('POSTGRES_DB', 'test-feme'),
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', 5432),
}


class Config:
    ERROR_404_HELP = False

    SECRET_KEY = os.getenv('APP_SECRET', 'secret key')

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(
        **POSTGRES)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DOC_USERNAME = 'api'
    DOC_PASSWORD = 'password'

    # Security Settings
    # https://pythonhosted.org/Flask-Security/configuration.html
    # https://pythonhosted.org/Flask-JWT/
    JWT_EXPIRATION_DELTA = timedelta(days=30)
    JWT_AUTH_URL_RULE = '/dev-api/v1/auth'
    JWT_AUTH_USERNAME_KEY = 'username'
    JWT_AUTH_PASSWORD_KEY = 'password'
    SECURITY_URL_PREFIX = '/dev-api/v1/'
    SECURITY_CONFIRMABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_PASSWORD_SALT = 'add_salt'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FEME_CONFIG_PATH = '/Users/sunlingfeng/Documents/project/another/ccme/matchingengine/src/main/resources/quickfix/examples/ordermatch/marketclient.cfg'
    FEMD_CONFIG_PATH = '/Users/sunlingfeng/Documents/project/another/ccme/marketdata/src/main/resources/quickfix/examples/executor/executor.cfg'




class DevConfig(Config):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'feme.sqlite')
    DEBUG = True


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}'.format(
        **TEST_POSTGRES)
    TESTING = True
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False
    FEME_CONFIG_PATH = '/opt/project/ccme/matchingengine/src/main/resources/quickfix/examples/ordermatch/marketclient.cfg'
    FEMD_CONFIG_PATH = '/opt/project/ccme/marketdata/src/main/resources/quickfix/examples/executor/executor.cfg'



config = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig
}
