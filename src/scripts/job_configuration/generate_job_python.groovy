pipelineJob("${REPO_NAME}"){
    environmentVariables {
        env('REPO', "${REPO}")
        env('REPO_NAME', "${REPO_NAME}")
        propertiesFile("properties_file.props")
    }
    definition {
        cps {
            sandbox()
            script('''
void setCommitBuildStatus(String backrefLink, String commitSha) {
    echo env.REPO
    step([
        $class: "GitHubCommitStatusSetter",
        reposSource: [$class: "ManuallyEnteredRepositorySource", url: "${env.REPO}"],
        commitShaSource: [$class: 'ManuallyEnteredShaSource', sha: "${commitSha}"],
        errorHandlers: [[$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
        statusBackrefSource: [$class: "ManuallyEnteredBackrefSource", backref: "${backrefLink}"],
        statusResultSource: [$class: 'DefaultStatusResultSource']
    ]);
}


pipeline {
    agent any

    stages {
        stage("Set Environment") {
            steps {
                    script {
                    def props = readProperties  file:"${WORKSPACE}/properties_file.props"
                    echo env.REPO
                    env.REPO= props["REPO"]
                    env.REPO_NAME = props["REPO_NAME"]
                    env.REQUIREMENTS = props["REQUIREMENTS"]
                    env.INSTRUCTIONS = props["INSTRUCTIONS"]
                }
            }
        }

        stage("Checkout") {
            steps {
                script {
                    def scmVars = checkout([
                        $class: 'GitSCM', branches: [[name: '*/main']],
                        extensions: [[$class: 'RelativeTargetDirectory', relativeTargetDir: "${WORKSPACE}"],],
                        userRemoteConfigs: [[credentialsId: "git_pat_${REPO_NAME}", url: "$REPO"]]
                    ])
                    env.GIT_COMMIT = scmVars.GIT_COMMIT
                }
            }
        }

        stage("Build") {
            steps {
                script {
                    withPythonEnv('python3') {
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
        }

        stage('Test') {
            steps {
                script {
                    withPythonEnv('python3') {
                        sh 'python3 -m pytest --html=pytest_report.html --self-contained-html'
                    }
                }
            }
        }
    }
    post {
        always {
            withPythonEnv('python3') {
                archiveArtifacts 'pytest_report.html'
                publishHTML(target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'pytest_report.html',
                    reportName: 'pytest Output',
                    reportTitles: ''
                ])
            }
            withCredentials([usernamePassword(credentialsId: "git_pat_${REPO_NAME}", usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                script {
                    env.CONSOLE_LOG = Jenkins.getInstance().getItemByFullName(env.JOB_NAME).getBuildByNumber(Integer.parseInt(env.BUILD_NUMBER)).logFile
                    sh \'\'\'
                        #!/bin/bash
                        cp $CONSOLE_LOG output.md
                        echo $PASSWORD > git_token
                        gh auth login --with-token < git_token
                        export GIST_PATH=$(gh gist create -d "Build $BUILD_TAG console output" output.md | grep -o 'https://[^\"]*')

                        # Add GIST_PATH to the list of Environmental Variables
                        if [ "$(cat properties_file.props | grep GIST_PATH)" = "" ]; then
                            echo "GIST_PATH=$GIST_PATH" >> properties_file.props
                        else
                            sed -i "s,GIST_PATH=.*,GIST_PATH=$GIST_PATH," properties_file.props
                        fi
                        cat properties_file.props
                    \'\'\'
                    def props = readProperties file: 'properties_file.props'
                    env.NEW_GIST = props.GIST_PATH
                    echo "${NEW_GIST}, ${GIT_COMMIT}, ${REPO}"
                    setCommitBuildStatus("${NEW_GIST}", env.GIT_COMMIT)
                }
            }
        }
    }
}''')
        }
    }
}