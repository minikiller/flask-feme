from flask_restful import Resource
from app.models.trade import Trade, TradeSchema
from flask import request, jsonify, make_response
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.models.database import db


# http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
# https://github.com/marshmallow-code/marshmallow-jsonapi
schema = TradeSchema()
# schema = TradeSchema(include_data=('owner',))


class TradeListApi(Resource):
    def get(self):
        trades_query = Trade.query.all()

        results = schema.dump(trades_query, many=True)
        return results

    def post(self):
        # now_time = datetime.datetime.now()
        raw_dict = request.get_json(force=True)
        try:
            # Validate Data
            schema.validate(raw_dict)
            trade = Trade(raw_dict)

            trade.add(trade)

            # Return the new dog information
            query = Trade.query.get(trade.id)
            results = schema.dump(query)
            return results, 201

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp


class TradeApi(Resource):
    def get(self, trade_id):
        '''
        http://jsonapi.org/format/#fetching
        A server MUST respond to a successful request to fetch an individual resource or resource collection with
        a 200 OK response.

        A server MUST respond with 404 Not Found when processing a request to fetch a single resource that does not
        exist, except when the request warrants a 200 OK response with null as the primary data (as described above)
        a self link as part of the top-level links object
        '''
        trade_query = Trade.query.get_or_404(trade_id)
        result = schema.dump(trade_query)
        return result
    
    def patch(self, trade_id):
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
        trade = Trade.query.get_or_404(trade_id)
        raw_dict = request.get_json(force=True)

        try:
            schema.validate(raw_dict)
            trade_dict = raw_dict['data']['attributes']
            for key, value in trade_dict.items():

                setattr(trade, key, value)

            trade.update()
            return self.get(id)

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 401
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp

    def delete(self, trade_id):
        '''
        http://jsonapi.org/format/#crud-deleting
        A server MUST return a 204 No Content status code if a deletion request is successful and no content is returned.
        '''
        trade = Trade.query.get_or_404(trade_id)
        try:
            delete = trade.delete(trade)
            response = make_response()
            response.status_code = 204
            return response

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 401
            return resp
