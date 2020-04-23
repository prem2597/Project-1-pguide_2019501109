# from flask_sqlalchemy import TIMESTAMP
import csv
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, session , url_for, redirect
from flask_session import Session
from models import *
# from docutils.parsers import null

db = SQLAlchemy()

db.create_all()

with open('books.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    next(csv_reader)

    for line in csv_reader :
        book1 = Books(isbn=line[0], title=line[1], author=line[2], year=line[3])
        db.session.add(book1)
        db.session.commit()
