from flask import request, Blueprint
from utils.singletons import database_manager
from utils.authentication import login_required

blueprint = Blueprint("get_user", __name__)


@blueprint.route("/get_user", methods=["GET"])
@login_required
def get_user(user_id):
    if not request.is_json:
        return {
            "message": "Invalid request"
        }, 400

    json_data = request.json

    if not "user_id" in json_data:
        return {
            "message": "Invalid request"
        },400
    
    _id = json_data["user_id"]

    user = database_manager.get_user_by_id(_id)

    if user == None:
            return {
            "message": "user does not exist"
        }, 404
    

    return {
	    "_id": _id,
        "name": user["name"],
        "surname": user["surname"],
        "username": user["username"],
    }, 200
