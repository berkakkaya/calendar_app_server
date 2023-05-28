from flask import request, Blueprint
from utils.singletons import database_manager, token_manager
from utils.authentication import login_required
from utils.exceptions import TokenInvalidException

blueprint = Blueprint("get_events", __name__)


@blueprint.route("/events", methods=["GET"])
@login_required
def get_event(user_id):
    events = database_manager.get_all_events(user_id)
    
    return events, 200
