# views/auth.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from model import db, User
from flask_jwt_extended import create_access_token

# Create Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# User registration route
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "User already exists"}), 400

    # Hash password
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    # Create new user and save to database
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully!"}), 201

# User login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Check if user exists and password matches
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Invalid credentials"}), 401
