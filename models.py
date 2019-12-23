from app import db
from datetime import datetime


# class ModelWithDictRepr(db.Model):
#     def as_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Screening(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movieId = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False)
    # reservations = db.relationship('reservation', backref=db.backref('screening', lazy=True, cascade="all, delete-orphan")) # reservations in this screen by all users
    reservations = db.relationship('Reservation', backref='screening') # reservations in this screen by all users
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    fname = db.Column(db.String(12), nullable=False)
    lname = db.Column(db.String(12), nullable=False)
    birthDate = db.Column(db.DateTime, nullable=False)
    role = db.Column(db.String(10), nullable=False, default='customer')  # till now, the value should be in [admin, customer]

    # reservations = db.relationship('reservation', backref=db.backref('user', lazy=True, cascade="all, delete-orphan"), lazy=True) # reservations of this user in all screens
    reservations = db.relationship('Reservation', backref='user', lazy=True) # reservations of this user in all screens
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(20), nullable=False)
    length = db.Column(db.Integer)
    screenId = db.Column(db.Integer, db.ForeignKey('screen.id'), nullable=False)

    # screenings = db.relationship('Screening', backref=db.backref('movie', lazy=True, cascade="all, delete-orphan"), lazy=True)
    screenings = db.relationship('Screening', backref='movie', lazy=True)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Screen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True)
    rows = db.Column(db.Integer)
    cols = db.Column(db.Integer)
    # movies = db.relationship('Movie', backref=db.backref('screen', lazy=True, cascade="all, delete-orphan"), lazy=True)
    movies = db.relationship('Movie', backref='screen', lazy=True)
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# reservation = db.Table('reservation',
#     db.Column('id', db.Integer, primary_key=True),
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
#     db.Column('screening_id', db.Integer, db.ForeignKey('screening.id'), nullable=False),
#     db.Column('pos', db.String(10), nullable=False) # like (1, 3)
# )

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    screening_id = db.Column(db.Integer, db.ForeignKey('screening.id'), nullable=False)
    pos = db.Column(db.String(10), nullable=False) # like "1, 3"
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}    