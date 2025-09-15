from flask_restx import Resource, Namespace
from config.implemented import users_service
from config.utils import ip_required
from flask import request

users_ns =  Namespace('user')

@users_ns.route('/current/')
class CurrentUser(Resource):
    @ip_required
    def get(self):
        user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        if user_ip.startswith("::ffff:"):
            user_ip = user_ip.replace("::ffff:", "")

        result = users_service.get_current_user(user_ip)

        return result





