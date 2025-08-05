"""
Simple test API to check if Swagger works
"""

from flask_restx import Namespace, Resource, fields

# Create API namespace
api = Namespace('test', description='Simple test operations')

# Simple test model
test_model = api.model('Test', {
    'message': fields.String(required=True, description='Test message'),
    'status': fields.String(description='Status')
})

@api.route('/hello')
class HelloWorld(Resource):
    @api.doc('hello_world')
    @api.marshal_with(test_model)
    def get(self):
        """Simple hello world endpoint"""
        return {
            'message': 'Hello World from REST API!',
            'status': 'success'
        }