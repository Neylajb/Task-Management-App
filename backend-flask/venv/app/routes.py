from flask import Blueprint, jsonify, request, abort
from .models import Task, db, TaskStatus

bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@bp.route("/", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@bp.route("/<int:id>", methods=["GET"])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict())

@bp.route("/", methods=["POST"])
def create_task():
    try:
        data = request.get_json()
        
        # Check if required fields are present
        if not data or 'title' not in data:
            return jsonify({"error": "Title is required"}), 400
        
        new_task = Task(
            title=data['title'],
            description=data.get('description'),  # Use .get() to handle missing fields
            status=data.get('status', 'PENDING')   # Default to 'PENDING' if status not provided
        )
        
        db.session.add(new_task)
        db.session.commit()
        
        return jsonify(new_task.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@bp.route("/<int:id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.json
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.status = data.get("status", task.status)
    db.session.commit()
    return jsonify(task.to_dict())

@bp.route("/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})
