import os
import json
from datetime import datetime
from flask import Flask, render_template, request, session , url_for, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from flask_sqlalchemy import SQLAlchemy
import requests
import logging
# import flask.ext.sqlalchemy as flask_sqlalchemy
# import flask_whooshalchemy as wa

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.secret_key = 'super secret key'
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATION "] = False
Session(app)
db.init_app(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def coverpage():
    return render_template("welcome.html")

@app.route("/register")
def register():
    return render_template("Registration.html")

@app.route("/hello", methods=["GET", "POST"])
def hello():
    # db.create_all()
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

@app.route("/auth", methods=["GET","POST"])
def auth():
    # print("-------------------------hello----------------------")
    session.clear()
    if request.method == 'POST' :
        user_email = request.form.get("email")
        user_password = request.form.get("pass")
        users_data = Users.query.filter_by(email=user_email).first()
        if user_password == users_data.password :
            # pass
            # db.session.add(user_email)
            # db.session.commit()
            session["email"] = user_email
            # print("Hello")
            return render_template("logout.html")
        else :
            return redirect(url_for('login'))
    else :
        return render_template("login.html")

# @app.route("/search", methods=['POST'])
# # @auth_required
# def search():
#     print("-------------------------------------Hello")
#     searchword = request.form.get("data")
#     print(searchword)
#     searchword = "%" + searchword + "%"
#     books = Books.query.filter(Books.title.like(searchword)).all()
#     books1 = Books.query.filter(Books.author.like(searchword)).all()
#     books2 = Books.query.filter(Books.isbn.like(searchword)).all()
#     # books3 = Books.query.filter(Books.year.like(searchword)).all()
#     bookdata = books + books1 + books2
#     print(books)
#     return render_template("search.html", booklist = bookdata)

# @app.route("/book/<isbn>", methods=["GET"])
# def bookInfo(isbn):
#     # pass
#     response = goodread_api(isbn)
#     return render_template("bookInfo.html", Name = response["name"], Author = response["author"], ISBN = response["isbn"], Year = response["year"], rating = response["average_rating"], count = response["reviews_count"], image = response["img"])

# def goodread_api(isbn):
#     res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "0gaifU0ED4eOcG7fDno6g", "isbns": isbn}) 
#     logging.debug("Goodreads call Success")
#     response = res.json()
#     response = response['books'][0]
#     book_info = Books.query.get(isbn)
#     logging.debug("DB query executed successfully")
#     response['name'] = book_info.title
#     response['author'] = book_info.author
#     response['year'] = book_info.year
#     response['img'] = "http://covers.openlibrary.org/b/isbn/" + isbn + ".jpg"
#     return response

@app.route("/welcome", methods=["GET","POST"])
def logout():
    if request.method == "GET" :
    # user = user_email
        if session.get("email") is not None:
            # print("--------------------------------hi")
            user_email = session.get("email")
            session.clear()
            # db.session.commit()
            return render_template("welcome.html")
        else :
            details = "Session experied login again"
            return render_template("hello.html", name = details)
    else :
        return redirect(url_for('logout.html'))
