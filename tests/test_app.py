"""
TaskTrack – Automated Tests
Run with: pytest tests/ -v
"""

import json
import pytest

# Import the Flask app and reset shared state before each test
import app as app_module
from app import app


@pytest.fixture(autouse=True)
def reset_state():
    """Clear in-memory task list and reset the ID counter before every test."""
    app_module.tasks = []
    app_module.next_id = 1
    yield
    # Teardown: clean up again after the test
    app_module.tasks = []
    app_module.next_id = 1


@pytest.fixture
def client():
    """Create a Flask test client configured for testing."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ── Helper ────────────────────────────────────────────────────

def add_task(client, title="Test Task", description="Test description"):
    """POST a task and return the response."""
    return client.post(
        "/api/tasks",
        data=json.dumps({"title": title, "description": description}),
        content_type="application/json",
    )


# ── Tests ─────────────────────────────────────────────────────

class TestIndex:
    """Test the main dashboard route."""

    def test_index_returns_200(self, client):
        """GET / should return HTTP 200 and the dashboard HTML."""
        response = client.get("/")
        assert response.status_code == 200
        # Check that key HTML elements are present
        assert b"TaskTrack" in response.data

    def test_index_content_type_is_html(self, client):
        """The dashboard route should return HTML content."""
        response = client.get("/")
        assert "text/html" in response.content_type


class TestGetTasks:
    """Tests for GET /api/tasks."""

    def test_get_tasks_returns_200(self, client):
        """GET /api/tasks should return HTTP 200."""
        response = client.get("/api/tasks")
        assert response.status_code == 200

    def test_get_tasks_empty_at_start(self, client):
        """Task list should be empty and all counts zero on a fresh start."""
        response = client.get("/api/tasks")
        data = response.get_json()
        assert data["tasks"] == []
        assert data["summary"]["total"] == 0
        assert data["summary"]["pending"] == 0
        assert data["summary"]["completed"] == 0

    def test_get_tasks_reflects_added_task(self, client):
        """After adding a task, GET /api/tasks should list it."""
        add_task(client, title="My Task")
        response = client.get("/api/tasks")
        data = response.get_json()
        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["title"] == "My Task"


class TestAddTask:
    """Tests for POST /api/tasks."""

    def test_add_task_returns_201(self, client):
        """Adding a valid task should return HTTP 201 Created."""
        response = add_task(client, title="New Task")
        assert response.status_code == 201

    def test_add_task_response_fields(self, client):
        """The created task should have the correct fields."""
        response = add_task(client, title="Build App", description="Use Flask")
        task = response.get_json()
        assert task["title"] == "Build App"
        assert task["description"] == "Use Flask"
        assert task["status"] == "pending"
        assert task["id"] == 1
        assert "created_at" in task

    def test_add_task_increments_id(self, client):
        """Each new task should receive a unique, incrementing ID."""
        r1 = add_task(client, title="Task 1")
        r2 = add_task(client, title="Task 2")
        assert r1.get_json()["id"] == 1
        assert r2.get_json()["id"] == 2

    def test_add_task_missing_title_returns_400(self, client):
        """Submitting a task without a title should return HTTP 400."""
        response = client.post(
            "/api/tasks",
            data=json.dumps({"description": "No title here"}),
            content_type="application/json",
        )
        assert response.status_code == 400
        assert "error" in response.get_json()

    def test_add_task_empty_title_returns_400(self, client):
        """Submitting a task with a blank title should return HTTP 400."""
        response = client.post(
            "/api/tasks",
            data=json.dumps({"title": "   "}),
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_add_task_non_json_returns_400(self, client):
        """Sending a non-JSON body should return HTTP 400."""
        response = client.post(
            "/api/tasks",
            data="not json at all",
            content_type="text/plain",
        )
        assert response.status_code == 400

    def test_summary_updates_after_add(self, client):
        """Summary counts should reflect newly added tasks."""
        add_task(client, title="T1")
        add_task(client, title="T2")
        data = client.get("/api/tasks").get_json()
        assert data["summary"]["total"] == 2
        assert data["summary"]["pending"] == 2
        assert data["summary"]["completed"] == 0


class TestUpdateTask:
    """Tests for PUT /api/tasks/<id> (toggle status)."""

    def test_toggle_pending_to_completed(self, client):
        """A pending task should become completed after toggle."""
        task_id = add_task(client, title="Toggle Me").get_json()["id"]
        response = client.put(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        assert response.get_json()["status"] == "completed"

    def test_toggle_completed_to_pending(self, client):
        """A completed task should revert to pending on second toggle."""
        task_id = add_task(client, title="Double Toggle").get_json()["id"]
        client.put(f"/api/tasks/{task_id}")           # pending → completed
        response = client.put(f"/api/tasks/{task_id}") # completed → pending
        assert response.get_json()["status"] == "pending"

    def test_toggle_nonexistent_task_returns_404(self, client):
        """Toggling a task that doesn't exist should return HTTP 404."""
        response = client.put("/api/tasks/999")
        assert response.status_code == 404

    def test_summary_reflects_completed_task(self, client):
        """Summary should update completed/pending counts after toggle."""
        task_id = add_task(client, title="Sum Task").get_json()["id"]
        client.put(f"/api/tasks/{task_id}")
        data = client.get("/api/tasks").get_json()
        assert data["summary"]["completed"] == 1
        assert data["summary"]["pending"] == 0


class TestDeleteTask:
    """Tests for DELETE /api/tasks/<id>."""

    def test_delete_task_returns_200(self, client):
        """Deleting an existing task should return HTTP 200."""
        task_id = add_task(client, title="Delete Me").get_json()["id"]
        response = client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        assert "message" in response.get_json()

    def test_delete_removes_task_from_list(self, client):
        """After deletion the task should no longer appear in GET /api/tasks."""
        task_id = add_task(client, title="Gone Task").get_json()["id"]
        client.delete(f"/api/tasks/{task_id}")
        tasks = client.get("/api/tasks").get_json()["tasks"]
        assert all(t["id"] != task_id for t in tasks)

    def test_delete_nonexistent_task_returns_404(self, client):
        """Deleting a task that doesn't exist should return HTTP 404."""
        response = client.delete("/api/tasks/999")
        assert response.status_code == 404

    def test_summary_updates_after_delete(self, client):
        """Total count should decrease after a task is deleted."""
        task_id = add_task(client, title="Count Me").get_json()["id"]
        client.delete(f"/api/tasks/{task_id}")
        data = client.get("/api/tasks").get_json()
        assert data["summary"]["total"] == 0
