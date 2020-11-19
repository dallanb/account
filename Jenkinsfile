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
                    dockerImage = docker.build(registry + ":qaw", "-f ${dockerFile} .")
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