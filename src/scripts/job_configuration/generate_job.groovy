
pipelineJob("${REPO}"){
    definition {
        cps {
            script('''
                pipeline {
                    agent any

                    stages {
                        stage("test") {
                            steps {
                                    script {
                                    sh 'pwd && printenv'
                                }
                            }
                        }

                        stage('Checkout') {
                            steps {
                                checkout([
                                    $class: 'GitSCM', branches: [[name: '*/main']],
                                    extensions: [[$class: 'RelativeTargetDirectory', relativeTargetDir: "${WORKSPACE}"],],
                                    userRemoteConfigs: [[credentialsId: "git_pat_${REPO_NAME}", url: "$REPO"]]
                                ])
                            }
                        }
                    }
                }
            ''')
        }
    }
}