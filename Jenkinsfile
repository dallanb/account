pipeline {
    environment {
        githubCredential = 'github'
        container = 'account'
        registry = "dallanbhatti/account"
        registryCredential = 'dockerhub'
    }
    agent any
    stages {
        stage('Build') {
            steps {
                script {
                    dockerImageName = registry + ":$BRANCH_NAME"
                    dockerImage = ''
                    if (env.BRANCH_NAME == 'qaw') {
                        docker.image(dockerImageName).pull()
                        dockerImage = docker.build(dockerImageName, "-f build/Dockerfile.$BRANCH_NAME --cache-from $dockerImageName .")
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    if (dockerImage) {
                        docker.withRegistry( '', registryCredential ) {
                            dockerImage.push()
                        }
                    }
                }
            }
        }
        stage('Clean') {
            steps {
                script {
                    if (dockerImage) {
                        sh "docker image prune -f"
                    }
                }
            }
        }
        stage('Recreate') {
            steps {
                script {
                    if (dockerImage) {
                        httpRequest url: 'http://192.168.0.100:9000/hooks/redeploy', contentType: 'APPLICATION_JSON', httpMode: 'POST', requestBody: """
                            {
                                "project": {
                                    "name": "$container",
                                    "env": "$BRANCH_NAME"
                                }
                            }
                        """
                    }
                }
            }
        }
    }
    post {
        success {
          slackSend (color: '#00FF00', message: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
        }

        failure {
          slackSend (color: '#FF0000', message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
        }
    }
}