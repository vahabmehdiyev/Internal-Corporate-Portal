from flask_restx import Resource, Namespace
from config.utils import ip_required

auth_ns = Namespace('auth')

@auth_ns.route('/session/')
class Session(Resource):
    @ip_required
    def get(self):
        return True

