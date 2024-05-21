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
                                    if [ "\\$(find . -maxdepth 1 -name 'Makefile*')" != "" ]; then
                                        make install
                                    elif [ "\\${{REQUIREMENTS}}" == "true" ]; then
                                        pip install -r requirements.txt
                                    elif [ "\\$(find . -name 'setup.py')" != "" ] || [ "\\$(find . -name 'pyproject.toml')" != "" ]; then
                                        python3 -m pip install .
                                    fi
                                \'\'\'
                            }}
                        }}
                    }}
                }}

                stage('Test') {{
                    steps {{
                        script {{
                            withPythonEnv('python3') {{
                                sh \'\'\'
                                    #!/bin/bash
                                    pip install pytest pytest-html
                                    if [ "\\$(find . -maxdepth 1 -name 'test*')" != "" ]; then
                                        if [ "\\$(find . -name 'runtests.py')" != "" ]; then
                                            cd tests
                                            ./runtests.py
                                        else
                                            python3 -m pytest --html=pytest_report.html --self-contained-html
                                        fi
                                    else
                                        echo "No tests found!"
                                    fi
                                \'\'\'
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