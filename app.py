from flask import Flask
from endpoints import post_login


app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_world():
    return {
        "message": "Hello world!"
    }, 200

app.register_blueprint(post_login.blueprint)
