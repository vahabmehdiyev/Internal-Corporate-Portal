from api.auth.auth_model import IPAddress
from api.docs.docs_models import Documents
from sqlalchemy import or_, desc
from api.users.users_model import User


class DocsDAO:
    def __init__(self, session):
        self.session = session

    def get_docs(self, ordering: str = None):
        query = self.session.query(Documents).join(User, Documents.author_id == User.id)

        valid_columns = {
            "id": Documents.id,
            "name": Documents.name,
            "creation_date": Documents.creation_date,
            "description": Documents.description,
            "author": User.first_name  # Сортировка по имени автора
        }

        if ordering:
            column_name = ordering.lstrip("-")  # Убираем "-" (если есть)
            order_column = valid_columns.get(column_name)

            if order_column is not None:
                query = query.order_by(desc(order_column) if ordering.startswith("-") else order_column)

        return query.all()

    def search(self, search_query):
        return (
            self.session.query(Documents)
            .join(User, Documents.author_id == User.id)
            .filter(
                or_(
                    User.first_name.ilike(f"%{search_query}%"),
                    User.last_name.ilike(f"%{search_query}%"),
                    User.patronymic.ilike(f"%{search_query}%"),
                    Documents.name.ilike(f"%{search_query}%"),
                    Documents.description.ilike(f"%{search_query}%")
                )
            )
        ).all()

    def upload_file(self, filename, author_id, file_path):
        new_doc = Documents(name=filename, author_id=author_id, path=file_path)
        self.session.add(new_doc)
        self.session.commit()

    def get_file(self, doc_id):
        return (
            self.session.query(Documents)
            .filter(Documents.id == doc_id)
            .first())

    def get_ip(self, ip_address):
        return (
            self.session.query(IPAddress)
            .filter(IPAddress.ip_address == ip_address)
            .first()
        )
