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

    result=check_attributes(json_data,["name", "type", "participants", "start_at", "ends_at", "remind_at"])

    if result==False:
        return {
            "message": "Invalid request"
        }, 400
    #Burada ne yapmam gerektiğini tam anlayamadım
    #The same rule will also apply here. The parameter names aren't the wrong thing here, but we obtain those data from our JSON in different names. 
    # We just need to fix these key strings in json_data according to the thing I said in the upper comment, and we're done. :)
    insert_result = database_manager.post_event(
        name=json_data["name"],
        type=json_data["type"],
        created_by=json_data["created_by"],
        participants=json_data["participants"],
        start_at=json_data["start_at"],
        ends_at=json_data["ends_at"],
        remind_at=json_data["remind_at"],
        is_admin=False # gerekli mi?
    )
    
    if insert_result == False:
        return {
            "message": "event already exists."
        }, 409
    