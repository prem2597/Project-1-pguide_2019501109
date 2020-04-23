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
#change made by viswa
import flask_whooshalchemy as wa
from models import *

app1 = Flask(__name__)

app1.config["SESSION_PERMANENT"] = False
app1.config["SESSION_TYPE"] = "filesystem"
Session(app1)
db = SQLAlchemy()

app1.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# change made by viswa
app1.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
#change made by viswa
app1.config['DEBUG']=True
app1.config['WHOOSH_BASE']='whoosh'
app1.app_context().push()

db.init_app(app1)

class Books(db.Model):
    __tablename__ = "Books"
    __searchable__=['isbn','title','author','year']
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
def search():
    wa.whoosh_index(app1,Books)
    Books.query.whoosh_search('Aztec').all()

if __name__ == "__main__":
    main()