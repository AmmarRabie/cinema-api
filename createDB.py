from app import db
from models import *
from werkzeug.security import generate_password_hash
import datetime

db.drop_all()
db.create_all()

# insert initial data
admin = User(
    role="admin",
    fname="Ammar",
    lname="Rabie",
    username="AmmarRabie",
    email="ammar.s.rabie@gmail.com",
    password=generate_password_hash("123456789", method="sha256"),
    birthDate=datetime.datetime(1997, 8, 25),
)

screens = [
    Screen(number=1, rows=20, cols=30,),
    Screen(number=2, rows=50, cols=50,),
]

customers = [
    User(
        fname="customer",
        lname="1",
        username="customer1",
        email="customer1@gmail.com",
        password=generate_password_hash("123456789", method="sha256"),
        birthDate=datetime.datetime(1997, 8, 25),
    ),
    User(
        fname="customer2",
        lname="2",
        username="customer2",
        email="customer2@gmail.com",
        password=generate_password_hash("123456789", method="sha256"),
        birthDate=datetime.datetime(1997, 8, 25),
    ),
    User(
        fname="customer3",
        lname="3",
        username="customer3",
        email="customer3@gmail.com",
        password=generate_password_hash("123456789", method="sha256"),
        birthDate=datetime.datetime(1997, 8, 25),
    ),
]

movies = [
	Movie(name="movie1" , genre="action", length=1*60*60, screen=screens[0]),
	Movie(name="movie2" , genre="action", length=1*60*60, screen=screens[0]),
	Movie(name="movie3" , genre="action", length=2*60*60, screen=screens[1]),
	Movie(name="movie4" , genre="action", length=2*60*60, screen=screens[1]),
	Movie(name="movie5" , genre="action", length=2*60*60, screen=screens[1]),
]

screenings = [
	Screening(movie=movies[0], dateTime=datetime.datetime(2019, 12, 21, 20, 0, 0)),
	Screening(movie=movies[0], dateTime=datetime.datetime(2019, 12, 21, 22, 0, 0)),
	Screening(movie=movies[0], dateTime=datetime.datetime(2019, 12, 22, 20, 0, 0)),
	Screening(movie=movies[1], dateTime=datetime.datetime(2019, 12, 21, 20, 0, 0)),
	Screening(movie=movies[1], dateTime=datetime.datetime(2019, 12, 21, 22, 0, 0)),
	Screening(movie=movies[1], dateTime=datetime.datetime(2019, 12, 22, 20, 0, 0)),
	Screening(movie=movies[2], dateTime=datetime.datetime(2019, 12, 27, 20, 0, 0)),
	Screening(movie=movies[3], dateTime=datetime.datetime(2019, 12, 28, 20, 0, 0)),
	Screening(movie=movies[4], dateTime=datetime.datetime(2019, 12, 29, 20, 0, 0)),
]

reservations = [
	Reservation(user=customers[0], screening=screenings[0], pos = '1, 5'),
	Reservation(user=customers[1], screening=screenings[0], pos = '2, 6'),
	Reservation(user=customers[2], screening=screenings[0], pos = '13, 12'),

	Reservation(user=customers[1], screening=screenings[1], pos = '2, 6'),
	Reservation(user=customers[2], screening=screenings[2], pos = '10, 10'),
	Reservation(user=customers[0], screening=screenings[3], pos = '1, 5'),
	Reservation(user=customers[1], screening=screenings[4], pos = '2, 6'),
	Reservation(user=customers[2], screening=screenings[5], pos = '10, 10'),

	Reservation(user=customers[1], screening=screenings[6], pos = '2, 6'),
	Reservation(user=customers[2], screening=screenings[7], pos = '10, 10'),
	Reservation(user=customers[0], screening=screenings[8], pos = '1, 5'),
]

db.session.add(admin)
for reservation in reservations:
	db.session.add(reservation)
db.session.commit()
