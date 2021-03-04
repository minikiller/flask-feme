import click
from werkzeug.middleware.proxy_fix import ProxyFix
from app.models.base import db
from app.models.database import user_datastore, User
from app.models.trade import Trade
from app.models.setting import Setting
from .factory import Factory
from flask_security.utils import encrypt_password


def create_app(environment='development'):
    f = Factory(environment)
    f.set_flask()
    f.set_db()
    f.set_migration()
    f.set_api()
    f.set_security()

    # from models import Example

    app = f.flask

    if app.config['TESTING']:  # pragma: no cover
        # Setup app for testing
        @app.before_first_request
        def initialize_app():
            pass

    @app.before_first_request
    def bootstrap_app():
        if db.session.query(User).count() == 0:
            create_test_models()
        if db.session.query(Setting).count() == 0:
            create_settings_models()


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE')

        return response

    app.wsgi_app = ProxyFix(app.wsgi_app)

    @app.cli.command()
    @click.argument('command')
    def setup(command):
        pass

    return app

#############################################
########## Bootstrap Several Users
# https://github.com/graup/flask-restless-security/blob/master/server.py
#############################################


def create_trade_models():
    # # Create a couple of dogs and tie them to owners
    trade = Trade()
    trade.symbol = 'FMG3-DEC20'
    trade.strikePrice = 10.00
    trade.lowLimitPrice = 9.00
    trade.highLimitPrice = 20.00
    trade.tradingReferencePrice = 29.00
    trade.securityID = '001'
    trade.cfiCode = '001'
    trade.activationDate = "20210201-22:30:00.00"
    trade.lastEligibleTradeDate = "20210201-22:30:00.00"
    trade.add(trade)
  
    trade = Trade()
    trade.symbol = 'FMG3-MAR21'
    trade.strikePrice = 10.00
    trade.lowLimitPrice = 9.00
    trade.highLimitPrice = 20.00
    trade.tradingReferencePrice = 29.00
    trade.securityID = '002'
    trade.cfiCode = '001'
    trade.activationDate = "20210201-22:30:00.00"
    trade.lastEligibleTradeDate = "20210201-22:30:00.00"
    trade.add(trade)

    trade = Trade()
    trade.symbol = 'FMG3-JUN21'
    trade.strikePrice = 10.00
    trade.lowLimitPrice = 9.00
    trade.highLimitPrice = 20.00
    trade.tradingReferencePrice = 29.00
    trade.securityID = '003'
    trade.cfiCode = '001'
    trade.activationDate = "20210201-22:30:00.00"
    trade.lastEligibleTradeDate = "20210201-22:30:00.00"
    trade.add(trade)

    trade = Trade()
    trade.symbol = 'FMG3-SEP21'
    trade.strikePrice = 10.00
    trade.lowLimitPrice = 9.00
    trade.highLimitPrice = 20.00
    trade.tradingReferencePrice = 29.00
    trade.securityID = '004'
    trade.cfiCode = '003'
    trade.activationDate = "20210201-22:30:00.00"
    trade.lastEligibleTradeDate = "20210201-22:30:00.00"
    trade.add(trade)

    trade = Trade()
    trade.symbol = 'FMG3-DEC20-MAR21'
    trade.strikePrice = 10.00
    trade.lowLimitPrice = 9.00
    trade.highLimitPrice = 20.00
    trade.tradingReferencePrice = 29.00
    trade.securityID = '005'
    trade.cfiCode = '001'
    trade.activationDate = "20210201-22:30:00.00"
    trade.lastEligibleTradeDate = "20210201-22:30:00.00"
    trade.add(trade)

    trade = Trade()
    trade.symbol = 'FMG3-DEC20-JUN21'
    trade.strikePrice = 10.00
    trade.lowLimitPrice = 9.00
    trade.highLimitPrice = 20.00
    trade.tradingReferencePrice = 29.00
    trade.securityID = '006'
    trade.cfiCode = '001'
    trade.activationDate = "20210201-22:30:00.00"
    trade.lastEligibleTradeDate = "20210201-22:30:00.00"
    trade.add(trade)

    trade = Trade()
    trade.symbol = 'FMG3-DEC20-SEP21'
    trade.strikePrice = 10.00
    trade.lowLimitPrice = 9.00
    trade.highLimitPrice = 20.00
    trade.tradingReferencePrice = 29.00
    trade.securityID = '007'
    trade.cfiCode = '001'
    trade.activationDate = "20210201-22:30:00.00"
    trade.lastEligibleTradeDate = "20210201-22:30:00.00"
    trade.add(trade)

    trade = Trade()
    trade.symbol = 'FMG3-MAR21-JUN21'
    trade.strikePrice = 10.00
    trade.lowLimitPrice = 9.00
    trade.highLimitPrice = 20.00
    trade.tradingReferencePrice = 29.00
    trade.securityID = '008'
    trade.cfiCode = '001'
    trade.activationDate = "20210201-22:30:00.00"
    trade.lastEligibleTradeDate = "20210201-22:30:00.00"
    trade.add(trade)

    trade = Trade()
    trade.symbol = 'FMG3-MAR21-SEP21'
    trade.strikePrice = 10.00
    trade.lowLimitPrice = 9.00
    trade.highLimitPrice = 20.00
    trade.tradingReferencePrice = 29.00
    trade.securityID = '009'
    trade.cfiCode = '001'
    trade.activationDate = "20210201-22:30:00.00"
    trade.lastEligibleTradeDate = "20210201-22:30:00.00"
    trade.add(trade)

    trade = Trade()
    trade.symbol = 'FMG3-JUN21-SEP21'
    trade.strikePrice = 10.00
    trade.lowLimitPrice = 9.00
    trade.highLimitPrice = 20.00
    trade.tradingReferencePrice = 29.00
    trade.securityID = '010'
    trade.cfiCode = '001'
    trade.activationDate = "20210201-22:30:00.00"
    trade.lastEligibleTradeDate = "20210201-22:30:00.00"
    trade.add(trade)


