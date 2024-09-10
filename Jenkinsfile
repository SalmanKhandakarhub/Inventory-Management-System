pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                sh '. /venv/bin/activate && pip install --no-cache-dir -r requirements.txt'
            }
        }
        stage('Run Application') {
            steps {
                script {
                    sh '''
                    . /venv/bin/activate
                    BUILD_ID=dontKillMe nohup gunicorn -w 4 -b 0.0.0.0:9001 webapp:create_app > app.log 2>&1 &
                    echo $! > flask_app.pid
                    '''
                }
            }
        }
        stage('Post-deployment') {
            steps {
                echo "Deployment successful"
                sleep(time: 10, unit: 'SECONDS')
            }
        }
    }
    post {
        always {
            echo 'Checking logs...'
            sh 'cat app.log || echo "No logs found!"'
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
