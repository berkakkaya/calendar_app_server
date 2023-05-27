from flask import request, Blueprint
from utils.singletons import database_manager
from utils.authentication import login_required

blueprint = Blueprint("get_users", __name__)


@blueprint.route("/get_users", methods=["GET"])
@login_required
def get_users():
    if not request.is_json:
        return {
            "message": "Invalid request"
        }, 400

    users = []
    result = []
    users = database_manager.get_all_users()

    for user in users:
        result.append({
	    "_id": str(user["_id"]),
        "name": user["name"],
        "surname": user["surname"],
        "username": user["username"],
        })
    return result, 200

