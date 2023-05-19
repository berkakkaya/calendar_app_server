from flask import request, Blueprint
from utils.singletons import token_manager, database_manager
from utils.exceptions import TokenInvalidException


blueprint = Blueprint("post_login", __name__)


@blueprint.route("/login", methods=["POST"])
def post_login():
    if not request.is_json:
        return {
            "message": "Invalid request"
        }, 400
    
    json_data = request.json

    if not "email" in json_data or not "password" in json_data:
        return {
            "message": "Invalid request"
        },400
    
    user = database_manager.get_user_by_email(json_data["email"])
   
    if user == None:
        return {
            "message": "Email or password is invalid"
        }, 403
    
    if json_data["password"] != user["password"]:
        return {
            "message": "Email or password is invalid"
        }, 403
    
    refresh_token = token_manager.create_refresh_token(str(user["_id"]))
    access_token = token_manager.create_access_token(refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }, 200


@blueprint.route("/token", methods=["POST"])
def post_token():

    authorization = request.headers.get("Authorization")
    
    if authorization == None:
        return {
            "message": "Authorization header is missing"
        }, 400
    
    authorization = authorization.split(" ")
    
    if len(authorization) != 2 or authorization[0] != "Bearer":
        return {
            "message": "Invalid authorization header"
        }, 400
    
    refresh_token = authorization[1]

    try: 
        access_token = token_manager.create_access_token(refresh_token)
 
    except TokenInvalidException:
        return {
            "message": "Invalid token"
        }, 401
    
    return {
        "access_token": access_token
    }, 200
