from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from app.schemas.user import UserRegisterSchema, UserLoginSchema
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)
register_schema = UserRegisterSchema()
login_schema = UserLoginSchema()

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    errors = register_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    if User.query.filter((User.email == data["email"]) | (User.username == data["username"])).first():
        return jsonify({"message": "User with email or username already exists."}), 400

    user = User(
        email=data["email"],
        username=data["username"]
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    errors = login_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if user and user.check_password(data["password"]):
        #token = create_access_token(identity=user.id)
        token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": token}), 200
    return jsonify({"message": "Invalid email or password"}), 401

from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app.schemas.user import UserProfileSchema

profile_schema = UserProfileSchema()

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify(profile_schema.dump(user)), 200
