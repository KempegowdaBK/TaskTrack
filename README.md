# TaskTrack – Smart Task Management System with Automated CI/CD

> **College Demo Project** · Python Flask · Jenkins · pytest · GitHub

A beginner-friendly web application that lets you create, track, complete, and delete tasks from a modern dashboard, with a full automated CI/CD pipeline powered by Jenkins.

---

## 📁 Project Structure

```
TaskTrack/
├── app.py                 # Flask application (REST API + dashboard)
├── requirements.txt       # Python dependencies (Flask, pytest)
├── Jenkinsfile            # Declarative CI/CD pipeline (Windows)
├── README.md              # This file
├── .gitignore             # Excludes venv, cache, secrets
├── templates/
│   └── index.html         # Dashboard HTML
├── static/
│   ├── style.css          # Responsive styles
│   └── script.js          # Vanilla JavaScript
└── tests/
    └── test_app.py        # Automated pytest test suite (18+ tests)
```

---

## ✨ Features

| Feature | Description |
|---|---|
| ➕ Add tasks | Provide a title and optional description |
| 📋 View tasks | All tasks displayed newest-first |
| ✅ Toggle status | Switch between **pending** and **completed** |
| 🗑 Delete tasks | Remove any task permanently |
| 📊 Live summary | Total / Pending / Completed counts update automatically |
| 📱 Responsive UI | Works on desktop and mobile |

---

## 🛠 Prerequisites

| Tool | Version | Download |
|---|---|---|
| Python | 3.8 or later | https://python.org/downloads |
| Git | Any recent version | https://git-scm.com/download/win |
| Jenkins | LTS | https://jenkins.io/download |

> **Check your Python version:** Open PowerShell and run `python --version`

---

## 🚀 Quick Start (Windows)

### 1 — Clone the repository
```powershell
git clone https://github.com/<your-username>/TaskTrack.git
cd TaskTrack
```

### 2 — Create and activate a virtual environment
```powershell
python -m venv venv
venv\Scripts\activate
```
> Your prompt will change to `(venv)` when the environment is active.

### 3 — Install dependencies
```powershell
pip install -r requirements.txt
```

### 4 — Run the application
```powershell
python app.py
```

### 5 — Open in your browser
Navigate to **http://127.0.0.1:5000**

### 6 — Stop the server
Press `Ctrl + C` in the terminal.

---

## 🧪 Running Tests

```powershell
# Make sure the virtual environment is active first
venv\Scripts\activate

pytest tests/ -v
```

**Expected output:**
```
tests/test_app.py::TestIndex::test_index_returns_200             PASSED
tests/test_app.py::TestIndex::test_index_content_type_is_html   PASSED
tests/test_app.py::TestGetTasks::test_get_tasks_returns_200      PASSED
... (18+ tests)

================ 18 passed in X.XXs ================
```

---

## 🔗 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Dashboard page |
| `GET` | `/api/tasks` | List all tasks + summary |
| `POST` | `/api/tasks` | Create a new task |
| `PUT` | `/api/tasks/<id>` | Toggle task status |
| `DELETE` | `/api/tasks/<id>` | Delete a task |

**POST /api/tasks — Request body:**
```json
{
  "title": "Complete assignment",
  "description": "Chapter 5 – due Friday"
}
```

---

## ⚙️ Jenkins CI/CD Setup (Windows)

### Prerequisites
1. [Download and install Jenkins](https://www.jenkins.io/download/) on Windows (LTS version recommended).
2. Complete initial setup and ensure the standard **Pipeline** and **Git** plugins are installed.
3. **Important for Windows Jenkins:** Ensure Python 3.8+ and Git are in the **System PATH** (accessible to the Jenkins service user):
   - In PowerShell or Command Prompt, verify:
     ```cmd
     python --version
     git --version
     ```
   - If Jenkins runs as a Windows Service (`Local System`), restart the Jenkins service after modifying System PATH.

### Create the Pipeline Job

1. Open Jenkins in your browser at **http://localhost:8080**
2. Click **New Item** → enter `TaskTrack` → select **Pipeline** → click **OK**
3. In the Pipeline configuration:
   - **Definition**: Select `Pipeline script from SCM`
   - **SCM**: Select `Git`
   - **Repository URL**: `https://github.com/KempegowdaBK/TaskTrack.git` (or your repository URL)
   - **Branch Specifier**: `*/main`
   - **Script Path**: `Jenkinsfile`
4. Click **Save**, then click **Build Now**

### Pipeline Architecture & Stages

The pipeline uses **Declarative Pipeline syntax** and executes native **Windows `bat` commands**:

```
[Checkout] ➔ [Install Dependencies] ➔ [Test] ➔ [Build] ➔ [Deploy]
```

| Stage | Batch Execution (`bat`) | Details & Safety Features |
|---|---|---|
| **1. Checkout** | `checkout scm` | Checks out source from GitHub into the Jenkins workspace. |
| **2. Install Dependencies** | `python -m venv venv`<br>`call venv\Scripts\activate.bat`<br>`pip install -r requirements.txt` | • Checks that Python is accessible.<br>• Creates `venv` only if not already present.<br>• Activates virtual environment and installs/updates packages.<br>• Safe to rerun anytime. |
| **3. Test** | `python -m pytest tests/ -v --tb=short` | • Executes all 20 automated tests using Flask test client.<br>• Halts pipeline immediately if any test fails. |
| **4. Build** | Source verification & `type build\build_info.txt` | • Verifies presence of all required files (`app.py`, `templates/index.html`, etc.).<br>• Generates `build\build_info.txt` with build timestamp and Git commit ID. |
| **5. Deploy** | `rmdir /s /q deployed_app`<br>`copy` & `xcopy` | • **Idempotent and clean**: Cleans prior deployment folder before copying.<br>• Copies application files to `deployed_app/` (demonstration folder).<br>• Verifies deployed files are present. |

> **College Demo Tip:** To test the deployed application, navigate into the Jenkins workspace (or locally) and run:
> ```cmd
> python deployed_app\app.py
> ```

---

## 📌 Notes for College Demo

- **No database required** — tasks are stored in Python memory. They reset when the server restarts (perfect for a demo).
- **No Docker or paid services** — everything runs locally on Windows.
- **Security** — the `.gitignore` ensures `venv/`, `__pycache__/`, and `.env` are never committed.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is created for educational purposes as a college demonstration.
