from flask_restx import Resource, Namespace
from config.implemented import docs_service
from config.utils import ip_required

docs_ns = Namespace('docs')


@docs_ns.route('/')
class Documents(Resource):
    @ip_required
    def get(self):
        return docs_service.get_docs()

@docs_ns.route('/search/')
class Search(Resource):
    @ip_required
    def get(self):
        return docs_service.search()

@docs_ns.route('/add/')
class Search(Resource):
    @ip_required
    def post(self):
        return docs_service.upload_file()

@docs_ns.route('/download/<int:doc_id>/')
class Search(Resource):
    @ip_required
    def get(self, doc_id):
        return docs_service.download_file(doc_id)
