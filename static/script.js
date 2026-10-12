// ============================================================
// TaskTrack – Frontend Logic
// Communicates with the Flask REST API (no external libraries)
// ============================================================

const API = "/api/tasks";

// ── DOM references ────────────────────────────────────────────
const form       = document.getElementById("task-form");
const titleInput = document.getElementById("task-title");
const descInput  = document.getElementById("task-desc");
const taskList   = document.getElementById("task-list");
const emptyMsg   = document.getElementById("empty-msg");
const formError  = document.getElementById("form-error");
const countTotal     = document.getElementById("count-total");
const countPending   = document.getElementById("count-pending");
const countCompleted = document.getElementById("count-completed");

// ── Fetch & render all tasks ──────────────────────────────────
async function loadTasks() {
  try {
    const res  = await fetch(API);
    const data = await res.json();
    renderSummary(data.summary);
    renderTasks(data.tasks);
  } catch (err) {
    console.error("Failed to load tasks:", err);
  }
}

// ── Update summary cards ──────────────────────────────────────
function renderSummary({ total, pending, completed }) {
  countTotal.textContent     = total;
  countPending.textContent   = pending;
  countCompleted.textContent = completed;
}

// ── Render task cards ─────────────────────────────────────────
function renderTasks(tasks) {
  // Remove old task items (keep the empty-msg element)
  document.querySelectorAll(".task-item").forEach(el => el.remove());

  if (tasks.length === 0) {
    emptyMsg.style.display = "block";
    return;
  }
  emptyMsg.style.display = "none";

  // Render newest first
  [...tasks].reverse().forEach(task => {
    const item = document.createElement("div");
    item.className = `task-item${task.status === "completed" ? " completed" : ""}`;
    item.dataset.id = task.id;

    const isCompleted = task.status === "completed";

    item.innerHTML = `
      <span class="task-badge ${isCompleted ? "badge-completed" : "badge-pending"}">
        ${isCompleted ? "✓ Done" : "⏳ Pending"}
      </span>
      <div class="task-body">
        <div class="task-title">${escapeHtml(task.title)}</div>
        ${task.description ? `<div class="task-desc">${escapeHtml(task.description)}</div>` : ""}
        <div class="task-meta">Added: ${task.created_at}</div>
      </div>
      <div class="task-actions">
        <button
          class="btn ${isCompleted ? "btn-toggle-completed" : "btn-toggle-pending"}"
          onclick="toggleTask(${task.id})"
          title="Toggle status"
        >
          ${isCompleted ? "↩ Undo" : "✓ Complete"}
        </button>
        <button
          class="btn btn-delete"
          onclick="deleteTask(${task.id})"
          title="Delete task"
        >
          🗑 Delete
        </button>
      </div>
    `;
    taskList.appendChild(item);
  });
}

// ── Add task ──────────────────────────────────────────────────
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  formError.textContent = "";

  const title = titleInput.value.trim();
  const description = descInput.value.trim();

  if (!title) {
    formError.textContent = "⚠ Please enter a task title.";
    titleInput.focus();
    return;
  }

  try {
    const res = await fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, description }),
    });

    if (!res.ok) {
      const err = await res.json();
      formError.textContent = "⚠ " + (err.error || "Could not add task.");
      return;
    }

    // Clear inputs on success
    titleInput.value = "";
    descInput.value  = "";
    titleInput.focus();
    await loadTasks();
  } catch (err) {
    formError.textContent = "⚠ Network error. Is the server running?";
    console.error(err);
  }
});

// ── Toggle task status ────────────────────────────────────────
async function toggleTask(id) {
  try {
    await fetch(`${API}/${id}`, { method: "PUT" });
    await loadTasks();
  } catch (err) {
    console.error("Toggle failed:", err);
  }
}

// ── Delete task ───────────────────────────────────────────────
async function deleteTask(id) {
  if (!confirm("Delete this task?")) return;
  try {
    await fetch(`${API}/${id}`, { method: "DELETE" });
    await loadTasks();
  } catch (err) {
    console.error("Delete failed:", err);
  }
}

// ── Utility: prevent XSS ─────────────────────────────────────
function escapeHtml(str) {
  const div = document.createElement("div");
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
}

// ── Initialise ────────────────────────────────────────────────
loadTasks();
