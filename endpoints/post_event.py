from flask import request, Blueprint
from utils.singletons import token_manager, database_manager
from utils.exceptions import TokenInvalidException
from utils.check_attributes import check_attributes


blueprint = Blueprint("post_event", __name__)

@blueprint.route("/event", methods=["POST"])
def post_event():
    if not request.is_json:
        return {
            "message": "Invalid request"
        }, 400
    json_data=request.json

    result=check_attributes(json_data,["event_name", "event_type", "created_by", "participants", "start_at", "ends_at", "remind_at"])

    if result==False:
        return {
            "message": "Invalid request"
        }, 400
    
    event_id = database_manager.post_event(
        event_name=json_data["event_name"],
        event_type=json_data["event_type"],
        created_by=json_data["created_by"],
        participants=json_data["participants"],
        start_at=json_data["start_at"],
        ends_at=json_data["ends_at"],
        remind_at=json_data["remind_at"],
        is_admin=False # gerekli mi?
    )
    
    if event_id == None:
        return {
            "message": "event already exists."
        }, 409
    

    refresh_token=token_manager.create_refresh_token(event_id)
    access_token=token_manager.create_access_token(refresh_token)    

    return{
        "access_token":access_token, 
        "refresh_token": refresh_token
    },200
