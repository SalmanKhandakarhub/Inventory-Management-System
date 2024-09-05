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
            parallel {
                stage('Run Flask App') {
                    steps {
                        sh '''
                        nohup python3 main.py > app.log 2>&1 &
                        '''
                    }
                }
                // Other parallel stages can be defined here
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
