// ============================================================
// TaskTrack - Declarative Jenkinsfile (Windows / bat commands)
// ============================================================
pipeline {
    agent any

    environment {
        // Name of the local virtual-environment folder in workspace
        VENV_DIR = "venv"
        // Destination directory for local demonstration deployment
        DEPLOY_DIR = "deployed_app"
    }

    stages {

        // ── 1. Checkout ──────────────────────────────────────────
        stage('Checkout') {
            steps {
                echo 'Stage 1: Checking out repository from SCM...'
                checkout scm
            }
        }

        // ── 2. Install Dependencies ──────────────────────────────
        stage('Install Dependencies') {
            steps {
                echo 'Stage 2: Setting up virtual environment and dependencies...'
                bat '''
                    @echo off
                    echo Checking Python installation...
                    python --version
                    IF ERRORLEVEL 1 (
                        echo ERROR: Python is not available in PATH.
                        exit /b 1
                    )

                    IF NOT EXIST "%VENV_DIR%\\Scripts\\activate.bat" (
                        echo Creating virtual environment in %VENV_DIR%...
                        python -m venv "%VENV_DIR%"
                        IF ERRORLEVEL 1 (
                            echo ERROR: Failed to create virtual environment.
                            exit /b 1
                        )
                    ) ELSE (
                        echo Existing virtual environment detected.
                    )

                    echo Upgrading pip and installing requirements...
                    call "%VENV_DIR%\\Scripts\\activate.bat"
                    python -m pip install --upgrade pip --quiet
                    pip install -r requirements.txt --quiet
                    IF ERRORLEVEL 1 (
                        echo ERROR: Failed to install requirements.
                        exit /b 1
                    )
                    echo Dependencies successfully installed.
                '''
            }
        }

        // ── 3. Test ──────────────────────────────────────────────
        stage('Test') {
            steps {
                echo 'Stage 3: Running automated test suite with pytest...'
                bat '''
                    @echo off
                    IF NOT EXIST "%VENV_DIR%\\Scripts\\activate.bat" (
                        echo ERROR: Virtual environment not found. Run Install Dependencies first.
                        exit /b 1
                    )

                    call "%VENV_DIR%\\Scripts\\activate.bat"
                    python -m pytest tests/ -v --tb=short
                    IF ERRORLEVEL 1 (
                        echo ERROR: One or more automated tests failed.
                        exit /b 1
                    )
                    echo All tests passed successfully.
                '''
            }
        }

        // ── 4. Build ─────────────────────────────────────────────
        stage('Build') {
            steps {
                echo 'Stage 4: Verifying project structure and writing build metadata...'
                bat '''
                    @echo off
                    echo Verifying required source files...
                    IF NOT EXIST app.py (
                        echo ERROR: app.py missing!
                        exit /b 1
                    )
                    IF NOT EXIST requirements.txt (
                        echo ERROR: requirements.txt missing!
                        exit /b 1
                    )
                    IF NOT EXIST templates\\index.html (
                        echo ERROR: templates\\index.html missing!
                        exit /b 1
                    )
                    IF NOT EXIST static\\style.css (
                        echo ERROR: static\\style.css missing!
                        exit /b 1
                    )
                    IF NOT EXIST static\\script.js (
                        echo ERROR: static\\script.js missing!
                        exit /b 1
                    )

                    echo All required files verified.
                    IF NOT EXIST build mkdir build

                    set COMMIT_ID=%GIT_COMMIT%
                    IF "%COMMIT_ID%"=="" set COMMIT_ID=LOCAL_OR_MANUAL_TRIGGER

                    echo TaskTrack Build Information > build\\build_info.txt
                    echo Build Date/Time : %DATE% %TIME% >> build\\build_info.txt
                    echo Git Commit      : %COMMIT_ID% >> build\\build_info.txt
                    echo Status          : Passed automated tests and verification >> build\\build_info.txt

                    type build\\build_info.txt
                '''
            }
        }

        // ── 5. Deploy ────────────────────────────────────────────
        stage('Deploy') {
            steps {
                echo 'Stage 5: Deploying application to local folder (demonstration)...'
                bat '''
                    @echo off
                    echo Preparing deployment directory: %DEPLOY_DIR%

                    REM Remove previous deployment to guarantee a clean, idempotent rerun
                    IF EXIST "%DEPLOY_DIR%" (
                        echo Cleaning previous deployment...
                        rmdir /s /q "%DEPLOY_DIR%"
                    )
                    mkdir "%DEPLOY_DIR%"

                    echo Copying application files...
                    copy /y app.py "%DEPLOY_DIR%\\" >nul
                    copy /y requirements.txt "%DEPLOY_DIR%\\" >nul
                    copy /y build\\build_info.txt "%DEPLOY_DIR%\\" >nul

                    xcopy templates "%DEPLOY_DIR%\\templates\\" /e /i /y /q >nul
                    xcopy static "%DEPLOY_DIR%\\static\\" /e /i /y /q >nul

                    echo Verifying deployed files...
                    IF NOT EXIST "%DEPLOY_DIR%\\app.py" (
                        echo ERROR: Deployment verification failed for app.py!
                        exit /b 1
                    )
                    IF NOT EXIST "%DEPLOY_DIR%\\templates\\index.html" (
                        echo ERROR: Deployment verification failed for templates!
                        exit /b 1
                    )
                    IF NOT EXIST "%DEPLOY_DIR%\\static\\style.css" (
                        echo ERROR: Deployment verification failed for static!
                        exit /b 1
                    )

                    echo.
                    echo ========================================================
                    echo   Deployment Complete (Local Demonstration)
                    echo   Target directory : %DEPLOY_DIR%
                    echo   To run deployed app : python %DEPLOY_DIR%\\app.py
                    echo ========================================================
                '''
            }
        }
    }

    // ── Post-build notifications ──────────────────────────────────
    post {
        success {
            echo 'SUCCESS: Pipeline finished successfully! TaskTrack is verified and deployed.'
        }
        failure {
            echo 'FAILURE: Pipeline failed. Check stage console logs for error details.'
        }
        always {
            echo 'Pipeline execution completed.'
        }
    }
}
