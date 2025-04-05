pipeline {
    agent any

    environment {
        FLASK_APP_DIR = '/root/flask_app'
        SERVICE_NAME = 'flask_app'
        APP_PORT = '5000'
    }

    stages {
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
                    sleep 3
                    curl -f http://localhost:${APP_PORT}/ || echo "Flask app is not responding!"
                '''
            }
        }
    }

    post {
        failure {
            echo "❌ Deployment failed. Please check logs."
        }
        success {
            echo "✅ Flask app deployed successfully!"
        }
    }
}
