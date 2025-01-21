# views/posts.py
from flask import Blueprint, request, jsonify
from model import db, Post
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create Blueprint for posts
posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

# Create a new post
@posts_bp.route('/', methods=['POST'])
@jwt_required()  # JWT required to create a post
def create_post():
    data = request.get_json()
    user_id = get_jwt_identity()  # Get the user ID from the JWT token

    new_post = Post(title=data['title'], content=data['content'], user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"msg": "Post created successfully!"}), 201

# View all posts of the current user
@posts_bp.route('/', methods=['GET'])
@jwt_required()  # JWT required to view posts
def get_user_posts():
    user_id = get_jwt_identity()
    posts = Post.query.filter_by(user_id=user_id).all()

    if posts:
        posts_data = [{"id": post.id, "title": post.title, "content": post.content} for post in posts]
        return jsonify(posts_data), 200

    return jsonify({"msg": "No posts found"}), 404

# View a specific post by ID
@posts_bp.route('/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    user_id = get_jwt_identity()
    post = Post.query.filter_by(id=post_id, user_id=user_id).first()

    if post:
        return jsonify({"id": post.id, "title": post.title, "content": post.content}), 200

    return jsonify({"msg": "Post not found"}), 404

# Update a post
@posts_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    post = Post.query.filter_by(id=post_id, user_id=user_id).first()

    if post:
        post.title = data.get('title', post.title)
        post.content = data.get('content', post.content)
        db.session.commit()
        return jsonify({"msg": "Post updated successfully!"}), 200

    return jsonify({"msg": "Post not found"}), 404

# Delete a post
@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    user_id = get_jwt_identity()
    post = Post.query.filter_by(id=post_id, user_id=user_id).first()

    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({"msg": "Post deleted successfully!"}), 200

    return jsonify({"msg": "Post not found"}), 404
