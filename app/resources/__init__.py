from .example import ns as example_ns
from ..utils import PatchedApi
from flask_restful import Api
from flask import Blueprint
from .trade_views import TradeListApi, TradeApi
from .user import UserList, UserUpdate
from .role import RoleList, RoleUpdate
from .service import ListService, MDStartService, MDStopService, MEStartService, MEStopService
# api = PatchedApi()

# api.add_namespace(example_ns)


def initialize_trades(api):
    api.add_resource(TradeListApi, '/trades')
    api.add_resource(TradeApi, '/trade/<trade_id>')


def initialize_users(api):
    # Users
    api.add_resource(UserList, '/users')
    api.add_resource(UserUpdate, '/user/<int:id>')


def initialize_roles(api):
    # Roles
    api.add_resource(RoleList, '/roles')
    api.add_resource(RoleUpdate, '/role/<int:id>')


def initialize_service(api):
    # service
    api.add_resource(ListService, '/ListService')
    api.add_resource(MDStartService, '/MDStartService')
    api.add_resource(MDStopService, '/MDStopService')
    api.add_resource(MEStartService, '/MEStartService')
    api.add_resource(MEStopService, '/MEStopService')

def initialize_api(api):
    initialize_users(api)
    initialize_roles(api)
    initialize_trades(api)
    initialize_service(api)
