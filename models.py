# from flask_sqlalchemy import TIMESTAMP
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql.schema import ForeignKey, PrimaryKeyConstraint
from sqlalchemy import *
# from flask_marshmallow import Marshmallow

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = "Users"
    name = db.Column(db.String, nullable=False)
    dob = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    email = db.Column(db.String, primary_key=True)
    phone = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    timestamp = db.Column(db.String, nullable=False)

class Books(db.Model):
    __tablename__ = "Books"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)

class Review(db.Model):
    __tablename__="Reviews"
    isbn = db.Column(db.String, ForeignKey("Books.isbn"))
    username = db.Column(db.String, ForeignKey("Users.email"))
    rating = db.Column(db.Integer)
    review = db.Column(db.String)

    __table_args__ = (PrimaryKeyConstraint("isbn", "username"),)

