from flask import request, Blueprint
from utils.check_attributes import check_attributes
from utils.singletons import database_manager
from utils.authentication import login_required

blueprint = Blueprint("patch_event", __name__)


@blueprint.route("/event", methods=["PATCH"])
@login_required
def patch_event(user_id):
    if not request.is_json:
        return {
            "message": "Invalid request"
        }, 400

    json_data = request.json
    
    passed = check_attributes(json_data, [
        "_id",
        "name",
        "type",
        "created_by",
        "participants",
        "starts_at",
        "ends_at",
        "remind_at"
    ])

    if passed == False:
        return {
            "message": "Invalid request"
        }, 400
        
    event = database_manager.get_event_by_id(json_data["_id"])

    if event == None:
        return {
            "message": "The specified event does not exist"
        }, 404
    
    if user_id != event["created_by"]:
        return {
            "message": "User does not own this event"
        },406

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
            "message": "The requested document could not be found"
        }, 404
