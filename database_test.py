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

    def tearDown(self):
        pass

    def test_make_unique_nickname(self):
        name = Books.query.filter(Books.title.like("Chetan Bhagat")).all()
        self.assertEqual(0, len(name))

if __name__ == '__main__':
    unittest.main()
