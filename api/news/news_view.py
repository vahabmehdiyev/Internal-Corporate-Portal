from flask_restx import Resource, Namespace
from config.implemented import news_service
from config.utils import ip_required
news_ns = Namespace('news')

@news_ns.route('/<int:news_id>/')
class News(Resource):
    @ip_required
    def get(self, news_id):

        result = news_service.get_news_by_id(news_id)
        return result