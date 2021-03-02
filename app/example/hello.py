
import datetime
from marshmallow import Schema, fields, ValidationError, pre_load
class UserSchema(Schema):
    name = fields.Str()
    age = fields.Int()
    password = fields.Str()
    created = fields.DateTime()

    class Meta:
        load_only = ['password']
        datetimeformat = '%Y-%m-%dT%H:%M:%SZ'


data = dict(name='tom', age=40, password='123',
            created=datetime.datetime.now())
# {'name': 'tom',
#  'age': 40,
#  'password': '123',
#  'created': datetime.datetime(2019, 10, 18, 9, 36, 36, 263384)}

schema = UserSchema()


dump = schema.dump(data)
print(dump)
