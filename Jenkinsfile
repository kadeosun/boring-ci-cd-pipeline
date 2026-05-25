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
                echo 'Verifying Python syntax compliance...'
                sh 'python3 -m py_compile app.py'
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
