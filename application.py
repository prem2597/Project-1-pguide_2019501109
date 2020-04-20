import os
from datetime import datetime

from flask import Flask, render_template, request, session , url_for, redirect
from flask_session import Session
# from sqlalchemy.exc import SQLAlchemyError
from models import *

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATION "] = False
Session(app)
db.init_app(app)

@app.route("/")
def coverpage():
    return render_template("welcome.html")

@app.route("/register")
def register():
    return render_template("Registration.html")

@app.route("/hello", methods=["GET", "POST"])
def hello():
    db.create_all()
    if request.method == "GET":
        return "Please register into the web site"
    else :
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
        full_name = first_name + " " + last_name
        birth = request.form.get("date-of-birth")
        gen = request.form.get("gender")
        mail = request.form.get("email")
        ph = request.form.get("Phone-number")
        pswd = request.form.get("password")
        # details = full_name +"\n"+ birth +"\n"+ gen +"\n"+ mail + "\n" + ph
        user1 = Users(name=full_name, dob=birth, gender=gen, email=mail, phone=ph, password=pswd, timestamp=datetime.now())
        try :
            db.session.add(user1)
            db.session.commit()
            details = "Data Base is successfully updated"
        except:
            details = "Invalid Credentials"
        return render_template("hello.html", name = details)

@app.route("/admin")
def admin():
    users_data = Users.query.order_by(Users.timestamp).all()
    return render_template("admin.html", name = users_data)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/auth", methods=["POST"])
def auth():
    print("-------------------------hello----------------------")
    user_email = request.form.get("email")
    user_password = request.form.get("pass")
    users_data = Users.query.filter_by(email=user_email).first()
    if user_password == users_data.password :
        # pass
        # db.session.add(user_email)
        # db.session.commit()
        session["email"] = user_email
        print("Hello")
        return render_template("logout.html")
    else :
        return redirect(url_for('login.html'))

@app.route("/welcome", methods=["GET","POST"])
def logout():
    if request.method == "GET" :
    # user = user_email
        if session.get("email") is not None:
            user_email = session.get("email")
            session.clear()
            # db.session.commit()
            return render_template("welcome.html")
        else :
            details = "Session experied login again"
            return render_template("hello.html", name = details)
    else :
        return redirect(url_for('logout.html'))
