from .example import ns as example_ns
from ..utils import PatchedApi
from flask_restful import Api
from flask import Blueprint
from .trade_views import TradeListApi,TradeApi
# api = PatchedApi()

# api.add_namespace(example_ns)

def initialize_trades(api):
    api.add_resource(TradeListApi, '/trades')
    api.add_resource(TradeApi, '/trade/<trade_id>')
