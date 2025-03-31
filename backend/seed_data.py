from models import db, User  # Assuming 'User' is your model name
from app import app

with app.app_context():
    # Sample User Data
    test_user = User(username='admin', password='123')

    # Add data to the database
    db.session.add(test_user)
    db.session.commit()

    print("Sample user added successfully! 🚀")
