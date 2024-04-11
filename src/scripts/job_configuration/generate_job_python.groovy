pipelineJob("${REPO_NAME}"){
    environmentVariables {
        propertiesFile("properties_file.props")
    }
    definition {
        cps {
            sandbox()
            script('''
pipeline {
    agent any

    stages {
        stage("Set Environment") {
            steps {
                    script {
                    def props = readProperties  file:"${WORKSPACE}/properties_file.props"
                    env.REPO= props["REPO"]
                    env.REPO_NAME = props["REPO_NAME"]
                    env.REQUIREMENTS = props["REQUIREMENTS"]
                    env.INSTRUCTIONS = props["INSTRUCTIONS"]
                }
            }
        }

        stage("Checkout") {
            steps {
                checkout([
                    $class: 'GitSCM', branches: [[name: '*/main']],
                    extensions: [[$class: 'RelativeTargetDirectory', relativeTargetDir: "${WORKSPACE}"],],
                    userRemoteConfigs: [[credentialsId: "git_pat_${REPO_NAME}", url: "$REPO"]]
                ])
            }
        }

        stage("Build") {
            steps {
                script {
                    if (env.REQUIREMENTS == "true" ) {
                        sh 'pip install -r requirements.txt'
                    }
                }
            }
        }
    }
}''')
        }
    }
}