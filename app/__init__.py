from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()

login_manager.init_app(app)

@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"


@app.route("/register")
def register():
    return "<h1>Registration Page</h1>"


@app.route("/home")
def home():
    return "<h1>Homepage</h1>"
