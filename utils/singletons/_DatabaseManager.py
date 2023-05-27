from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
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
                     event_type, 
                     created_by, 
                     participants, 
                     starts_at, 
                     ends_at,
                     remind_at,
                     document_id = None):

        # Convert strings to ObjectId
        for i in range(len(participants)):
            participants[i] = ObjectId(participants[i])
        
        document = {
            "name":name,
            "type":event_type,
            "created_by":ObjectId(created_by),
            "participants": participants,
            "starts_at": datetime.fromtimestamp(starts_at),
            "ends_at": datetime.fromtimestamp(ends_at),
            "remind_at": remind_at
        }

        if document_id != None:
            document["_id"] = ObjectId(document_id)

        result = self._collection_events.insert_one(document)
        inserted_id = result.inserted_id

        if inserted_id == None:
            return None

        return str(inserted_id)
    
    
    def get_event(self, event_id):
        return self._collection_events.find_one({"_id": ObjectId(event_id)})
    
    
    def delete_event(self, event_id):
        result = self._collection_events.find_one_and_delete(
            {"_id": ObjectId(event_id)}
        )

        if result == None:
            return False
        
        return True
    

    def get_user_by_id(self, user_id):
        user_id = ObjectId(user_id)
        found_user = self._collection_users.find_one({"_id": str(user_id)})
        return found_user
    
    def get_all_users(self):
        projection  = {
        "_id": 1,  
        "name": 1,
        "surname": 1,
        "username": 1
        }
        
        users = self._collection_users.find({}, projection )

        user_list = []
        for user in users:
            user["_id"] = str(user["_id"])
            user_list.append(user)

        return user_list

