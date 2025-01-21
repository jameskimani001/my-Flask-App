# app.py
from flask import Flask
from flask_jwt_extended import JWTManager
from model import db
from views.auth import auth_bp  # Import the auth blueprint
from views.post import posts_bp  # Import the posts blueprint


# Initialize the app
app = Flask(__name__)

# Flask app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkey'

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(posts_bp)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
