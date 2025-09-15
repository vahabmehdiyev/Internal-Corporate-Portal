from api.phones.phones_dao import PhonesDAO
from config.utils import pagination


class PhonesService:
    def __init__(self, dao: PhonesDAO):
        self.dao = dao

    def get_subsidiaries(self):
        subsidiaries = self.dao.get_subsidiaries()

        return [
            {
                "id": str(sub.id),
                "slug": sub.slug,
                "name": sub.name,
                "address": sub.address,
                "phone": sub.phone,
            }
            for sub in subsidiaries
        ]

    def get_users_by_slug(self, slug, current_page):
        users = self.dao.get_users_by_slug(slug)
        paginated_data = pagination(users, current_page, per_page=15)

        data = [
            {
                "id": user.id,
                "contact": f"{user.last_name} {user.first_name} {user.patronymic or ''}".strip(),
                "email": user.email,
                "phone": user.phone,
                "office": user.office_id,
                "personal_phone": user.personal_phone,
                "position": user.position,
            }
            for user in paginated_data["response"]
        ]

        return {
            "data": data,
            "is_end": paginated_data["is_end"],
            "current_page": paginated_data["current_page"],
        }

    def search_users(self, search_text):
        users = self.dao.search_users(search_text)

        if not users:
            return []

        grouped_data = {}
        for user, subsidiary, office in users:
            key = (subsidiary.address, subsidiary.phone)
            if key not in grouped_data:
                grouped_data[key] = {
                    "address": subsidiary.address,
                    "phone": subsidiary.phone,
                    "table": []
                }

            grouped_data[key]["table"].append({
                "id": user.id,
                "contact": f"{user.last_name} {user.first_name} {user.patronymic or ''}".strip(),
                "email": user.email,
                "phone": user.phone,
                "office": office.name,
                "personal_phone": user.personal_phone,
                "position": user.position,
            })

        return list(grouped_data.values())