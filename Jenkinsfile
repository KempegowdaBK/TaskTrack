// ============================================================
// TaskTrack - Declarative Jenkinsfile (Windows / bat commands)
// ============================================================
pipeline {
    agent any

    environment {
        // Name of the local virtual-environment folder
        VENV_DIR = "venv"
        // Destination folder used as a "deploy" demonstration
        DEPLOY_DIR = "deployed_app"
    }

    stages {

        // ── 1. Checkout ──────────────────────────────────────────
        stage('Checkout') {
            steps {
                echo 'Stage 1 – Checking out source code...'
                checkout scm
            }
        }

        // ── 2. Install Dependencies ──────────────────────────────
        stage('Install Dependencies') {
            steps {
                echo 'Stage 2 – Creating virtual environment and installing packages...'
                bat '''
                    IF NOT EXIST %VENV_DIR% (
                        python -m venv %VENV_DIR%
                    )
                    CALL %VENV_DIR%\\Scripts\\activate.bat
                    python -m pip install --upgrade pip --quiet
                    pip install -r requirements.txt --quiet
                '''
            }
        }

        // ── 3. Test ──────────────────────────────────────────────
        stage('Test') {
            steps {
                echo 'Stage 3 – Running automated tests with pytest...'
                bat '''
                    CALL %VENV_DIR%\\Scripts\\activate.bat
                    pytest tests/ -v --tb=short
                '''
            }
        }

        // ── 4. Build ─────────────────────────────────────────────
        stage('Build') {
            steps {
                echo 'Stage 4 – Preparing build artefacts...'
                bat '''
                    IF NOT EXIST build MKDIR build
                    echo TaskTrack build - %DATE% %TIME% > build\\build_info.txt
                    echo Commit: %GIT_COMMIT% >> build\\build_info.txt
                    echo All tests passed. Application is ready. >> build\\build_info.txt
                    TYPE build\\build_info.txt
                '''
            }
        }

        // ── 5. Deploy ────────────────────────────────────────────
        stage('Deploy') {
            steps {
                echo 'Stage 5 – Deploying application to local folder (demo)...'
                bat '''
                    REM Clean previous deployment so the stage is safe to rerun
                    IF EXIST %DEPLOY_DIR% RMDIR /S /Q %DEPLOY_DIR%
                    MKDIR %DEPLOY_DIR%

                    REM Copy application files
                    COPY app.py %DEPLOY_DIR%\\
                    COPY requirements.txt %DEPLOY_DIR%\\
                    XCOPY templates %DEPLOY_DIR%\\templates\\ /E /I /Q
                    XCOPY static %DEPLOY_DIR%\\static\\ /E /I /Q
                    COPY build\\build_info.txt %DEPLOY_DIR%\\

                    echo.
                    echo ================================================
                    echo  Deployment complete!
                    echo  Files copied to: %DEPLOY_DIR%
                    echo  To run: python %DEPLOY_DIR%\\app.py
                    echo ================================================
                '''
            }
        }
    }

    // ── Post-build actions ────────────────────────────────────────
    post {
        success {
            echo '✅ Pipeline finished successfully! TaskTrack is ready.'
        }
        failure {
            echo '❌ Pipeline failed. Check the stage logs above for details.'
        }
        always {
            echo 'Pipeline execution complete.'
        }
    }
}
