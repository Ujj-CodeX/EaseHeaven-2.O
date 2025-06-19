from werkzeug.security import generate_password_hash
from models.model import db, Admin, app

with app.app_context():

    db.create_all()

    
    existing_admin = Admin.query.filter_by(username='Ujju89@').first()
    if not existing_admin:
        admin = Admin(
            username='Ujju89@',
            password=generate_password_hash('985679@U')
        )
        db.session.add(admin)
        db.session.commit()
        print(" Admin created successfully.")
    else:
        print(" Admin already exists.")

    # Confirm from DB
    print(" Current Admin Table:")
    for a in Admin.query.all():
        print( a.username)
