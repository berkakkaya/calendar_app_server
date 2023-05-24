from flask import Flask
from endpoints import post_login
from endpoints import post_register
from endpoints.events import delete_event

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_world():
    return {
        "message": "Hello world!"
    }, 200

app.register_blueprint(post_login.blueprint)
app.register_blueprint(post_register.blueprint)
app.register_blueprint(delete_event.blueprint)
