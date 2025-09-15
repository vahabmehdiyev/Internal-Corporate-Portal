from flask_restx import Resource, Namespace
from flask import request
from config.implemented import devs_service

dev_ns = Namespace("dev")


@dev_ns.route('/add/')
class AddIP(Resource):
    def head(self):
        ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
        if ip_address.startswith("::ffff:"):
            ip_address = ip_address.replace("::ffff:", "")
        if not ip_address:
            return "", 400

        status_code = devs_service.check_ip_add(ip_address)
        return "", status_code


@dev_ns.route('/delete/')
class DeleteIP(Resource):
    def head(self):
        ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
        if ip_address.startswith("::ffff:"):
            ip_address = ip_address.replace("::ffff:", "")
        if not ip_address:
            return "", 400

        status_code = devs_service.check_ip_delete(ip_address)
        return "", status_code
