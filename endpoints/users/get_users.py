from flask import request, Blueprint
from utils.singletons import database_manager
from utils.authentication import login_required

blueprint = Blueprint("get_users", __name__)


@blueprint.route("/users", methods=["GET"])
@login_required
def get_users():

    users = database_manager.get_all_users()

    return users, 200

