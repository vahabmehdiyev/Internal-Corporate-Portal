from api.faq.faq_models import Section, FAQ
from sqlalchemy import or_


class FaqsDAO:
    def __init__(self, session):
        self.session = session

    def get_sections(self):
        sections = self.session.query(Section).all()
        return sections

    def search(self, search_query):
        return (
            self.session.query(FAQ)
            .join(Section)
            .filter(
                or_(
                    Section.name.ilike(f"%{search_query}%"),
                    FAQ.question.ilike(f"%{search_query}%")
                )
            )
        ).all()

