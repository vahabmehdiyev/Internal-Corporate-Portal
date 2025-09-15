from api.users.users_dao import UsersDAO


class UserService:
    def __init__(self, dao: UsersDAO):
        self.users_dao = dao

    def get_current_user(self, ip_address):
        user = self.users_dao.get_user_by_ip(ip_address)

        if not user:
            return None

        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "patronymic": user.patronymic,
            "email": user.email,
            "phone": user.phone,
            "access": [access.slug for access in user.accesses],
            "registration_date": user.registration_date.strftime("%Y-%m-%d %H:%M:%S"),
        }

