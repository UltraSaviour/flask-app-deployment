pipeline {
    agent any

    environment {
        CONTAINER_ID = '101'
        DEST_DIR = '/root/flask_app'
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
                echo "Copying files to container..."
                sudo pct push ${CONTAINER_ID} Jenkinsfile ${DEST_DIR}/
                sudo pct push ${CONTAINER_ID} app.py ${DEST_DIR}/
                sudo pct push ${CONTAINER_ID} nohup.out ${DEST_DIR}/
                sudo pct push ${CONTAINER_ID} requirements.txt ${DEST_DIR}/
                sudo pct push ${CONTAINER_ID} venv ${DEST_DIR}/ --recursive

                echo "Restarting flask_app service inside container..."
                sudo pct exec ${CONTAINER_ID} -- systemctl daemon-reexec
                sudo pct exec ${CONTAINER_ID} -- systemctl restart flask_app
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
