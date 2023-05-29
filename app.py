from flask import Flask
from endpoints import post_login
from endpoints import post_register
from endpoints.events import delete_event
from endpoints.events import get_event
from endpoints.users import get_user
from endpoints.users import get_users
from endpoints.events import patch_event

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_world():
    return {
        "message": "Hello world!"
    }, 200

app.register_blueprint(post_login.blueprint)
app.register_blueprint(post_register.blueprint)
app.register_blueprint(delete_event.blueprint)
app.register_blueprint(get_event.blueprint)
app.register_blueprint(get_user.blueprint)
app.register_blueprint(get_users.blueprint)
app.register_blueprint(patch_event.blueprint)
