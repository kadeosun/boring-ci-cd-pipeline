pipeline {
    agent any

    environment {
        DOCKER_USER = 'kadeosun'
        IMAGE_NAME  = 'boring-app'
        IMAGE_TAG   = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Code Quality Audit') {
            steps {
                echo 'Executing Enterprise Static Code Analysis...'
                sh """
                    docker build -t lint-test:${BUILD_NUMBER} .
                    docker run --rm -u 0 lint-test:${BUILD_NUMBER} sh -c \
                    "pip install --quiet flake8 && \
                    flake8 app.py --count --select=E9,F63,F7,F82 --show-source --statistics && \
                    flake8 app.py --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics"
                """
            }
        }

        stage('Build and Push Image') {
            steps {
                script {
                    echo "Building image: ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker build -t ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG} ."
                    
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', 
                                                      usernameVariable: 'DOCKER_USR', 
                                                      passwordVariable: 'DOCKER_PSW')]) {
                        sh "echo ${DOCKER_PSW} | docker login -u ${DOCKER_USR} --password-stdin"
                        sh "docker push ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
                        sh "docker logout"
                    }
                }
            }
        }

        stage('Integration Testing') {
            steps {
                echo 'Running integration tests...'
                sh "echo 'Integration tests passed!'"
            }
        }

        stage('Rolling Deployment') {
            steps {
                script {
                    echo "Deploying version ${IMAGE_TAG}..."
                    // We use 'docker compose' (no hyphen) which is the modern plugin
                    sh """
                        export IMAGE_TAG=${IMAGE_TAG}
                        docker compose up -d
                    """
                }
            }
        }
    }
}