def create_settings_models():
    # # Create a couple of dogs and tie them to owners
    setting = Setting()
    setting.name = "InstrumentName"
    setting.value = "FMG3"
    setting.type = "String"
    setting.comment = "Instrument Name, split by ','"
    setting.application = "Market Data"
    setting.add(setting)

    setting = Setting()
    setting.name = "InstrumentDate"
    setting.value = "DEC20,MAR21,JUN21,SEP21"
    setting.comment = "Instrument Date, split by ','"
    setting.type = "String"
    setting.application = "Market Data"
    setting.add(setting)

def create_test_models():
    # Create the default roles
    basic = user_datastore.find_or_create_role(
        name='User', description="Basic user")
    admin = user_datastore.find_or_create_role(
        name='Admin', description='API Administrator')

    # Create the default users
    user_datastore.create_user(email='test1@gmail.com', password=encrypt_password(
        'testing123'), first_name="Test User", last_name="1")
    user_datastore.create_user(email='test2@gmail.com', password=encrypt_password(
        'testing123'), first_name="Test User", last_name="2")
    user_datastore.create_user(email='test3@gmail.com', password=encrypt_password(
        'testing123'), first_name="Test User", last_name="3")

    # Save users
    db.session.commit()

    # Activate users and assign roles
    user1 = user_datastore.find_user(email='test1@gmail.com')
    user2 = user_datastore.find_user(email='test2@gmail.com')
    user3 = user_datastore.find_user(email='test3@gmail.com')

    user_datastore.activate_user(user1)
    user_datastore.activate_user(user2)
    user_datastore.activate_user(user3)

    user_datastore.add_role_to_user(user1, admin)
    user_datastore.add_role_to_user(user2, basic)
    user_datastore.add_role_to_user(user3, basic)

    # Save changes
    db.session.commit()
    create_trade_models()
    # create_settings_models()



