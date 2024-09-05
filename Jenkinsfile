pipeline {
    agent any

    environment {
        VENV_PATH = "${WORKSPACE}/venv"
    }

    stages {
        stage('Preparation') {
            steps {
                script {
                    // Create virtual environment if it doesn't exist
                    if (!fileExists("${VENV_PATH}/bin/activate")) {
                        sh 'python3 -m venv venv'
                    }
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                bash -c "
                # Activate virtual environment
                source ${VENV_PATH}/bin/activate
                
                # Install project dependencies from requirements.txt
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Application') {
            steps {
                sh '''
                bash -c "
                # Activate virtual environment
                source ${VENV_PATH}/bin/activate
                
                # Run Flask app
                nohup python main.py > app.log 2>&1 &
                '''
            }
        }

        stage('Post-deployment') {
            steps {
                echo "Deployment successful"
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Application deployed successfully!'
        }
        failure {
            echo 'Deployment failed.'
        }
    }
}
