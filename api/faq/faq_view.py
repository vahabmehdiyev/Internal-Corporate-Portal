from flask_restx import Resource, Namespace
from config.implemented import faqs_service
from config.utils import ip_required

faq_ns = Namespace('api/faq')


@faq_ns.route('/')
class Faq(Resource):
    @ip_required
    def get(self):
        return faqs_service.get_sections()

@faq_ns.route('/search/')
class FaqSearch(Resource):
    @ip_required
    def get(self):
        return faqs_service.search()

