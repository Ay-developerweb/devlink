from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Project
from app.schemas.user import UserProfileSchema
from app import db

admin_bp = Blueprint("admin", __name__)
user_schema = UserProfileSchema(many=True)

def is_admin(user):
    return user.role == "admin"

@admin_bp.route("/users", methods=["GET"])
@jwt_required()
def get_all_users():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if not is_admin(current_user):
        return jsonify({"message": "Admins only"}), 403

    users = User.query.all()
    return jsonify(user_schema.dump(users)), 200


@admin_bp.route("/users/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    if not is_admin(current_user):
        return jsonify({"message": "Admins only"}), 403

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted"}), 200
