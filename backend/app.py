from flask import Flask
from models import db
from routes import routes  # Import the blueprint
import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_migrate import Migrate




app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)


app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Use a strong secret key
jwt = JWTManager(app)

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

# Initialize the database with the app instance
db.init_app(app)

migrate = Migrate(app, db)

# Register the blueprint
app.register_blueprint(routes)

# Ensure tables are created before running the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database and tables initialized successfully! 🚀")
    app.run(debug=True)
