from flask import request, Blueprint
from utils.singletons import database_manager
from utils.authentication import login_required

blueprint = Blueprint("get_user", __name__)


@blueprint.route("/user", methods=["GET"])
@login_required
def get_user(user_id):
    if not request.is_json:
        return {
            "message": "The request body isn't in JSON format."
        }, 400
    
    json_data = request.json
    
    # If "user_id" parameter is supplied
    if json_data != None and "user_id" in json_data:
        _id = json_data["user_id"]

        return _get_data(user_id=_id)
    
    # If not, return the user data of requester
    return _get_data(user_id=user_id)


def _get_data(user_id):
    user = database_manager.get_user_by_id(user_id)

    if user == None:
        return {
            "message": "User does not exist"
        }, 404

    return user, 200
