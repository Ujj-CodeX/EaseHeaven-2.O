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
    db = get_db()
    cursor = db.cursor()
    query = "SELECT name FROM service"
    cursor.execute(query)
    service = [row[0] for row in cursor.fetchall()]
    

    return render_template('Pr_reg.html', service=service)


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
    return redirect(url_for('show2'))

@app.route('/Customers_management')
def Cust_mng():
    return redirect(url_for('show3'))

@app.route('/Admin_login')
def Admin_login():
    return render_template('Admin_login.html')

@app.route('/Partner_login')
def Partner_login():
    return render_template('Pr_login.html')


@app.route('/Booking_management')
def Booking():
    return render_template('Booking_mng.html')


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
                return redirect(url_for('show'))
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
            status= "INACTIVE"
            exp=request.form['exp']
            serv=request.form['service']

            db=get_db()
            cursor=db.cursor()
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


#------------------> Service management

@app.route('/service', methods=['GET', 'POST'])
def service():
    
    if request.method == 'POST' :
       ser = request.form['service']
       price = request.form['price']

       db = get_db()
       cursor = db.cursor()
       cursor.execute('''INSERT INTO service (name,charges) VALUES (?, ?)''',(ser, price))
       db.commit()
       flash('Service Creation successful!')



    
    return render_template(url_for('show'))

@app.route('/Show_table', methods=['GET' , 'POST'])
def show():
    db = get_db()
    cursor = db.cursor()


    result = None  # to hold the searched service result

    # If form submitted (POST)
    if request.method == 'POST':
        service_name = request.form.get('service_name')
        cursor.execute("SELECT name, charges FROM service WHERE name = ?", (service_name,))
        result = cursor.fetchone()

    cursor.execute('SELECT name, charges ,id FROM service')
    table1 = cursor.fetchall()
    return render_template('Admin_dash1.html' , table1=table1 ,  result=result)


@app.route('/delete_service/<int:service_id>', methods=['POST'])
def delete(service_id):
    db = get_db()
    cursor =db.cursor()
    cursor.execute("DELETE FROM service WHERE id = ?", (service_id,))
    db.commit()
    flash("Service deleted successfully.")
    return redirect(url_for('show'))


@app.route('/update_service/<int:service_id>', methods=['POST'])
def update(service_id):
    name=request.form['service']
    price = request.form['price']

    db=get_db()
    cursor=db.cursor()
    cursor.execute("UPDATE service SET name = ?, charges = ? WHERE id = ?", (name, price, service_id))
    db.commit()
    flash("Service updated successfully.")
    return redirect(url_for('show'))
 

#-------------------Searching of Service ------->>>>

@app.route('/search-service', methods=['POST'])
def search_service():
    service= request.form['service_name']
    
    db= get_db()
    cursor=db.cursor()
    cursor.execute("SELECT * FROM service WHERE name = ?", (service,))
    result = cursor.fetchone()


    return redirect(url_for('show'), result=result)



###-----------------------Review Block ----->>>>>
@app.route('/review', methods=['POST'])
def user_review():
    db= get_db()
    cursor=db.cursor()
    ID =session['id']
    rv=request.form['review']
    cursor.execute('''INSERT INTO review (username, review) VALUES (?, ?)''', (ID, rv))
    db.commit()
    flash('Review Submitted!', 'success')
    return redirect(url_for('User_dash'))


##------------------Partners Management------>.
@app.route('/Show_table2', methods=['GET' , 'POST'])
def show2():
    db = get_db()
    cursor = db.cursor()


    result = None  # to hold the searched service result

    # If form submitted (POST)
    if request.method == 'POST':
        username = request.form.get('username')
        cursor.execute("SELECT full_name, gender , phone , pincode ,address , email, experience, status , service FROM active_professional WHERE username = ?", (username,))
        result = cursor.fetchone()



       ##----Block and Unblock of professionals-----

    cursor.execute('SELECT username, email, phone , service,gender,experience, address FROM active_professional')
    table2 = cursor.fetchall()

    cursor.execute('SELECT username , full_name, phone , gender , experience , service_type , address , pincode FROM professional')
    table1 = cursor.fetchall()
    
    

    if request.method == 'POST' and 'approve_professional' in request.form:
        
        user_id = request.form.get('username')
        cursor.execute(''' INSERT INTO active_professional (username,password,gender,pincode,phone,address,email,service,full_name,experience,status )
                       SELECT username,password,gender,pincode,phone,address,email ,service_type ,full_Name,experience,'Unblocked' FROM professional WHERE username = ? ''', (user_id,))
        cursor.execute('''
                    DELETE FROM professional
                    WHERE username = ?
                ''', (user_id,))
        db.commit()

    if request.method == 'POST' and 'reject_professional' in request.form:
        user_id = request.form.get('username')
        cursor.execute('DELETE FROM professional WHERE username = ?', (user_id,))
        db.commit()


    cursor.execute('SELECT service, COUNT(*) FROM active_professional GROUP BY service')
    data = cursor.fetchall()

    labels = [row[0] for row in data]
    counts = [row[1] for row in data]

    return render_template('Admin_dash2.html' , table1=table1 ,  result=result , table2=table2 , labels=labels , counts = counts)




####----------------------Customers Management ----------->>>>

@app.route('/Show_table3', methods=['GET' , 'POST'])
def show3():
    db = get_db()
    cursor = db.cursor()


    result = None  # to hold the searched service result

    # If form submitted (POST)
    if request.method == 'POST':
        username = request.form.get('username')
        cursor.execute("SELECT name, gender , phone , pincode ,address , email, status FROM customer_details WHERE username = ?", (username,))
        result = cursor.fetchone()



       ##----Block and Unblock of professionals-----


    cursor.execute('SELECT username , name, phone , gender , pincode FROM customer_details')
    table1 = cursor.fetchall()
    
    

    cursor.execute('SELECT service, COUNT(username) FROM service_request GROUP BY service')
    data = cursor.fetchall()

    labels = [row[0] for row in data]
    counts = [row[1] for row in data]

    return render_template('Admin_dash3.html' , table1=table1 ,  result=result , labels=labels , counts = counts)




if __name__ == '__main__':
    app.run(debug=True)

