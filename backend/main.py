from logging import error
from flask import Flask, render_template,request,redirect, url_for,session, g, flash
import os
import sqlite3
from werkzeug.security import check_password_hash


app = Flask(__name__, template_folder='../templates')
app.secret_key = 'EaseHeaven@123'

#generated_secret_key via cmd

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
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
    return render_template('Pr_reg.html')

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

@app.route('/Partner_Management')
def Partner_mng():
    return render_template('Admin_dash2.html')

@app.route('/Customers_management')
def Cust_mng():
    return render_template('Admin_dash3.html')

@app.route('/Admin_login')
def Admin_login():
    return render_template('Admin_login.html')

@app.route('/Partner_login')
def Partner_login():
    return render_template('Pr_login.html')



#-------------------END---------------------------------------#

#--------------------Authentication----------------------------#

#-----> User Registration

@app.route("/Reg_user", methods=['GET', 'POST'])
def Reg_user():
        if request.method == 'POST':
            # Collect form data
            userid = request.form['username']
            password = request.form['password']
            Fullname = request.form['name']
            Gender = request.form['gender']
            address = request.form['address']
            Pincode = request.form['pincode']
            phone = request.form['contact']
            email = request.form['email']
            status= "Unblocked"


            # Insert data into the database
            db = get_db()
            cursor = db.cursor()


            cursor.execute("SELECT * FROM customer_details WHERE username = ?", (userid,))
            existing_user=cursor.fetchone()

            if existing_user:
                flash('Username already exist. Please choose another username')
                return render_template('User_reg.html')




            cursor.execute('''INSERT INTO customer_details 
                              (username, password, name, gender, address, pincode, phone, email ,status ) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ? ,?)''',
                           (userid, password, Fullname,Gender, address, Pincode, phone, email , status))
            db.commit()
            flash('Registration successful!')
            return redirect(url_for('home'))
        return render_template('User_reg.html')



#---------------> User login
@app.route("/login_pg", methods=['GET', 'POST'])
def login_pg():
    if request.method == 'POST':
        id = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM customer_details WHERE username = ? AND password = ? AND status=? ", (id, password,"Unblocked"))
        user = cursor.fetchone()

        if user:
            session['id'] = id
            return redirect(url_for('User_dash'))
        else:
            flash('Invalid user ID or password.')
            return redirect(url_for('home'))
    return render_template('User_login.html')



#-----------> Admin login

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        id = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM admin WHERE username = ? ", (id, ))
        user = cursor.fetchone()

        if user :
            print(user)
            if check_password_hash(user[2],password):
                session['id'] = id
                return redirect(url_for('Service'))
        else:
            flash('Invalid user ID or password.')
            return redirect(url_for('Admin_login'))
    return render_template('Admin_login.html')

#------> Partners Registration 

@app.route("/Reg_partner", methods=['GET', 'POST'])
def Reg_partner():
        if request.method == 'POST':
            # Collect form data
            userid = request.form['username']
            password = request.form['password']
            Fullname = request.form['name']
            Gender = request.form['gender']
            address = request.form['address']
            Pincode = request.form['pincode']
            phone = request.form['contact']
            email = request.form['email']
            status= "Unblocked"
            exp=request.form['exp']
            serv=request.form['service']


            # Insert data into the database
            db = get_db()
            cursor = db.cursor()


            cursor.execute("SELECT * FROM active_professional WHERE username = ?", (userid,))
            existing_user=cursor.fetchone()

            if existing_user:
                flash('Username already exist. Please choose another username')
                return render_template('Pr_reg.html')




            cursor.execute('''INSERT INTO professional 
                              (username, password, full_name, gender, address, pincode, phone, email ,status, service_type , experience) 
                              VALUES (?, ?, ?, ?, ?, ?, ?, ? ,? , ? , ?)''',
                           (userid, password, Fullname,Gender, address, Pincode, phone, email , status , serv , exp))
            db.commit()
            flash('Registration successful!')
            return redirect(url_for('Partner_login'))
        return render_template('Pr_reg.html')



if __name__ == '__main__':
    app.run(debug=True)

