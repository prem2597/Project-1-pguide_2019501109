from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

data = []

@app.route("/register")
def register():
    return render_template("Registration.html")

@app.route("/hello", methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return "Please register into the web site"
    else :
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
        name = first_name + " " + last_name
        dob = request.form.get("date-of-birth")
        gender = request.form.get("gender")
        email = request.form.get("email")
        phone = request.form.get("Phone-number")
        details = name +"\n"+ dob +"\n"+ gender +"\n"+ email + "\n" + phone
        print(details)
        return render_template("hello.html", name = details)