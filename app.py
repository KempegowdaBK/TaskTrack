"""
TaskTrack - Smart Task Management System
A simple Flask web app to manage tasks with a modern dashboard.
"""

from flask import Flask, jsonify, request, render_template
from datetime import datetime

app = Flask(__name__)

# In-memory task storage (no database required)
tasks = []
next_id = 1  # Auto-increment ID counter


def get_task_by_id(task_id):
    """Return the task dict matching task_id, or None if not found."""
    return next((t for t in tasks if t["id"] == task_id), None)


# ── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the main dashboard page."""
    return render_template("index.html")


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Return all tasks and summary counts as JSON."""
    total = len(tasks)
    completed = sum(1 for t in tasks if t["status"] == "completed")
    pending = total - completed
    return jsonify({
        "tasks": tasks,
        "summary": {
            "total": total,
            "completed": completed,
            "pending": pending,
        }
    })


@app.route("/api/tasks", methods=["POST"])
def add_task():
    """Create a new task. Expects JSON body with 'title' and 'description'."""
    global next_id
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    title = (data.get("title") or "").strip()
    description = (data.get("description") or "").strip()

    if not title:
        return jsonify({"error": "Task title is required."}), 400

    task = {
        "id": next_id,
        "title": title,
        "description": description,
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    tasks.append(task)
    next_id += 1
    return jsonify(task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Toggle a task's status between 'pending' and 'completed'."""
    task = get_task_by_id(task_id)
    if task is None:
        return jsonify({"error": "Task not found."}), 404

    task["status"] = "completed" if task["status"] == "pending" else "pending"
    return jsonify(task)


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Remove a task permanently."""
    global tasks
    task = get_task_by_id(task_id)
    if task is None:
        return jsonify({"error": "Task not found."}), 404

    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Task deleted successfully."})


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
