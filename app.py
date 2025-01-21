from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from model import db, User, Post
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Flask app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Secret key for JWT

# Initialize extensions
db.init_app(app)  # Initialize the db with the app
jwt = JWTManager(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# User Registration Route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if the user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "User already exists"}), 400

    # Hash the password using pbkdf2:sha256
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    # Create a new user
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully!"}), 201

# User Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    # Check if user exists and password is correct
    if user and check_password_hash(user.password, data['password']):
        # Create JWT token
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Invalid username or password"}), 401

# Create a new Post
@app.route('/post', methods=['POST'])
@jwt_required()  # Ensure the user is logged in (JWT required)
def create_post():
    data = request.get_json()

    # Get the user ID from the JWT token
    user_id = get_jwt_identity()

    # Create a new post
    new_post = Post(title=data['title'], content=data['content'], user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"msg": "Post created successfully!"}), 201

# View all posts of the current user
@app.route('/posts', methods=['GET'])
@jwt_required()
def get_user_posts():
    user_id = get_jwt_identity()
    
    # Fetch posts of the current logged-in user
    posts = Post.query.filter_by(user_id=user_id).all()
    
    if posts:
        posts_data = [{"id": post.id, "title": post.title, "content": post.content} for post in posts]
        return jsonify(posts_data), 200

    return jsonify({"msg": "No posts found"}), 404

# View a specific post by ID
@app.route('/post/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    user_id = get_jwt_identity()
    
    # Fetch the post by ID for the logged-in user
    post = Post.query.filter_by(id=post_id, user_id=user_id).first()
    
    if post:
        return jsonify({"id": post.id, "title": post.title, "content": post.content}), 200

    return jsonify({"msg": "Post not found"}), 404

# Update a post by ID
@app.route('/post/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    data = request.get_json()
    user_id = get_jwt_identity()

    # Fetch the post by ID for the logged-in user
    post = Post.query.filter_by(id=post_id, user_id=user_id).first()

    if post:
        post.title = data.get('title', post.title)
        post.content = data.get('content', post.content)
        db.session.commit()
        return jsonify({"msg": "Post updated successfully!"}), 200

    return jsonify({"msg": "Post not found"}), 404

# Delete a post by ID
@app.route('/post/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    user_id = get_jwt_identity()

    # Fetch the post by ID for the logged-in user
    post = Post.query.filter_by(id=post_id, user_id=user_id).first()

    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({"msg": "Post deleted successfully!"}), 200

    return jsonify({"msg": "Post not found"}), 404

# Delete a user (only the user can delete their own account)
@app.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    
    # Only the user themselves can delete their own account
    if current_user_id == user_id:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"msg": "User deleted successfully!"}), 200
        return jsonify({"msg": "User not found"}), 404
    
    return jsonify({"msg": "Unauthorized"}), 403

# View all registered users (any authenticated user can view this)
@app.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    # Fetch all registered users
    users = User.query.all()
    users_data = [{"id": u.id, "username": u.username} for u in users]
    return jsonify(users_data), 200

# Main function to run the app
if __name__ == '__main__':
    app.run(debug=True)
