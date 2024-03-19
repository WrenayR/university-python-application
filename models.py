from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash
from database import db
# db = SQLAlchemy()  # db intitialized here
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret key'
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)
# app.app_context().push()
# db.create_all()

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='regular')
    customer = db.relationship('Customer', backref='user', cascade="all, delete-orphan", passive_deletes=True, lazy=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Customer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    account_number = db.Column(db.Integer, nullable=False)
    sort_code = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f'<User {self.id} - {self.first_name} {self.last_name}>'
