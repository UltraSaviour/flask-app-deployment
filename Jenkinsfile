pipeline {
    agent any

    environment {
        CONTAINER_ID = '101'
        DEST_DIR = '/root/flask_app'
        CONTAINER_PORT = '5000'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/UltraSaviour/flask-app-deployment.git'
            }
        }

        stage('Push Code to Container') {
            steps {
                sh '''
                echo "Creating destination directory in container..."
                sudo pct exec $CONTAINER_ID -- mkdir -p $DEST_DIR

                echo "Pushing files to container..."
                for file in Jenkinsfile app.py requirements.txt; do
                    sudo pct push $CONTAINER_ID $file $DEST_DIR/
                done
                '''
            }
        }

        stage('Install Dependencies in Container') {
            steps {
                sh '''
                echo "Installing Python dependencies inside container..."
                sudo pct exec $CONTAINER_ID -- bash -c "cd $DEST_DIR && python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt"
                '''
            }
        }

        stage('Restart Flask App Service') {
            steps {
                sh '''
                echo "Restarting Flask systemd service in container..."
                sudo pct exec $CONTAINER_ID -- systemctl daemon-reexec
                sudo pct exec $CONTAINER_ID -- systemctl restart flask_app
                '''
            }
        }

        stage('Health Check') {
            steps {
                script {
                    echo "Fetching container IP..."
                    def containerIP = sh(
                        script: "sudo pct exec $CONTAINER_ID -- hostname -I | awk '{print $1}'",
                        returnStdout: true
                    ).trim()

                    echo "Performing health check at http://${containerIP}:${CONTAINER_PORT} ..."
                    sh "curl -f http://${containerIP}:${CONTAINER_PORT} || exit 1"
                }
            }
        }
    }

    post {
        always {
            echo "Fetching last 50 logs from flask_app service inside the container..."
            sh 'sudo pct exec 101 -- journalctl -u flask_app --no-pager -n 50'
        }

        failure {
            echo '❌ Deployment failed. Please check logs.'
        }

        success {
            echo '✅ Deployment successful.'
        }
    }
}
