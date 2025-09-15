from api.faq.faq_dao import FaqsDAO
from flask import request


class FaqsService:
    def __init__(self, session):
        self.faqs_dao = FaqsDAO(session)

    def get_sections(self):
        sections = self.faqs_dao.get_sections()

        response = [
            {
                "title": section.name,
                "description": section.description,
                "questions": [
                    {
                        "question": faq.question,
                        "answer": faq.answer
                    }
                    for faq in section.faqs
                ]
            }
            for section in sections
        ]

        return response

    def search(self):
        args = request.args
        search_query = args.get('search')

        faqs = self.faqs_dao.search(search_query)

        response = [
            {
                "question":faq.question,
                "answer": faq.answer
            }
            for faq in faqs
        ]

        return response

