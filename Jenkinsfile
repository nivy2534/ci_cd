pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        IMAGE_NAME = "nivy2534/ci_cd:v1"
        DOCKER_REGISTRY = "https://registry.hub.docker.com"
    }

    stages {
        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/nivy2534/ci_cd.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $IMAGE_NAME .'
                    sh 'docker tag $IMAGE_NAME nivy2534/ci_cd:latest'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credential',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push $IMAGE_NAME'
                    sh 'docker push nivy2534/ci_cd:latest'
                }
            }
        }

        stage('Deploy MySQL') {
            steps {
                withKubeConfig([credentialsId: 'kubeconfig']) {
                    sh '''
                        echo "Deploying MySQL infrastructure..."
                        kubectl apply -f k8s/mysql-secret.yaml
                        kubectl apply -f k8s/mysql-pv.yaml
                        kubectl apply -f k8s/mysql-pvc.yaml
                        kubectl apply -f k8s/mysql-deployment.yaml
                        kubectl apply -f k8s/mysql-service.yaml
                        
                        echo "Waiting for MySQL to be ready..."
                        kubectl wait --for=condition=ready pod -l app=mysql --timeout=300s
                    '''
                }
            }
        }

        stage('Deploy Task App') {
            steps {
                withKubeConfig([credentialsId: 'kubeconfig']) {
                    sh '''
                        echo "Deploying Task App..."
                        if kubectl get deployment task-app -n default > /dev/null 2>&1; then
                            echo "Updating existing deployment..."
                            kubectl set image deployment/task-app task-app-container=$IMAGE_NAME -n default
                            kubectl rollout status deployment/task-app -n default --timeout=300s
                        else
                            echo "Creating new deployment..."
                            kubectl apply -f k8s/deployment.yaml
                            kubectl apply -f k8s/service.yaml
                            kubectl wait --for=condition=available --timeout=300s deployment/task-app -n default
                        fi
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                withKubeConfig([credentialsId: 'kubeconfig']) {
                    sh '''
                        echo "Checking deployment status..."
                        kubectl get deployments -n default
                        kubectl get pods -n default -l app=task-app
                        kubectl get svc -n default
                        
                        echo "Checking service endpoint..."
                        NODEPORT=$(kubectl get svc python-app-service -n default -o jsonpath='{.spec.ports[0].nodePort}')
                        echo "Task App is accessible at port: $NODEPORT"
                    '''
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout'
        }

        success {
            echo 'Pipeline executed successfully!'
        }

        failure {
            echo 'Pipeline failed! Check logs for more details.'
        }
    }
}
