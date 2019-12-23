from datetime import datetime, timedelta
from flask import jsonify, request
from jwt import encode as jwtEncode
from sqlalchemy import desc
from app import app, db
from config import app_secret_key
from models import *
from wrappers import user_token_available, userRequiredJson
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/movies', methods=['post'])
@userRequiredJson('admin')
def insertMovie(admin):
    data_json = request.get_json()
    print(data_json)
    if (not data_json):
        return jsonify({'err': "body is empty or can't be parsed to a valid json"}), 400
    interestingData = ('name', 'genre', 'length', 'screenId')
    mappingInDb =     ('name', 'genre', 'length', 'screenId')
    d = {dbKey: data_json[apiKey] for apiKey, dbKey in zip(interestingData, mappingInDb)}
    newMovie = Movie(**d)
    db.session.add(newMovie)
    db.session.commit()
    res = {**newMovie.as_dict(), 'screen': newMovie.screen.as_dict(), 'screenings': [s.as_dict() for s in newMovie.screenings]}
    return jsonify({'movie': res}), 200

@app.route('/movies/<int:movieId>', methods=['post'])
@userRequiredJson('admin')
def addMovieScreening(admin, movieId):
    data_json = request.get_json()
    if (not data_json):
        return jsonify({'err': "body is empty or can't be parsed to a valid json"}), 400
    data_json['movieId'] = movieId
    interestingData = ('movieId', 'time')
    mappingInDb =     ('movieId', 'dateTime')
    d = {dbKey: data_json[apiKey] for apiKey, dbKey in zip(interestingData, mappingInDb)}
    newScreening = Screening(**d)
    db.session.add(newScreening)
    db.session.commit()
    return jsonify({'screening': newScreening.as_dict()}), 200

@app.route('/movies/', methods=['get'])
@userRequiredJson('admin, customer')
def listMovies(user):
    movies = Movie.query.all()
    return jsonify({'movies': [{**m.as_dict(), 'screen': m.screen.as_dict(), 'screenings': [s.as_dict() for s in m.screenings]} for m in movies]}), 200

@app.route('/screenings/<int:screeningId>/reservations', methods=['get'])
@userRequiredJson('admin, customer')
def listScreeningReservations(user, screeningId):
    screening = Screening.query.filter_by(id=screeningId).first()
    if screening is None:
        return jsonify({"err": "invalid screening id"}), 400
    screeningReservations = screening.reservations
    return jsonify({"reservations": [r.as_dict() for r in screeningReservations]})

@app.route('/screenings/<int:screeningId>/reservations', methods=['post'])
@userRequiredJson('admin, customer')
def makeReservation(user, screeningId):
    screening = Screening.query.filter_by(id=screeningId).first()
    if screening is None:
        return jsonify({"err": "invalid screening id"}), 400
    data_json = request.get_json()
    if not data_json:
        return jsonify({'err': "body is empty or can't be parsed to a valid json"}), 400
    requestedPos = data_json['pos']
    isPosAvailable = Reservation.query.filter_by(screening_id=screeningId, pos=requestedPos).first() == None
    if not isPosAvailable:
        return jsonify({'err': "another customer has just taken this pos"}), 405
    # TODO : this should be handled atomically through database itself
    screeningReservations = screening.reservations
    newReseravation = Reservation(user_id = user['id'], screening_id = screeningId, pos = requestedPos)
    db.session.add(newReseravation)
    db.session.commit()
    return jsonify({"ticket": newReseravation.id})


@app.route('/signup', methods=['post'])
def signup():
    data_json = request.get_json()
    hashedPassword = generate_password_hash(data_json['password'], method='sha256')
    interestingData = ('fname', 'lname', 'username', 'email', 'birthDate')
    mappingInDb =     ('fname', 'lname', 'username', 'email', 'birthDate')
    d = {dbKey: data_json[apiKey] for apiKey, dbKey in zip(interestingData, mappingInDb)}
    newUser = User(**d, password=hashedPassword)
    db.session.add(newUser)
    db.session.commit()
    token = jwtEncode({
        'userId': newUser.id,
        'role': newUser.role,
        'username': newUser.username,
        'email': newUser.email,
        'exp': datetime.utcnow() + timedelta(hours=48)
    }, app.config['SECRET_KEY']).decode('UTF-8')
    return jsonify({'token': token, 'role': newUser.role}), 200

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'err': "you should enter username and password"}), 401

    userId = auth.username.strip()
    password = auth.password
    user = User.query.filter_by(username=userId).first()
    if (not user):
        return jsonify({'err': 'not a valid user'}), 400
    user = user.as_dict()
    if not check_password_hash(user['password'], password):
        return jsonify({'err': 'not a valid user (pass)'}), 400
    token = jwtEncode({
        'userId': user['id'],
        'role': user['role'],
        'username': user['username'],
        'email': user['email'],
        'exp': datetime.utcnow() + timedelta(hours=48)
    }, app.config['SECRET_KEY']).decode('UTF-8')
    return jsonify({'token': token, 'role': user['role']}), 200
