from .base import Base
from sqlalchemy import Column, DateTime, func, Integer, String, Float
from .database import CRUD
from marshmallow import validate
from marshmallow import Schema, fields

# 用于配置文件的管理
# Create the validation for what we see as "not blank"
NOT_BLANK = validate.Length(min=1, error='Field cannot be blank')
PASSWORD_LENGTH = validate.Length(min=10, error='Password too short')


class Setting(Base, CRUD):
    name = Column(String) # 配置名称
    value = Column(String) # 配置数值
    type = Column(String)  # 配置类型 字符型，整数型
    comment = Column(String)  # 配置说明
    application = Column(String) # 所属应用MarketData or Matching Engine

class SettingSchema(Schema):

    # Validation for the different fields
    id = fields.Integer(dump_only=True)
    name = fields.String(validate=NOT_BLANK)
    value = fields.String(dump_only=True)
    type = fields.String(dump_only=True)
    comment = fields.String(dump_only=True)
    application = fields.String(dump_only=True)

    # Self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/settings/"
        else:
            self_link = "/setting/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        type_ = 'setting'
