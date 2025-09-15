from api.dev.dev_dao import DevDAO

class DevService:
    def __init__(self, dao: DevDAO):
        self.dao = dao

    def check_ip_add(self, ip_address):
        existing_ip_id = self.dao.get_ip_id_by_address(ip_address)
        if existing_ip_id:
            return 409

        new_ip_id = self.dao.add_ip_and_get_id(ip_address)

        if new_ip_id is not None:
            self.dao.update_default_user_ip(new_ip_id)
            return 200  # OK

        return 500

    def check_ip_delete(self, ip_address):
        # IP-nin ID-sini tap
        ip_id = self.dao.get_ip_id_by_address(ip_address)

        if ip_id is None:
            return 404

        # self.dao.update_user_ip_to_default(ip_id)
        self.dao.delete_ip(ip_id)

        return 200

