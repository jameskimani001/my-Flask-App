from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from model import db, User, Post  # Importing db and models

# Initialize Flask app
app = Flask(__name__)

# Flask app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Secret key for JWT

# Initialize extensions
db.init_app(app)  # Initialize the db with the app
jwt = JWTManager(app)

# Manually create tables if they do not exist (can be used for debugging)
@app.cli.command('create_tables')
def create_tables():
    with app.app_context():
        db.create_all()
        print("Tables created successfully.")

# User Registration Route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if the user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "User already exists"}), 400

    # Hash the password
    hashed_password = generate_password_hash(data['password'], method='sha256')

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

# Main function to run the app
if __name__ == '__main__':
    app.run(debug=True)
