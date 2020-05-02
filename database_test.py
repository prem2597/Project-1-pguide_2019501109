import os,unittest
from models import *
from application import *
from flask_sqlalchemy import sqlalchemy
from flask import session
from flask.app import Flask


class TestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db = SQLAlchemy()
        db.init_app(app)
        app.app_context().push()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        
        if not os.getenv("DATABASE_URL"):
            raise RuntimeError("DATABASE_URL is not set")
        self.app = app.test_client()
        # self.assertEqual(app.DEBUG, False)
        # db.create_all()

    def tearDown(self):
        # db.session.remove()
        # db.drop_all()
        pass

    def test_make_unique_nickname(self):
        # book = Books(isbn = "123456", title = "2States", author = "Chetan Bhagat", year = "2015")
        # db.session.add(book)
        # db.session.commit()
        # name = Books.query.get('123456').title
        # assert name == '2States'
        # book = Books(isbn = "123457", title = "Revolution2020", author = "Chetan Bhagat", year = "2013")
        # db.session.add(book)
        # db.session.commit()
        name = Books.query.filter(Books.title.like("Chetan Bhagat")).all()
        # name = Books.query.get(title = 'Chetan Bhagat')
        # name = name.title
        print(type(name))
        self.assertEqual(0, len(name))

if __name__ == '__main__':
    unittest.main()