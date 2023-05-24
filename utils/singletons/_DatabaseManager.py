from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
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

    def get_user_by_email(self, email):
        found_user = self._collection_users.find_one({"email": email})
        return found_user
    
    def get_event(self, event_id):
        return self._collection_events.find_one({"_id": ObjectId(event_id)})
        
    def delete_event(self, user_id, event_id):
        result = self._collection_events.find_one_and_delete(
            {"_id": ObjectId(event_id)}
        )

        if result == None:
            return False
        
        return True
    