pipeline {
    agent any

    environment {
        IMAGE_NAME = "ml-project"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '. venv/bin/activate && python train.py'
            }
        }

        stage('Test') {
            steps {
                sh '. venv/bin/activate && pytest -v test_model.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:${BUILD_NUMBER} .'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker rm -f ml-app || true
                docker run -d --name ml-app -p 5000:5000 $IMAGE_NAME:${BUILD_NUMBER}
                '''
            }
        }
    }

    post {
        success { echo 'Pipeline succeeded' }
        failure { echo 'Pipeline failed' }
    }
}
