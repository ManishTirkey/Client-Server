import json


class ExistIPException(Exception):
    pass


class ExistNameMappingException(Exception):
    pass


class Mapping:
    def __init__(self):
        self.mapping = []
        self.load_mapping()

    def load_mapping(self):
        with open('clients_db.json', 'r') as clients_file:
            self.mapping = json.load(clients_file)

    def get_all_maps(self):
        return self.mapping

    def save(self):
        with open('clients_db.json', 'w') as clients_file:
            json.dump(self.mapping, clients_file)
        self.load_mapping()

    def get_ip_with_name(self, name=None):
        if name:
            for client in self.mapping:
                if client["name"] == name:
                    return client["ip"]

    def get_name_with_ip(self, ip=None):
        if ip:
            for client in self.mapping:
                if client["ip"] == ip:
                    return client["name"]

    def is_exists(self, ip=None, name=None):
        if ip and self.get_name_with_ip(ip):
            return True

        if name and self.get_ip_with_name(name):
            return True

        return False

    def insert(self, client=None):
        if client:

            if self.is_exists(ip=client['ip']):
                raise ExistIPException("IP already exists.")
            if self.is_exists(name=client['name']):
                raise ExistNameMappingException("Name already exists.")

            self.mapping.append(client)
            print("After inserting:")
            print(self.mapping)
            self.save()


mapping = Mapping()