from flask import Flask
from models import db
import models  # To register all the models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database/Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class CustomerDetails(db.Model):
    __tablename__ = 'customer_details'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Customer {self.username}>'

class ActiveProfessional(db.Model):
    __tablename__ = 'active_professionals'

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

    def __repr__(self):
        return f'<Professional {self.username}>'

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'

    sr_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    date_e = db.Column(db.Date, nullable=False)   # Expected Date
    date_o = db.Column(db.Date, nullable=False)   # Ordered Date
    ser_st = db.Column(db.String(50), nullable=False)  # Service status like "pending", "completed"
    status = db.Column(db.String(50), nullable=False)
    prf_id = db.Column(db.Integer, nullable=False)  # Professional ID

    def __repr__(self):
        return f'<ServiceRequest {self.sr_id} for {self.username}>'

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    review = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Review by {self.username}>'
    

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    charges = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Service {self.name}: ₹{self.charges}>'
    


class Professional(db.Model):
    __tablename__ = 'professionals'

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

    def __repr__(self):
        return f'<Professional {self.username}>'


with app.app_context():
    db.create_all()
    print(" Database and all tables created successfully!")
