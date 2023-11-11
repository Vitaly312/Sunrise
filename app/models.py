from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False, unique=True)
    gender = db.Column(db.Boolean())
    password_hash = db.Column(db.String(200), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.now)

    def __repr__(self):
	    return f"<{self.id}:{self.name}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(5000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='tasks', cascade='all,delete')
    done = db.Column(db.Boolean(), default=False, nullable=False)
    date_completed = db.Column(db.DateTime())
    created_on = db.Column(db.DateTime(), default=datetime.now)

    def __repr__(self):
        return f"<{self.id}>:<{self.title[:40]}>"

    def __str__(self):
        return self.title

    def set_done(self):
        self.done = True
        self.date_completed = datetime.now()