from flask import request, Blueprint
from utils.singletons import database_manager
from utils.check_attributes import check_attributes
from utils.authentication import login_required


blueprint = Blueprint("post_event", __name__)


@blueprint.route("/event", methods=["POST"])
@login_required
def post_event(user_id):
    if not request.is_json:
        return {
            "message": "Invalid request"
        }, 400
    
    json_data = request.json

    result = check_attributes(json_data, ["name", "type", "participants", "starts_at", "ends_at", "remind_at"])

    if result == False:
        return {
            "message": "Invalid request"
        }, 400
    
    inserted_id = database_manager.create_event(
        name=json_data["name"],
        event_type=json_data["type"],
        created_by=user_id,
        participants=json_data["participants"],
        starts_at=json_data["starts_at"],
        ends_at=json_data["ends_at"],
        remind_at=json_data["remind_at"]
    )
    
    if inserted_id == False:
        return {
            "message": "An issue happened while creating a new event."
        }, 500
    
    # Convert strings to ObjectId
    for i in range(len(json_data["participants"])):
        json_data["participants"][i] = str(json_data["participants"][i])
    
    return {
	    "_id": inserted_id,
        "name": json_data["name"],
        "type": json_data["type"],
        "created_by": user_id,
        "participants": json_data["participants"],
        "starts_at": json_data["starts_at"],
        "ends_at": json_data["ends_at"],
        "remind_at": json_data["remind_at"]
    }, 200
    
