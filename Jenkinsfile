pipeline {
    agent any

    environment {
        IMAGE_NAME = "nivy2534/ci_cd:v1"
    }

    stages {

        stage('Clone') {
            steps {
            		git branch: 'main', url: 'https://github.com/nivy2534/ci_cd.git'
		}
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
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
                }
            }
        }
	stage('Deploy to K8s') {
    		steps {
        		withKubeConfig([credentialsId: 'kubeconfig']) {
            		sh """
                	if kubectl get deployment task-app -n default > /dev/null 2>&1; then
                    		kubectl rollout restart deployment/task-app -n default
                	else
                    		kubectl apply -f deployment.yaml
                    		kubectl apply -f service.yaml
                	fi
            		"""
        		}
    		}
	}
    }
}
