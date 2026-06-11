from flask import Blueprint, request
from db import conn, cursor
import bcrypt
import jwt
import datetime
from functools import wraps
from flask import request

auth_bp = Blueprint("auth", __name__)

SECRET_KEY = "your_secret_key"

@auth_bp.route("/signup", methods=["POST"])
def signup():

    data = request.json

    email = data["email"]
    password = data["password"]

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    cursor.execute(
        """
        INSERT INTO users (email, password)
        VALUES (%s, %s)
        """,
        (email, hashed_password)
    )

    conn.commit()

    return {
        "message": "User created successfully"
    }
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data["email"]
    password = data["password"]

    # Find user
    cursor.execute(
        """
        SELECT user_id, password
        FROM users
        WHERE email = %s
        """,
        (email,)
    )

    user = cursor.fetchone()

    # User not found
    if user is None:
        return {
            "error": "Invalid email or password"
        }, 401

    user_id = user[0]
    hashed_password = user[1]

    # Verify password
    if not bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    ):
        return {
            "error": "Invalid email or password"
        }, 401

    # Generate JWT token
    token = jwt.encode(
        {
            "user_id": user_id,
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return {
        "token": token
    }
def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        # Read Authorization header
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]

        if not token:
            return {
                "error": "Token is missing"
            }, 401

        try:
            # Remove Bearer prefix
            token = token.split(" ")[1]
            current_user = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])

        except:
            return {
                "error": "Invalid token"
            }, 401

        return f(current_user, *args, **kwargs)

    return decorated