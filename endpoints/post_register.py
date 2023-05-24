from flask import request, Blueprint
from utils.singletons import token_manager, database_manager
from utils.exceptions import TokenInvalidException
from utils.check_attributes import check_attributes


blueprint= Blueprint("post_register", __name__)

@blueprint.route("/register", methods=["POST"] )
def register():
    if not request.is_json:
        return {
            "message": "Invalid request"
        }, 400
    json_data=request.json

    result=check_attributes(json_data,["name", "surname", "email", "username", "password", "tc_identity_number", "phone", "address"])

    if result==False:
        return {
            "message": "Invalid request"
        }, 400
    
    user_id = database_manager.create_user(
        name=json_data["name"],
        surname=json_data["surname"],
        username=json_data["username"],
        password=json_data["password"],
        tc_identity_no=["tc_identity_no"],
        phone=json_data["phone"],
        email=json_data["email"],
        address=json_data["address"],
        is_admin=False
    )

    if user_id == None:
        return {
            "message": "A person with a same email and/or username exists."
        }, 409
    

    refresh_token=token_manager.create_refresh_token(user_id)
    access_token=token_manager.create_access_token(refresh_token)

    return{
        "access_token":access_token, 
        "refresh_token": refresh_token
    },200
    
