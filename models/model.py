from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from werkzeug.security import generate_password_hash


db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class CustomerDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)

class ActiveProfessional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    service = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.String(50), nullable=False)

class ServiceRequest(db.Model):
    sr_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    date_e = db.Column(db.Date, nullable=False)
    date_o = db.Column(db.Date, nullable=False)
    ser_st = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    prf_id = db.Column(db.Integer, nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    review = db.Column(db.Text, nullable=False)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    charges = db.Column(db.Float, nullable=False)

class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    experience = db.Column(db.String(50), nullable=False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password= db.Column(db.String(200), nullable=False)


with app.app_context():
    db.create_all()
    print(" Database and all tables created successfully.")
