from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from consts import ENV


class _DatabaseManager:
    def __init__(self):
        self._connection_string = ENV.get("DATABASE_URL")

        if self._connection_string == None:
            raise AttributeError("DATABASE_URL is not defined.")

        self._client = MongoClient(
            self._connection_string, server_api=ServerApi("1"))

        self._database = self._client["Database"]
        self._collection_events = self._database["events"]
        self._collection_users = self._database["users"]

    def create_user(self,
                    name,
                    surname,
                    username,
                    password,
                    tc_identity_no,
                    phone,
                    email,
                    address,
                    is_admin):

        self._collection_users.insert_one({
            "name": name,
            "surname": surname,
            "username": username,
            "password": password,
            "tc_identity_no": tc_identity_no,
            "phone": phone,
            "email": email,
            "address": address,
            "is_admin": is_admin
        })
