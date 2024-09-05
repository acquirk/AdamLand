from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Set a secret key for CSRF protection
app.config['SECRET_KEY'] = '4b2e2f12ff1e9c33a69f9fbd1f63b2a1'  # Replace with a real secret key

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Import routes and models at the bottom to avoid circular imports
from app import routes, models

