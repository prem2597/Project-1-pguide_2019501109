import os
import json
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, session , url_for, redirect, jsonify, abort
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import requests
import logging

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
ma = Marshmallow(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))

class BooksSchema(ma.Schema):
    class Meta:
        fields = ('isbn', 'title', 'author', 'review', 'year', 'rating', 'img', 'user_rating', 'user_review', 'name')

product_schema = BooksSchema ()
products_schema = BooksSchema (many = True)

@app.route("/")
def coverpage():
    return render_template("welcome.html")

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
        full_name = first_name + " " + last_name
        birth = request.form.get("date-of-birth")
        gen = request.form.get("gender")
        mail = request.form.get("email")
        ph = request.form.get("Phone-number")
        pswd = request.form.get("password")
        password = hashlib.md5(pswd.encode()).hexdigest()
        repswd = request.form.get("re-password")
        repassword = hashlib.md5(repswd.encode()).hexdigest()
        user1 = Users(name=full_name, dob=birth, gender=gen, email=mail, phone=ph, password=password, timestamp=datetime.now())
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
    session.clear()
    if request.method == 'POST' :
        user_email = request.form.get("email")
        user_password = request.form.get("pass")
        user_pswd = hashlib.md5(user_password.encode()).hexdigest()
        users_data = Users.query.filter_by(email=user_email).first()
        if user_pswd == users_data.password :
            session["email"] = user_email
            return render_template("logout.html")
        else :
            return redirect(url_for('login'))
    else :
        return render_template("login.html")

@app.route("/search", methods=['POST'])
def search():
    searchword = request.form.get("data")
    searchword = "%" + searchword + "%"
    books = Books.query.filter(Books.title.like(searchword)).all()
    books1 = Books.query.filter(Books.author.like(searchword)).all()
    books2 = Books.query.filter(Books.isbn.like(searchword)).all()
    bookdata = books + books1 + books2
    return render_template("search.html", booklist = bookdata)

@app.route("/book:<isbn>", methods=["GET", "POST"])
def bookInfo(isbn):
    response = goodread_api(isbn)
    if request.method == "GET":
        if session.get('email') is not None:
            email = session["email"]
            name = Users.query.get(email)
            name = name.name
            review_data = Review.query.filter_by(username= email, isbn = isbn).first()
            if review_data is not None:
                rating_data = review_data.rating
                review = review_data.review
                return render_template("bookInfo.html", Name = response["name"], Author = response["author"], ISBN = response["isbn"], Year = response["year"], rating = response["average_rating"], count = response["reviews_count"], image = response["img"], button = "Edit", rating_data = rating_data, Review = review, name = name, Submit = "Edit")
            else :
                return render_template("bookInfo.html", Name = response["name"], Author = response["author"], ISBN = response["isbn"], Year = response["year"], rating = response["average_rating"], count = response["reviews_count"], image = response["img"], button = "Review", rating_data = 0, name = name, Submit = "Submit")
        return redirect(url_for("auth"))
    elif request.method == "POST":
        email = session["email"]
        review_data = Review.query.filter_by(username = email, isbn = isbn).first()
        name = Users.query.get(email)
        name = name.name
        rating_dat = request.form.get('rating')
        rev = request.form.get('matter')
        if review_data is None:
            revs = Review(username = email, isbn = isbn, rating = rating_dat,review = rev)
            total_rating = ((float(response["average_rating"]) * int(response["reviews_count"])) + int(rating_dat))/(int(response["reviews_count"]) + 1)
            response["average_rating"] = str(total_rating)
            response["reviews_count"] = str(int(response["reviews_count"]) + 1)
            db.session.add(revs)
            db.session.commit()
            return render_template("bookInfo.html", Name = response["name"], Author = response["author"], ISBN = response["isbn"], Year = response["year"], rating = response["average_rating"], count = response["reviews_count"], image = response["img"], button = "Edit", rating_data = rating_dat, Review = rev, name = name, Submit = "Edit")
        else:
            review_data.rating = rating_dat
            review_data.review = rev
            total_rating = ((float(response["average_rating"]) * int(response["reviews_count"])) + int(rating_dat))/(int(response["reviews_count"]) + 1)
            db.session.commit()
            return render_template("bookInfo.html", Name = response["name"], Author = response["author"], ISBN = response["isbn"], Year = response["year"], rating = response["average_rating"], count = response["reviews_count"], image = response["img"], button = "Edit", rating_data = rating_dat, Review = rev, name = name, Submit = "Edit")

