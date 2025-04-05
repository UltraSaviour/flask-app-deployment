pipeline {
    agent any

    environment {
        FLASK_APP_DIR = '/root/flask_app'  // Path where your app is deployed
        SERVICE_NAME = 'flask_app'         // Name of your SystemD service
        APP_PORT = '5000'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/UltraSaviour/flask-app-deployment.git'
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Deploy Flask App') {
            steps {
                sh '''
                    echo "Copying files to app directory..."
                    sudo cp -r * ${FLASK_APP_DIR}/

                    echo "Restarting SystemD service..."
                    sudo systemctl daemon-reexec
                    sudo systemctl restart ${SERVICE_NAME}
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    sleep 3  # give the app time to restart
                    curl -f http://localhost:${APP_PORT}/ || echo "Flask app is not responding!"
                '''
            }
        }
    }

    post {
        failure {
            echo "Pipeline failed."
        }
        success {
            echo "Deployment complete!"
        }
    }
}
