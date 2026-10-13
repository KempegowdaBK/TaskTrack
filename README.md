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

## ☁️ Connecting & Deploying to AWS EC2 / Temporary Cloud Server

The `Jenkinsfile` Deploy stage automatically supports deploying to an **AWS EC2 instance** or any remote Linux server using native Windows OpenSSH (`scp` and `ssh`).

### Option 1: AWS EC2 Instance Deployment (Recommended for Cloud Demonstration)

#### Step 1: Launch an AWS EC2 Instance
1. Log into your [AWS Management Console](https://aws.amazon.com/console/) and navigate to **EC2**.
2. Click **Launch Instance**:
   - **Name**: `TaskTrack-Server`
   - **OS**: Ubuntu 24.04 LTS (Free Tier eligible).
   - **Instance Type**: `t2.micro` or `t3.micro`.
   - **Key pair**: Create or select an existing key pair (e.g. `tasktrack-key.pem`). Download and save the `.pem` file to your laptop (e.g. `C:\keys\tasktrack-key.pem`).
3. Under **Network Settings / Security Group**, allow incoming traffic for:
   - **SSH** (Port `22`) from `Anywhere (0.0.0.0/0)` or your IP.
   - **Custom TCP** (Port `5000`) from `Anywhere (0.0.0.0/0)`.
4. Click **Launch Instance** and note the **Public IPv4 address** (e.g., `3.110.120.45`).

#### Step 2: One-Time Server Setup on AWS
Connect once to your EC2 instance from PowerShell:
```powershell
ssh -i "C:\keys\tasktrack-key.pem" ubuntu@<YOUR-EC2-PUBLIC-IP>
```
Run this single command on the server to prepare Python and the destination folder:
```bash
sudo apt update && sudo apt install -y python3 python3-pip python3-venv
mkdir -p ~/tasktrack
```

#### Step 3: Configure Jenkins for Automated AWS Deployment
In your Jenkins dashboard:
1. Go to **Manage Jenkins** ➔ **System** ➔ Scroll down to **Global properties** ➔ Check **Environment variables**.
2. Add the following variables:
   - `AWS_EC2_HOST` = `<YOUR-EC2-PUBLIC-IP>` (e.g. `3.110.120.45`)
   - `AWS_EC2_USER` = `ubuntu`
   - `AWS_SSH_KEY`  = `C:\keys\tasktrack-key.pem`
3. Click **Save**.

Now, whenever you push code to GitHub:
1. Jenkins detects the change automatically via **SCM Polling**.
2. Runs all unit tests.
3. Packages the build.
4. Uses `scp` to copy files to your AWS server.
5. Uses `ssh` to restart the Flask application on AWS.
6. Your updated app is immediately live at: **`http://<YOUR-EC2-PUBLIC-IP>:5000`**!

---

### Option 2: Free Instant Public Server (No AWS Credit Card Needed)

If you don't have an AWS account or want a completely free temporary public URL for your demo:

#### A. Free Cloud Hosting via Render.com:
1. Go to [https://render.com](https://render.com) and create a free account with GitHub.
2. Click **New +** ➔ **Web Service** ➔ Connect your `TaskTrack` GitHub repository.
3. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app || python app.py`
4. Click **Deploy**. Render gives you a public URL (e.g. `https://tasktrack.onrender.com`) that automatically redeploys on every GitHub push!

#### B. Instant Public URL via ngrok:
To make your deployed app accessible on the internet instantly:
```powershell
ngrok http 5000
```
This gives you a public URL like `https://xyz.ngrok-free.app` that proxies to your live application!

---

## 🌐 Solving the Local Jenkins vs GitHub Webhook Challenge

### The Problem
- **GitHub** is a cloud service on the public internet.
- **Jenkins** is running on your local laptop at `http://localhost:8082` (inside your local network / behind Wi-Fi NAT and Windows Firewall).
- When you push code, GitHub cannot directly send an HTTP webhook to `http://localhost:8082` because `localhost` refers to GitHub's own server, not your machine.

---

### Solution A: SCM Polling (Recommended for College Demo — 100% Reliable & Zero Setup)

Instead of GitHub pushing an inbound webhook to your laptop (which is blocked by NAT/Firewall), **Jenkins on your laptop initiates outbound polling to GitHub** on a schedule.

#### How it works:
1. Jenkins runs `pollSCM('* * * * *')` (every minute).
2. Because your laptop can access GitHub via standard HTTPS (outbound), this works behind any college Wi-Fi, home router, or mobile hotspot without opening ports.
3. Jenkins asks GitHub: *"Has the commit SHA on branch `main` changed?"*
4. As soon as you run `git push`, Jenkins automatically detects the new commit within 60 seconds and triggers:
   `Checkout ➔ Install Dependencies ➔ Run Pytest ➔ Build ➔ Deploy`

#### How to enable it in Jenkins:
1. In your **TaskTrack-CI-CD** job configuration in Jenkins:
2. Under **Build Triggers**, check **Poll SCM**.
3. In the **Schedule** box, enter:
   ```cron
   * * * * *
   ```
   *(Checks GitHub every minute for new commits).*
4. Click **Save**.
5. Test it: Push any change to GitHub, and within 1 minute Jenkins automatically triggers a build and executes all 20 tests!

---

### Solution B: Webhook Tunneling via ngrok (For Real-Time Webhook Demonstration)

If your examiner specifically requests a real-time GitHub Webhook event payload:

1. Download **ngrok** from [https://ngrok.com](https://ngrok.com) (or run `winget install ngrok`).
2. Start an HTTP tunnel to your local Jenkins port:
   ```cmd
   ngrok http 8082
   ```
3. Copy the public forwarding URL provided by ngrok (e.g. `https://a1b2-c3d4.ngrok-free.app`).
4. Go to your GitHub repository:
   - Navigate to **Settings** ➔ **Webhooks** ➔ **Add webhook**
   - **Payload URL**: `https://a1b2-c3d4.ngrok-free.app/github-webhook/`
     *(Ensure the trailing slash `/` is included)*
   - **Content type**: `application/json`
   - **Which events**: Select **Just the push event**
   - Click **Add webhook**
5. Now, whenever you run `git push`, GitHub sends an instant webhook to the ngrok URL, which forwards it to `localhost:8082`, immediately triggering your pipeline!

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
