pipelineJob("${{REPO_NAME}}"){{
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

        def fileExists(filePath) {{
            def file = new File(filePath)
            return file.exists()
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
                            // Check for Gradle build script
                            if (fileExists('build.gradle')) {{
                                sh './gradlew build'
                            }}
                            // Check for Ant build script
                            else if (fileExists('build.xml')) {{
                                sh 'ant build'
                            }}
                            // Check for Makefile
                            else if (fileExists('Makefile')) {{
                                sh 'make'
                            }}
                            // Default to Maven
                            else {{
                                sh 'mvn clean install'
                            }}
                        }}
                    }}
                }}

                stage('Test') {{
                    steps {{
                        script {{
                            // Check for Gradle test task
                            if (fileExists('build.gradle')) {{
                                sh './gradlew test'
                            }}
                            // Check for Ant junit task
                            else if (fileExists('build.xml')) {{
                                sh 'ant junit'
                            }}
                            // Default to maven
                            else {{
                                sh 'mvn test'
                            }}
                        }}
                    }}
                }}
            }}
            post {{
                always {{
                    archiveArtifacts artifacts: '**/target/*.jar', allowEmptyArchive: true
                    junit '**/target/surefire-reports/*.xml'
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