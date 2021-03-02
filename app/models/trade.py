from .base import Base
from sqlalchemy import Column, DateTime, func, Integer, String, Float
from .database import CRUD
from marshmallow import validate
from marshmallow import Schema, fields

# Create the validation for what we see as "not blank"
NOT_BLANK = validate.Length(min=1, error='Field cannot be blank')
PASSWORD_LENGTH = validate.Length(min=10, error='Password too short')


class Trade(Base, CRUD):
    symbol = Column(String)
    strikePrice = Column(Float)
    lowLimitPrice = Column(Float)
    highLimitPrice = Column(Float)
    tradingReferencePrice = Column(Float)
    securityID = Column(String)
    cfiCode = Column(String)
    activationDate = Column(String)
    lastEligibleTradeDate = Column(String)


class TradeSchema(Schema):

    # Validation for the different fields
    id = fields.Integer(dump_only=True)
    symbol = fields.String(validate=NOT_BLANK)
    strikePrice = fields.Float(dump_only=True)
    lowLimitPrice = fields.Float(dump_only=True)
    highLimitPrice = fields.Float(dump_only=True)
    tradingReferencePrice = fields.Float(dump_only=True)
    securityID = fields.String(dump_only=True)
    cfiCode = fields.String(dump_only=True)
    activationDate = fields.String(dump_only=True)
    lastEligibleTradeDate = fields.String(dump_only=True)

    # owner = fields.Relationship(related_url='/users/{user_id}',
    #                             related_url_kwargs={'user_id': '<owner_id>'},
    #                             many=False,
    #                             include_resource_linkage=True,
    #                             type_='user',
    #                             schema='UserSchema'
    #                             )

    # Self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/trades/"
        else:
            self_link = "/trade/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        type_ = 'trade'
