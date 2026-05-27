stage('Rolling Deployment') {
            steps {
                script {
                    echo "Deploying version ${IMAGE_TAG}..."
                    // We explicitly point to the workspace path and the file
                    sh """
                        docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -v /var/jenkins_home/workspace/boring-app-final-pipeline:/app \
                        -w /app \
                        docker/compose:latest -f docker-compose.yml up -d
                    """
                }
            }
        }
