from api.auth.auth_model import IPAddress
from api.users.users_model import User

class DevDAO:
    def __init__(self, session):
        self.session = session

    def get_ip_id_by_address(self, ip_address):
        ip_entry = self.session.query(IPAddress.id).filter_by(ip_address=ip_address).first()
        return ip_entry.id if ip_entry else None

    def add_ip_and_get_id(self, ip_address):
        existing_ip_id = self.get_ip_id_by_address(ip_address)
        if existing_ip_id:
            return existing_ip_id


        new_ip = IPAddress(ip_address=ip_address)
        self.session.add(new_ip)
        self.session.commit()
        return new_ip.id

    def update_default_user_ip(self, ip_id):
        if ip_id is None:
            return

        default_user = self.session.query(User).filter_by(id=10).first()  # Default user ID = 10
        if default_user:
            default_user.ip_address = ip_id
            self.session.commit()

    def update_user_ip_to_default(self, ip_id):
        if ip_id is None:
            return

        self.session.query(User).filter_by(ip_address=ip_id).update({"ip_address": 37})
        self.session.commit()

    def delete_ip(self, ip_id):
        if ip_id is None:
            return

        existing_ip = self.session.query(IPAddress).filter_by(id=ip_id).first()
        if existing_ip:
            self.session.delete(existing_ip)
            self.session.commit()