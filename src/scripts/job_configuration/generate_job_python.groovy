                        pipelineJob("${{REPO_NAME}}"){{
                            environmentVariables {{
                                env('REPO', "${{REPO}}")
                                env('REPO_NAME', "${{REPO_NAME}}")
                                propertiesFile("properties_file.props")
                            }}
                            definition {{
                                cps {{
                                    sandbox()
                                    script("""
        pipeline {{
            agent any

            stages {{
                stage("Checkout") {{
                    steps {{
                        script {{
                            def scmVars = checkout([
                                \\$class: 'GitSCM', branches: [[name: '*/main']],
                                extensions: [[\\$class: 'RelativeTargetDirectory', relativeTargetDir: "\\${{WORKSPACE}}"],],
                                userRemoteConfigs: [[credentialsId: "git_pat_\\${{REPO_NAME}}", url: "\\$REPO"]]
                            ])
                            env.GIT_COMMIT = scmVars.GIT_COMMIT
                        }}
                    }}
                }}

                stage("Build") {{
                    steps {{
                        script {{
                            withPythonEnv('python3') {{
                                sh \'\'\'
                                    #!/bin/bash
                                    if [ "\\$(find . -name 'Makefile*')" != "" ]; then
                                        make install
                                    elif [ "\\${{REQUIREMENTS}}" == "true" ]; then
                                        pip install -r requirements.txt
                                    fi
                                \'\'\'
                                // if (env.REQUIREMENTS == "true" ) {{
                                //     sh 'pip install -r requirements.txt'
                                // }}
                            }}
                        }}
                    }}
                }}

                stage('Test') {{
                    steps {{
                        script {{
                            withPythonEnv('python3') {{
                                sh 'python3 -m pytest --html=pytest_report.html --self-contained-html'
                            }}
                        }}
                    }}
                }}
            }}
            post {{
                always {{
                    withPythonEnv('python3') {{
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
                    }}
                }}
            }}
        }}""")
                                }}
                            }}
                        }}