def goodread_api(isbn):
    key_value = "0gaifU0ED4eOcG7fDno6g"
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key_value, "isbns": isbn})
    response = res.json()
    response = response['books'][0]
    book_info = Books.query.get(isbn)
    response['name'] = book_info.title
    response['author'] = book_info.author
    response['year'] = book_info.year
    response['img'] = "http://covers.openlibrary.org/b/isbn/" + isbn + ".jpg"
    return response

@app.route("/welcome", methods=["GET","POST"])
def logout():
    if request.method == "GET" :
        if session.get("email") is not None:
            user_email = session.get("email")
            session.clear()
            return render_template("welcome.html")
        else :
            details = "Session experied login again"
            return render_template("hello.html", name = details)
    else :
        return redirect(url_for('logout.html'))

@app.route("/api/search", methods=["POST"])
def get_search():
    if request.method == "POST":
        query = request.get_json()
        if 'search' in query:
            text = query["search"].strip()
            searchword = "%" + text + "%"
            books = Books.query.filter(Books.title.like(searchword)).all()
            books1 = Books.query.filter(Books.author.like(searchword)).all()
            books2 = Books.query.filter(Books.isbn.like(searchword)).all()
            bookdata = books + books1 + books2
            l = []
            books_json = {}
            for book in bookdata :
                dict2 = {}
                dict2["isbn"] = book.isbn
                dict2["title"] = book.title
                l.append(dict2)
            books_json["bookdata"] = l
            return jsonify(books_json)

@app.route("/api/book", methods=["GET", "POST"])
def get_bookinfo():
    isbn = request.args.get('isbn')
    if request.method == "POST":
        searched_value = Books.query.filter(Books.isbn.like(isbn)).all()
        result = products_schema.dump(searched_value)
        return jsonify(result[0]), 200
    else :
        key_value = "0gaifU0ED4eOcG7fDno6g"
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": key_value, "isbns": isbn})
        response = res.json()
        book_info = book_det(isbn)
        email = session["email"]
        name = Users.query.get(email)
        name = name.name
        h = book_det_review(isbn,email)
        if book_info is None:
            return jsonify({"success": False})
        l = []
        dict2 = {}
        dict2['title'] = book_info.title
        dict2['author'] = book_info.author
        dict2['year'] = book_info.year
        dict2['isbn'] = book_info.isbn
        dict2['img'] = "http://covers.openlibrary.org/b/isbn/" + isbn + ".jpg"
        dict2['review'] = response["books"][0]["reviews_count"]
        dict2['rating'] = response["books"][0]["ratings_count"]
        dict2['user_rating'] = h['rating']
        dict2['user_review'] = h['review']
        dict2['name'] = name
        l.append(dict2)
        result = products_schema.dump(l)
        return jsonify(result), 200

def book_det(isbn):
    book_info = Books.query.filter(Books.isbn.like(isbn)).all()
    if book_info is None :
        print("Null")
    return book_info[0]

def book_det_review(isbn, email) :
    review_data = Review.query.filter_by(username= email, isbn = isbn).first()
    review_dict = {}
    if review_data is not None:
        review_dict["rating"] = review_data.rating
        review_dict["review"] = review_data.review
    else :
        review_dict["rating"] = '0'
        review_dict["review"] = '0'
    return review_dict

@app.route("/api/submit_review", methods=["GET", "POST"])
def get_review():
    if request.method == "GET":
        isbn = request.args.get('isbn')
        searched_value = Review.query.filter_by(isbn = isbn).all()
        if len(searched_value) == 0:
            return jsonify({"error": "There is no such book"}), 400
        else :
            result = products_schema.dump(searched_value)
            return jsonify(result), 200
    else :
        email = session["email"]
        query = request.get_json()
        if query is not None:
            review_data = Review.query.filter_by(username= email, isbn = query["isbn"]).first()
            if review_data is None :
                revs = Review(username = email, isbn = query["isbn"], rating = query["rating"],review = query["review"])
                db.session.add(revs)
                db.session.commit()
                return jsonify({"success": True})
            else :
                review_data.rating = query["rating"]
                review_data.review = query["review"]
                db.session.commit()
                return jsonify({"success": True})
        else :
            return jsonify({"Failed": False})
