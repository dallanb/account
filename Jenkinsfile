pipeline {

    environment {
        githubCredential = 'github'
        registry = "dallanbhatti/account"
        registryCredential = 'dockerhub'
        dockerImage = ''
        dockerFile = 'build/Dockerfile.qaw'
    }
    agent any
    stages {
        stage('Build') {
            steps {
                script {
                    echo "$BRANCH_NAME"
                    dockerImage = docker.build(registry + ":$BRANCH_NAME", "-f ${dockerFile} .")
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                    }
                }
            }
        }
        stage('Clean') {
            steps {
                sh "docker rmi $registry:qaw"
            }
        }
    }
}