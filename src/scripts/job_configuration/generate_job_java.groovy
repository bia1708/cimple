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
                }}
            }}
        }}""")
                                }}
                            }}
                        }}