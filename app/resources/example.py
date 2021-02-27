from flask_restplus import Namespace, Resource, fields
from app.utils  import requires_auth

ns = Namespace('example', description='Examples')

success_model = ns.model('Success', {
    'message': fields.String
})


@ns.route('', endpoint='index')
class IndexPage(Resource):
    @requires_auth
    @ns.marshal_with(success_model)
    def get(self):
        """
        Example url
        """
        return {'message': 'Success'}
