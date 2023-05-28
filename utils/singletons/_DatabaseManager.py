from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from consts import ENV
import datetime

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

        result = self._collection_users.insert_one({
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

        if result.inserted_id != None:
            return str(result.inserted_id)

    def get_user_by_email(self, email):
        found_user = self._collection_users.find_one({"email": email})
        return found_user
    
    
    def get_event_by_id(self, event_id):
        found_event = self._collection_events.find_one({"_id": ObjectId(event_id)})

        if found_event == None:
            return None
    
        found_event["starts_at"] = found_event["starts_at"].timestamp()

        found_event["ends_at"] = found_event["ends_at"].timestamp()

        found_event["_id"] = str(event_id)
        
        participants = found_event["participants"]

        for i in range(participants):
            participants[i] = str(participants[i])
        
        found_event["participants"] = participants
            
        return found_event
    
    def get_all_events(self, user_id):
        events = self._collection_events.find({
        "$or": [
            {
                "participants": ObjectId(user_id)
            },
            {
                "created_by": ObjectId(user_id)
            }
            ]
        }, 
        projection=["name", "type", "starts_at", "ends_at"])
        
        for event in events:
            event["_id"] =  str(event["_id"])

            event["starts_at"] = event["starts_at"].timestamp()

            event["ends_at"] = event["ends_at"].timestamp()

        return events

    def delete_event(self, event_id):
        result = self._collection_events.find_one_and_delete(
            {"_id": ObjectId(event_id)}
        )

        if result == None:
            return False
        
        return True
    