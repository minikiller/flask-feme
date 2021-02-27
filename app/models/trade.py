from .base import Base
from sqlalchemy import Column, DateTime, func, Integer, String
from .database import CRUD
from marshmallow import validate
from marshmallow_jsonapi import Schema, fields

# Create the validation for what we see as "not blank"
NOT_BLANK = validate.Length(min=1, error='Field cannot be blank')
PASSWORD_LENGTH = validate.Length(min=10, error='Password too short')


class Trade(Base, CRUD):
    name = Column(String)
    symbol = Column(String)
    roster_id = Column(Integer)  # roster id


class TradeSchema(Schema):

    # Validation for the different fields
    id = fields.Integer(dump_only=True)
    symbol = fields.String(validate=NOT_BLANK)
    created_at = fields.DateTime(dump_only=True)
    roster_id = fields.String(dump_only=True)  # roster id

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
