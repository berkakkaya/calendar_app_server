from flask import request, Blueprint
from utils.singletons import database_manager
from utils.authentication import login_required

blueprint = Blueprint("patch_event", __name__)


@blueprint.route("/event", methods=["PATCH"])
@login_required
def patch_event(**event):
    if not request.is_json:
        return {
            "message": "Invalid request"
        }, 400

    json_data = request.json

    if not "_id" in event:
        return {
            "message": "Invalid request"
        },400
    
    if json_data["user_id"] != event["created_by"]:
        return {
            "message": "User does not own this event"
        },406

    if event == None:
        return {
            "message": ": The specified event does not exist"
        }, 404
    
    is_event_patched = database_manager.patch_event({
                        "_id": event["_id"],
                        "name": event["name"],
                        "type": event["type"],
                        "created_by": event["created_by"],
                        "participants": event["participants"],
                        "starts_at": event["starts_at"],
                        "ends_at": event["ends_at"],
                        "remind_at": event["remind_at"]
                    })
    
    if is_event_patched == True:
        return {
            "message": "The request has been completed successfully"
        }, 200
    else:
        return {
            "message": "Invalid request"
        }, 400

