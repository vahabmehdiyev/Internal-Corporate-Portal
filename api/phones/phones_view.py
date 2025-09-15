from flask_restx import Resource, Namespace
from config.implemented import phones_service
from config.utils import ip_required
from flask import request

phones_ns = Namespace('phones')


@phones_ns.route('/subsidiaries/')
class Subsidiaries(Resource):
    @ip_required
    def get(self):
        result = phones_service.get_subsidiaries()
        return result

@phones_ns.route('/<string:slug>/')
class UsersBySlug(Resource):
    @ip_required
    def get(self, slug):
        current_page = request.args.get('current_page', 1, type=int)
        result = phones_service.get_users_by_slug(slug, current_page)
        return result

@phones_ns.route('/search/')
class Search(Resource):
    @ip_required
    def get(self):
        search_text = request.args.get('search', '')
        result = phones_service.search_users(search_text)
        return result