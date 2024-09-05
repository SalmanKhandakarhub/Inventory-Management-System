pipeline {
    agent any
    
    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                # Install project dependencies from requirements.txt
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Application') {
            steps {
                sh '''
                # Run Flask app
                python3 main.py > app.log 2>&1
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
            echo 'Checking logs...'
            sh 'cat app.log'
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
