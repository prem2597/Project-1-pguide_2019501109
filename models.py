# from flask_sqlalchemy import TIMESTAMP
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "Users"
    name = db.Column(db.String, nullable=False)
    dob = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    email = db.Column(db.String, primary_key=True)
    phone = db.Column(db.String, nullable=False)
    password = db.Column(db.String, primary_key=True)
    timestamp = db.Column(db.String, nullable=False)
