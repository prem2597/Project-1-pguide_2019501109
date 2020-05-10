import csv
import os
import json
from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from models import *

app1 = Flask(__name__)

app1.config["SESSION_PERMANENT"] = False
app1.config["SESSION_TYPE"] = "filesystem"
Session(app1)
db = SQLAlchemy()

app1.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app1.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app1.app_context().push()

db.init_app(app1)

class Books(db.Model):
    __tablename__ = "Books"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __init__(self, isbn, title, author, year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year

db.create_all()

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    i = 0
    for isbn, title, author, year in reader:
        if i!= 0 :
            book = Books(isbn=isbn, title=title, author=author, year=year)
            db.session.add(book)
        i = i + 1
    db.session.commit()

if __name__ == "__main__":
    main()
