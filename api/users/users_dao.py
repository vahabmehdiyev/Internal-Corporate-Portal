from api.users.users_model import User
from api.auth.auth_model import IPAddress


class UsersDAO:
    def __init__(self, session):
        self.session = session

    def get_user_by_ip(self, ip_address):
        return self.session.query(User).join(IPAddress).filter(IPAddress.ip_address == ip_address).first()


