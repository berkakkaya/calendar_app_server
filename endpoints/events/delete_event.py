from flask import request, Blueprint
from utils.singletons import database_manager
from utils.authentication import login_required

blueprint = Blueprint("delete_event", __name__)


@blueprint.route("/event", methods=["DELETE"])
@login_required
def delete_event(user_id):
    if not request.is_json:
        return {
            "message": "Invalid request"
        }, 400

    json_data = request.json

    if not "event_id" in json_data:
        return {
            "message": "Invalid request"
        },400
    
    event_id = json_data["event_id"]

    event = database_manager.get_event(event_id)

    if event == None:
        return {
            "message": "Event does not exist"
        }, 404
    
    if str(event["created_by"]) != user_id:
        return {
            "message": "User does not own this event"
        }, 406
    
    result = database_manager.delete_event(event_id)

    return {
        "message": "The event has been deleted successfully"
    }, 200
