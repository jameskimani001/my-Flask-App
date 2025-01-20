# my-Flask-App

# Flask User Authentication with JWT and Post Creation API -->
This Flask app implements user registration, login functionality with JWT (JSON Web Tokens) authentication, and the ability to create and retrieve posts. It uses SQLAlchemy for database management and JWT for authentication.

# Features
User Registration: Allows users to register with a username and password.
User Login: Users can log in and obtain a JWT token.
JWT Authentication: Protects routes with JWT authentication for authorized access.
Post Creation: Allows logged-in users to create posts.
View Posts: Allows users to retrieve posts they created.
# Requirements
Python 3.8+
Flask
Flask-SQLAlchemy
Flask-JWT-Extended
Werkzeug
# Setup Instructions
1. Clone the Repository
Clone this repository to your local machine:
git clone <repository-url>
cd <project-directory>
2. Create a Virtual Environment
It's recommended to use a virtual environment to keep dependencies isolated.
<!-- python3 -m venv flask_env -->
source flask_env/bin/activate  # On Windows, use flask_env\Scripts\activate
3. Install Dependencies
Install the required Python packages by running:
<!-- pip install -r requirements.txt -->
Alternatively, install them individually:
<!-- pip install Flask Flask-SQLAlchemy Flask-JWT-Extended Werkzeug -->
4. Create the Database Tables
Before starting the app, create the required tables:
<!-- flask create_tables -->
5. Configure the Flask App
Make sure the app.py file is configured correctly for your environment. By default, it uses sqlite:///users.db as the database URI, which will create a SQLite database in your project folder.

API Endpoints
1. User Registration (POST /register)
Register a new user.

URL: /register

Method: POST

Body (JSON):

json

<!-- {
  "username": "john_doe",
  "password": "password123"
} -->
Response (Success):

json
<!-- {
  "msg": "User registered successfully!"
} -->
Response (Failure):

json
<!-- {
  "msg": "User already exists"
} -->
2. User Login (POST /login)
Login to the application and get a JWT token.

URL: /login

Method: POST

Body (JSON):

json
<!-- {
  "username": "john_doe",
  "password": "password123"
} -->
Response (Success):

json
<!-- {
  "access_token": "<your-jwt-token>"
} -->
Response (Failure):

json
<!-- {
  "msg": "Invalid username or password"
} -->
3. Create Post (POST /post)
Create a new post (only accessible to authenticated users).

URL: /post

Method: POST

Headers: Authorization: Bearer <your-jwt-token>

Body (JSON):

json
<!-- {
  "title": "My First Post",
  "content": "This is the content of my first post."
} -->
Response (Success):

json
<!-- {
  "msg": "Post created successfully!"
} -->
4. Get Posts (GET /posts)
Get all posts created by the authenticated user.

URL: /posts

Method: GET

Headers: Authorization: Bearer <your-jwt-token>

Response (Success):

json
<!-- [
  {
    "id": 1,
    "title": "My First Post",
    "content": "This is the content of my first post."
  }
] -->
5. Get Current User (GET /current_user)
Get the current logged-in user's username.

URL: /current_user

Method: GET

Headers: Authorization: Bearer <your-jwt-token>

Response (Success):

json
<!-- {
  "username": "john_doe"
} -->
Running the App
1. Start the Flask Development Server
To start the app in development mode, run:
<!-- flask run --debug -->
The app will be accessible at http://127.0.0.1:5000.

Testing the API with Postman
Register a new user:

Send a POST request to /register with the user details in the request body.
Login:

Send a POST request to /login with the username and password. You will receive a JWT token in the response.
Create a Post:

Send a POST request to /post with the title and content. Include the Authorization header with the Bearer <jwt-token>.
Get Posts:

Send a GET request to /posts with the Authorization header set to Bearer <jwt-token>.
Get Current User:

Send a GET request to /current_user with the Authorization header set to Bearer <jwt-token>.
# well created and coded by passion by Techei kim