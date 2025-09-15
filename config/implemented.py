from api.docs.docs_service import DocsService
from api.news.news_dao import NewsDAO
from api.phones.phones_dao import PhonesDAO
from api.phones.phones_service import PhonesService
from api.users.users_dao import UsersDAO
from api.users.users_service import UserService
from api.news.news_service import NewsService
from api.dev.dev_dao import DevDAO
from api.dev.dev_service import DevService
from api.faq.faq_service import FaqsService
from config.database import db

users_service = UserService(UsersDAO(db.session))
devs_service = DevService(DevDAO(db.session))
phones_service = PhonesService(PhonesDAO(db.session))
docs_service = DocsService(db.session)
faqs_service = FaqsService(db.session)

news_dao = NewsDAO(db.session)
news_service = NewsService(dao=news_dao)







