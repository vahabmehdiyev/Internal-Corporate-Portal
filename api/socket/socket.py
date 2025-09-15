from config.implemented import news_service
from api.graphs_reports.graphs_reports_service import  get_dashboard_data
from config.utils import ip_required
import json

def websocket(sock):
    @sock.route("/socket/news/")
    @ip_required
    def get_news(ws):
        news_service.news_socket(ws)


def websocket_graph(sock):
    @sock.route("/socket/graph_reports/")
    #@ip_required
    def get_graph_reports(ws):
        while True:
            message = ws.receive()
            if message is None:
                break

            try:
                data = json.loads(message)
                response = get_dashboard_data(data)
                ws.send(json.dumps(response))
            except Exception as e:
                ws.send(json.dumps({
                    "data": {
                        "code": 500,
                        "message": f"Xəta: {str(e)}"
                    },
                    "response": {}
                }))
