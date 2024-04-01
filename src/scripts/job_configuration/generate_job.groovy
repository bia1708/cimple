
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
                    }
                }
            ''')
        }
    }
}