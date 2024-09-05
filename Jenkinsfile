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
                script {
                    // Run Flask app in the background and save the process ID
                    sh '''
                    python3 main.py > app.log 2>&1
                    echo $! > flask_app.pid
                    '''
                }
            }
        }
        stage('Post-deployment') {
            steps {
                echo "Deployment successful"
                // Optional: Add a sleep to allow time for the application to start
                sleep(time: 10, unit: 'SECONDS')
            }
        }
    }
    post {
        always {
            echo 'Checking logs...'
            sh 'cat app.log'
            // Clean up Flask process if needed
            script {
                if (fileExists('flask_app.pid')) {
                    def pid = readFile('flask_app.pid').trim()
                    sh "kill -9 ${pid} || true"
                }
            }
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
