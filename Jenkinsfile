pipeline {
  agent any

  environment {
    IMAGE = "saniya7110/ml-api-2"
    TAG   = "${env.BUILD_NUMBER}"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Test') {
      steps {
        sh '''
          cd api
          python3 -m venv venv
          . venv/bin/activate
          pip install -r requirements.txt
          pytest -q
        '''
      }
    }

    stage('Build Image') {
      steps {
        sh 'docker build -t $IMAGE:$TAG -t $IMAGE:latest ./api'
      }
    }

    stage('Push Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub',
                         usernameVariable: 'DH_USER',
                         passwordVariable: 'DH_PASS')]) {
          sh '''
            echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
            docker push $IMAGE:$TAG
            docker push $IMAGE:latest
          '''
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        sh '''
          kubectl set image deployment/ml-api ml-api=$IMAGE:$TAG
          kubectl rollout status deployment/ml-api --timeout=180s
          kubectl get pods
        '''
      }
    }
  }

  post {
    success { echo "Deployed $IMAGE:$TAG successfully" }
    failure { echo "Pipeline failed - check the console output" }
  }
}
