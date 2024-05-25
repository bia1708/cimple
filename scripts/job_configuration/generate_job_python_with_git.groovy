                        pipelineJob("${{REPO_NAME}}"){{
                            properties {{
                                githubProjectUrl("${{REPO}}")
                            }}
                            triggers {{
                                githubPush()
                            }}
                            environmentVariables {{
                                env('REPO', "${{REPO}}")
                                env('REPO_NAME', "${{REPO_NAME}}")
                            }}
                            definition {{
                                cps {{
                                    sandbox()
                                    script("""
        void setCommitBuildStatus(String backrefLink, String commitSha) {{
            echo env.REPO
            step([
                \\$class: "GitHubCommitStatusSetter",
                reposSource: [\\$class: "ManuallyEnteredRepositorySource", url: "\\${{env.REPO}}"],
                commitShaSource: [\\$class: 'ManuallyEnteredShaSource', sha: "\\${{commitSha}}"],
                errorHandlers: [[\\$class: "ChangingBuildStatusErrorHandler", result: "UNSTABLE"]],
                statusBackrefSource: [\\$class: "ManuallyEnteredBackrefSource", backref: "\\${{backrefLink}}"],
                statusResultSource: [\\$class: 'DefaultStatusResultSource']
            ]);
        }}


        pipeline {{
            agent any

            stages {{
                stage("Checkout") {{
                    steps {{
                        script {{
                            try {{
                                def scmVars = checkout([
                                    \\$class: 'GitSCM', branches: [[name: '*/main']],
                                    extensions: [[\\$class: 'RelativeTargetDirectory', relativeTargetDir: "\\${{WORKSPACE}}"]],
                                    userRemoteConfigs: [[credentialsId: "git_pat_\\${{REPO_NAME}}", url: "\\$REPO"]]
                                ])
                                env.GIT_COMMIT = scmVars.GIT_COMMIT
                            }} catch (Exception e) {{
                                echo 'Main branch not found, trying master branch...'
                                def scmVars = checkout([
                                    \\$class: 'GitSCM', branches: [[name: '*/master']],
                                    extensions: [[\\$class: 'RelativeTargetDirectory', relativeTargetDir: "\\${{WORKSPACE}}"]],
                                    userRemoteConfigs: [[credentialsId: "git_pat_\\${{REPO_NAME}}", url: "\\$REPO"]]
                                ])
                                env.GIT_COMMIT = scmVars.GIT_COMMIT
                            }}
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
                    withCredentials([usernamePassword(credentialsId: "git_pat_\\${{REPO_NAME}}", usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD'), usernamePassword(credentialsId: "jenkins_token", usernameVariable: 'JENKINS_USER', passwordVariable: 'JENKINS_API_TOKEN')]) {{
                        script {{
                            env.CONSOLE_OUTPUT = "\\${{env.BUILD_URL}}consoleText"
                            sh \'\'\'
                                #!/bin/bash
                                wget --auth-no-challenge --user=\\$JENKINS_USER --password=\\$JENKINS_API_TOKEN -O consoleOutput \\${{CONSOLE_OUTPUT}}
                                cat consoleOutput | grep -vi pipeline > output.txt
                                echo \\$PASSWORD > git_token
                                gh auth login --with-token < git_token
                                export GIST_PATH=\\$(gh gist create -d "Build \\$BUILD_TAG console output" output.txt | grep -o 'https://[^\"]*')

                                # Add GIST_PATH to the list of Environmental Variables
                                if [ "\\$(cat properties_file.props | grep GIST_PATH)" = "" ]; then
                                    echo "GIST_PATH=\\$GIST_PATH" >> properties_file.props
                                else
                                    sed -i "s,GIST_PATH=.*,GIST_PATH=\\$GIST_PATH," properties_file.props
                                fi
                                cat properties_file.props
                            \'\'\'
                            def props = readProperties file: 'properties_file.props'
                            env.NEW_GIST = props.GIST_PATH
                            echo "\\${{NEW_GIST}}, \\${{GIT_COMMIT}}, \\${{REPO}}"
                            setCommitBuildStatus("\\${{NEW_GIST}}", env.GIT_COMMIT)
                        }}
                    }}
                }}
            }}
        }}""")
                                }}
                            }}
                        }}