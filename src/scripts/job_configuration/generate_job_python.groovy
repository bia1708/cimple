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
                    sh 'export PATH="$PATH:${WORKSPACE}/.local/lib/python$(python3 --version | awk "{print $2}" | cut -d "." -f 1,2)/site-packages"'
                    // env.PATH = "${env.PATH}:" + "${env.WORKSPACE}/.local/lib/python*"
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
                    sh \'\'\'
                        #!/bin/bash
                        if [ "$(find . -name 'Makefile*')" != "" ]; then
                            make install
                        elif [ "${REQUIREMENTS}" == "true" ]; then
                            pip install -r requirements.txt
                        fi
                    \'\'\'
                    // if (env.REQUIREMENTS == "true" ) {
                    //     sh 'pip install -r requirements.txt'
                    // }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    sh 'pytest  --html=pytest_report.html --self-contained-html'
                }
            }
        }
    }
}''')
        }
    }
}