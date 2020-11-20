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
                    builderImageName = registry + ":builder"
                    dockerImage = ''
                    if (env.BRANCH_NAME == 'qaw') {
                        docker.image(builderImageName).pull()
                        dockerImage = docker.build(dockerImageName, "-f build/Dockerfile.$BRANCH_NAME --cache-from $builderImageName .")
                    }
//                     if (env.BRANCH_NAME == 'qaw' || env.BRANCH_NAME == 'prod') {
//                         dockerImage = docker.build(dockerImageName, "-f build/Dockerfile.$BRANCH_NAME .")
//                     }
//                     else {
//                         dockerImage = docker.build(dockerImageName, "-f build/Dockerfile .")
//                     }

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
                        sh "docker rmi $dockerImageName"
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
}