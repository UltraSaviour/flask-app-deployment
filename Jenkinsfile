pipeline {
    agent any

    environment {
        VENV_PATH = "${WORKSPACE}/venv"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/UltraSaviour/flask-app-deployment.git'
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip --break-system-packages
                pip install -r requirements.txt --break-system-packages
                '''
            }
        }

        stage('Deploy Flask App') {
            steps {
                sh '''
                echo Copying files to app directory...
                sudo cp -r Jenkinsfile __pycache__ app.py nohup.out requirements.txt venv /root/flask_app/

                echo Restarting SystemD service...
                sudo systemctl daemon-reexec
                sudo systemctl restart flask_app
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                echo "Checking Flask app health..."
                curl -f http://localhost:5000 || exit 1
                '''
            }
        }
    }

    post {
        failure {
            echo '❌ Deployment failed. Please check logs.'
        }
        success {
            echo '✅ Deployment successful.'
        }
    }
}
