from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "0010f95c9bc0cc186611f2058dbae586976723d5e847e668bf1b23141fcb3029"


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


@app.route("/login")
def login():
    return "<h1>Login Page</h1>"