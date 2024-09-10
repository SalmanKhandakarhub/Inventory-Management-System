pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Application') {
            steps {
                script {
                    sh '''BUILD_ID=dontKillMe nohup python3 main.py > app.log 2>&1 &
                    echo $! > flask_app.pid'''
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
            sh 'cat app.log'
            // script {
            //     if (fileExists('flask_app.pid')) {
            //         def pid = readFile('flask_app.pid').trim()
            //         sh "kill ${pid} || true"
            //     }
            // }
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
