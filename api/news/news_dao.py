from api.news.news_models import News
from api.users.users_model import User

class NewsDAO:
    def __init__(self, session):
        self.session = session

    def get_news(self, page: int, page_size: int = 5):
        offset = (page - 1) * page_size
        return (
            self.session.query(News)
            .filter(News.is_pinned == False)
            .order_by(News.creation_date.desc())
            .offset(offset)
            .limit(page_size + 1)
            .all()
        )

    def get_pinned_news(self, page: int, page_size: int = 5):
        offset = (page - 1) * page_size
        return (
            self.session.query(News)
            .filter(News.is_pinned == True)
            .order_by(News.creation_date.desc())
            .offset(offset)
            .limit(page_size + 1)
            .all()
        )

    def get_news_by_id(self, news_id):
        return (
            self.session.query(
                News.id,
                News.title,
                News.text,
                News.is_pinned,
                News.creation_date,
                User.first_name,
                User.last_name
            )
            .join(User, News.author_id == User.id)
            .filter(News.id == news_id)
            .first()
        )


