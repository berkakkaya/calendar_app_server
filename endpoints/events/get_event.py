from flask import request, Blueprint
from utils.singletons import database_manager
from utils.authentication import login_required

blueprint = Blueprint("get_event", __name__)


@blueprint.route("/event", methods=["GET"])
@login_required
def get_event(user_id):
    if not request.is_json:
        return {
            "message": "Invalid request"
        }, 400

    json_data = request.json

    if not "event_id" in json_data:
        return {
            "message": "Invalid request"
        },400

    event = database_manager.get_event_by_id(json_data["event_id"])

    if event == None:
        return {
            "message": "Event does not exist"
        }, 404
    
    return event, 200
