from api.users.users_model import Subsidiary, User, Office
from sqlalchemy import or_, func, and_


class PhonesDAO:
    def __init__(self, session):
        self.session = session

    def get_subsidiaries(self):
        return self.session.query(Subsidiary).all()

    def get_users_by_slug(self, slug):
        return (
            self.session.query(User)
            .join(Subsidiary, User.subsidiary_id == Subsidiary.id)
            .filter(Subsidiary.slug == slug)
            .all()
        )

    def search_users(self, search_text):
        search_terms = search_text.split()
        filters = []

        for term in search_terms:
            filters.append(
                or_(
                    func.concat(User.last_name, ' ', User.first_name, ' ', func.coalesce(User.patronymic, '')).ilike(
                        f"%{term}%"),
                    Subsidiary.name.ilike(f"%{term}%"),
                    Office.name.ilike(f"%{term}%"),
                    User.position.ilike(f"%{term}%"),
                )
            )

        return (
            self.session.query(User, Subsidiary, Office)
            .join(Subsidiary, User.subsidiary_id == Subsidiary.id)
            .join(Office, User.office_id == Office.id)
            .filter(and_(*filters))
            .all()
        )

