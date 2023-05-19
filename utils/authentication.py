from flask import request
from functools import wraps
from utils.singletons import token_manager
from utils.exceptions import TokenInvalidException


def login_required(f):

    @wraps(f)
    def controller_function(*args, **kwargs):

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
        
        access_token = authorization[1]
        
        try:
            result = token_manager.decode_access_token(access_token)

        except TokenInvalidException:
            return {
                "message": "Invalid token"
            }, 401
        
        user_id = result["user_id"]

        # All checks have been passed, continue operating normally
        return f(*args, **kwargs, user_id = user_id)
    
    return controller_function
