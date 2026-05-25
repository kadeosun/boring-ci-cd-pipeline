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
