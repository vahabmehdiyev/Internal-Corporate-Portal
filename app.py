from flask import Flask
from api.docs.docs_view import docs_ns
from api.phones.phones_view import phones_ns
from config.database import db
from flask_migrate import Migrate
from config.config import Config
from flask_restx import Api
from flask_sock import Sock
from api.socket.socket import websocket, websocket_graph

# Namespaces (REST API endpoints)
from api.auth.auth_view import auth_ns
from api.users.users_view import users_ns
from api.news.news_view import news_ns
from api.dev.dev_view import dev_ns
from api.faq.faq_view import faq_ns
from api.graphs_reports.graphs_reports_view import graph_reports_ns

# Creating the Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Creating the Sock object for WebSocket
sock = Sock(app)
websocket(sock)
websocket_graph(sock)

# SQLAlchemy & Migrate configuration
db.init_app(app)
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)

# Adding API Namespaces
api = Api(app)
api.add_namespace(auth_ns, "/api/auth")
api.add_namespace(users_ns, "/api/users")
api.add_namespace(news_ns, "/api/news")
api.add_namespace(dev_ns, "/api/dev")
api.add_namespace(phones_ns, "/api/phones")
api.add_namespace(docs_ns, "/api/docs")
api.add_namespace(faq_ns, "/api/faq")
api.add_namespace(graph_reports_ns, "/api/graph_reports")


if __name__ == '__main__':
    app.run(host='192.168.68.159', port=5000, debug=True)

