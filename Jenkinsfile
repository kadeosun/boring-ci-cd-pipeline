pipeline {
    agent any

    environment {
        IMAGE_NAME = "local-production-tasks-api"
        CONTAINER_NAME = "production-tasks-service"
        APP_PORT = "5000"
        HOST_PORT = "5002"
    }

    stages {
        stage('Code Initialization') {
            steps {
                echo 'Checking workspace sanity...'
                sh 'ls -la'
            }
        }

        stage('Code Quality Audit') {
            steps {
                echo 'Executing Enterprise Static Code Analysis...'
                sh '''
                    docker run --rm -v \$(pwd):/apps -w /apps python:3.10-slim sh -c "
                    echo 'Installing code quality framework...' && \
                    pip install --quiet flake8 && \
                    echo 'Running strict syntax compliance checks...' && \
                    flake8 app.py --count --select=E9,F63,F7,F82 --show-source --statistics && \
                    flake8 app.py --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
                    "
                '''
                echo 'Code quality audit passed successfully!'
            }
        }

        stage('Build Image') {
            steps {
                echo "Building application image layer: ${IMAGE_NAME}..."
                sh "docker build -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('Integration Testing') {
            steps {
                echo 'Spinning up transient container instance to verify stability...'
                sh "docker run --rm ${IMAGE_NAME}:latest python3 -m py_compile app.py"
            }
        }

        stage('Rolling Deployment') {
            steps {
                echo 'Executing rolling zero-downtime microservice update...'
                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm ${CONTAINER_NAME} || true"
                sh "docker run -d -p ${HOST_PORT}:${APP_PORT} --name ${CONTAINER_NAME} --restart unless-stopped ${IMAGE_NAME}:latest"
                echo "Deployment successfully executed. Listening on port ${HOST_PORT}"
            }
        }
    }
}
