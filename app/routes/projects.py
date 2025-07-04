from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Project, User
from app import db
from app.schemas.project import ProjectSchema

projects_bp = Blueprint("projects", __name__)
project_schema = ProjectSchema()
project_list_schema = ProjectSchema(many=True)


@projects_bp.route("/", methods=["POST"])
@jwt_required()
def create_project():
    data = request.get_json()
    errors = project_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    user_id = get_jwt_identity()
    project = Project(
        title=data["title"],
        description=data.get("description"),
        link=data.get("link"),
        screenshot=data.get("screenshot"),
        user_id=user_id
    )
    db.session.add(project)
    db.session.commit()

    return jsonify({"message": "Project created successfully", "project": project_schema.dump(project)}), 201


@projects_bp.route("/", methods=["GET"])
@jwt_required()
def get_user_projects():
    user_id = get_jwt_identity()
    projects = Project.query.filter_by(user_id=user_id).all()
    return jsonify(project_list_schema.dump(projects)), 200


@projects_bp.route("/<int:id>", methods=["GET"])
def get_project(id):
    project = Project.query.get_or_404(id)
    return jsonify(project_schema.dump(project)), 200


@projects_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_project(id):
    user_id = get_jwt_identity()
    project = Project.query.get_or_404(id)

    if project.user_id != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    errors = project_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    project.title = data.get("title", project.title)
    project.description = data.get("description", project.description)
    project.link = data.get("link", project.link)
    project.screenshot = data.get("screenshot", project.screenshot)

    db.session.commit()

    return jsonify({"message": "Project updated", "project": project_schema.dump(project)}), 200


@projects_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_project(id):
    user_id = get_jwt_identity()
    project = Project.query.get_or_404(id)

    if project.user_id != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    db.session.delete(project)
    db.session.commit()

    return jsonify({"message": "Project deleted"}), 200
