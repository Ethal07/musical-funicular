import sqlite3
from flask import *
from flask_login import *
from werkzeug.security import generate_password_hash, check_password_hash

# Establish connection to database
con = sqlite3.connect("database.db")

cur = con.cursor()

# Fetch list of all tables
listOfTables = cur.execute(
    """SELECT * FROM sqlite_master WHERE type='table';"""
).fetchall()

# Create tables
if "users" in listOfTables:  # Create table only if it does not exist
    cur.execute(
        """
    CREATE TABLE users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, username varchar UNIQUE NOT NULL, password_hash varchar NOT NULL);
    """
    )

if "readings" in listOfTables:
    cur.execute(
        """
    CREATE TABLE readings(reading_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id int, timestamp varchar NOT NULL, reading varchar NOT NULL, FOREIGN KEY (user_id) REFERENCES users(user_id));
    """
    )

# commit changes
con.commit()

# terminate connection
con.close()

# Create instance of Flask class
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    error = None

    con = sqlite3.connect("database.db")

    cur = con.cursor()

    usernames = cur.execute("""SELECT username FROM users""").fetchall()

    print(usernames)

    print("here1")
    if request.method == "POST":
        givenUsername = request.form["loginUsernameInput1"]
        givenPassword = request.form["loginPasswordInput1"]

        print(givenUsername, givenPassword, (givenUsername in usernames))

        print("here2")

        for i in usernames:
            if givenUsername in i:
                print("here3")
                if generate_password_hash(
                    givenPassword, method="pbkdf2:sha256"
                ) == cur.execute(
                    """SELECT password_hash FROM users WHERE username = (?);""",
                    givenUsername,
                ):
                    print("here4")
                    con.close()
                    return redirect(url_for("dashboard"))
    con.close()
    return render_template("login.html", error="Wrong username or password!")


@app.route("/register", methods=["POST", "GET"])
def register():

    if request.method == "POST":

        con = sqlite3.connect("database.db")

        cur = con.cursor()

        usernames = cur.execute("""SELECT username FROM users""").fetchall()

        username = request.form["registrationUsernameInput1"]
        password = request.form["registrationPasswordInput1"]

        for i in usernames:
            if username in i:
                return render_template(
                    "registration.html", error="Username already taken!"
                )

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        cur.execute(
            """INSERT INTO users(username, password_hash) VALUES (?, ?);""",
            (username, hashed_password),
        )

        con.commit()
        con.close()

        return redirect(url_for("login"))
    return render_template("registration.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


app.run(debug=True)
