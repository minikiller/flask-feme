from flask_restful import Resource
from app.models.setting import Setting,SettingSchema
from flask import request, jsonify, make_response
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.models.database import db
from app.utils import set_config


# http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
# https://github.com/marshmallow-code/marshmallow-jsonapi
schema = SettingSchema()
# schema = TradeSchema(include_data=('owner',))


class SettingListApi(Resource):
    def get(self):
        setting_query = Setting.query.all()

        results = schema.dump(setting_query, many=True)
        return {"settings": results}

    def post(self):
        # now_time = datetime.datetime.now()
        raw_dict = request.get_json(force=True)
        try:
            # Validate Data
            schema.validate(raw_dict)
            setting = Setting()
            setting_dict = raw_dict
            for key, value in setting_dict.items():

                setattr(setting, key, value)

            setting.add(setting)

            # Return the new dog information
            # query = Trade.query.get(trade.id)
            # results = schema.dump(query)
            # return results, 201
            response = jsonify({"code": 1})
            response.status_code = 201
            return response

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp


class SettingApi(Resource):
    def get(self, setting_id):
        '''
        http://jsonapi.org/format/#fetching
        A server MUST respond to a successful request to fetch an individual resource or resource collection with
        a 200 OK response.

        A server MUST respond with 404 Not Found when processing a request to fetch a single resource that does not
        exist, except when the request warrants a 200 OK response with null as the primary data (as described above)
        a self link as part of the top-level links object
        '''
        setting_query = Setting.query.get_or_404(setting_id)
        result = schema.dump(setting_query)
        return result

    def put(self, setting_id):
        '''
        http://jsonapi.org/format/#crud-updating
        The PATCH request MUST include a single resource object as primary data. The resource object MUST contain
        type and id members.

        If a request does not include all of the attributes for a resource, the server MUST interpret the missing
        attributes as if they were included with their current values. The server MUST NOT interpret missing
        attributes as null values.

        If a server accepts an update but also changes the resource(s) in ways other than those specified by the
        request (for example, updating the updated-at attribute or a computed sha), it MUST return a 200 OK
        response. The response document MUST include a representation of the updated resource(s) as if a GET request was made to the request URL.

        A server MUST return 404 Not Found when processing a request to modify a resource that does not exist.
        '''
        setting = Setting.query.get_or_404(setting_id)
        raw_dict = request.get_json(force=True)

        try:
            # schema.validate(raw_dict)
            set_config(setting.application, setting.name, setting.value,raw_dict['value'])
            setting_dict = raw_dict
            for key, value in setting_dict.items():

                setattr(setting, key, value)

            setting.update()
            
            response = jsonify({"code": 1})
            response.status_code = 200
            return response

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 401
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp

    def delete(self, setting_id):
        '''
        http://jsonapi.org/format/#crud-deleting
        A server MUST return a 204 No Content status code if a deletion request is successful and no content is returned.
        '''
        setting = Setting.query.get_or_404(setting_id)
        try:
            delete = setting.delete(setting)
            response = jsonify({"code": 1})
            response.status_code = 200
            return response

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp
