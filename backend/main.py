from logging import error
from flask import Flask, render_template,request,redirect, url_for,session, g, flash
import os
import sqlite3

app = Flask(__name__)
app.secret_key = app.secret_key = os.environ.get('SECRET_KEY', 'dev-fallback')
app = Flask(__name__, template_folder='../templates')
#generated_secret_key via cmd

Database = 'Database.db'

#Establishing Connection with Database

def get_db():
    db = getattr(g, '_database',None)
    if db is None:
        db = g._database = sqlite3.connect(Database)
    return db

#----------------Section of PAge Rendering------------------#

@app.route('/')
def home():
    return render_template('Home.html')  # This will include base.html properly

@app.route('/Registration')
def User_reg():
    return render_template('User_reg.html')

@app.route('/Professional_SignUp')
def pr_reg():
    return render_template('Pr.reg.html')

@app.route('/EaseHeaven')
def User_dash():
    return render_template('User_Dash.html')

@app.route('/Professional')
def Pr_reg():
    return render_template('Pr_reg.html')

@app.route('/Professionals_Dash')
def Pr_dash():
    return render_template('Pr_Dash.html')

@app.route('/Service_Management')
def Service():
    return render_template('Admin_dash1.html')

@app.route('/Partner Management')
def Partner_mng():
    return render_template('Admin_dash2.html')

@app.route('/Customers_management')
def Cust_mng():
    return render_template('Admin_dash3.html')

@app.route('/Admin_login')
def Admin_login():
    return render_template('Admin_login.html')

#-------------------END---------------------------------------#



if __name__ == '__main__':
    app.run(debug=True)

