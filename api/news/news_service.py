from api.news.news_dao import NewsDAO
import json

class NewsService:
    def __init__(self, dao: NewsDAO):
        self.news_dao = dao

    def news_socket(self, ws, page_size=7):
        def serialize(news_list):
            return [{
                "id": n.id,
                "title": n.title,
                "text": n.text[:100],
                "author":  f"{n.author.first_name} {n.author.last_name}",
                "creation_date": str(n.creation_date),
            } for n in news_list]

        def build_news_response(page):
            news_list = self.news_dao.get_news(page, page_size)
            is_end = len(news_list) <= page_size
            if not is_end:
                news_list = news_list[:page_size]

            return {
                "data": {
                    "code": 200,
                    "message": "News Success"
                },
                "response": {
                    "news": {
                        "data": serialize(news_list),
                        "current_page": page,
                        "is_end": is_end
                    }
                }
            }

        def build_pinned_response(page):
            pinned_list = self.news_dao.get_pinned_news(page, page_size)
            is_end = len(pinned_list) <= page_size
            if not is_end:
                pinned_list = pinned_list[:page_size]

            return {
                "data": {
                    "code": 200,
                    "message": "Pinned Success"
                },
                "response": {
                    "pinned": {
                        "data": serialize(pinned_list),
                        "current_page": page,
                        "is_end": is_end
                    }
                }
            }

        ws.send(json.dumps({
            "data": {
                "code": 200,
                "message": "Connected"
            },
            "response": {
                "news": build_news_response(1)["response"]["news"],
                "pinned": build_pinned_response(1)["response"]["pinned"]
            }
        }))

        while True:
            msg = ws.receive()
            if not msg:
                continue

            try:
                data = json.loads(msg)
                type_ = data.get("type")

                if not type_:
                    continue

                try:
                    raw_page = data.get("current_page")
                    page = int(raw_page) if raw_page is not None else 1
                except (ValueError, TypeError):
                    page = 1

                if type_ == "news":
                    ws.send(json.dumps(build_news_response(page)))
                elif type_ == "pinned":
                    ws.send(json.dumps(build_pinned_response(page)))
                else:
                    continue

            except Exception as e:
                ws.send(json.dumps({
                    "data": {
                        "code": 500,
                        "message": f"Error: {str(e)}"
                    }
                }))

    def get_news_by_id(self, news_id):
        news = self.news_dao.get_news_by_id(news_id)
        if not news:
            return None

        return {
            "id": news.id,
            "title": news.title,
            "text": news.text,
            "author": f"{news.first_name} {news.last_name}",
            "is_pinned": news.is_pinned,
            "creation_date": news.creation_date.strftime("%Y-%m-%d %H:%M:%S"),
        }


