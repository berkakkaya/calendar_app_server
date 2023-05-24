from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from consts import ENV
from datetime import datetime



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
    
    def create_event(self,  
                   name, 
                   type, 
                   created_by, 
                   participants, 
                   starts_at, 
                   ends_at, 
                   remind_at):
        result = self._collection_events.inserted_id({ #buradan emin değilim-It's better if we return the created document's ID. The insert_one function returns a InsertOneResult object, and it has a inserted_id property. If the operation has failed, this property will be None. We can simply return that property in this function. A detailed documentation can be found here.
            "name":name,
            "type":type,
            "created_by":ObjectId(created_by),
            "participants": participants,
            "starts_at": datetime.fromtimestamp(starts_at),
            "ends_at": datetime.fromtimestamp(ends_at),
            "remind_at": remind_at
        })
  

        
