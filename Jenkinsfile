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
                    echo "$GIT_LOCAL_BRANCH"
                    dockerImage = docker.build(registry + ":$GIT_LOCAL_BRANCH", "-f ${dockerFile} .")
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