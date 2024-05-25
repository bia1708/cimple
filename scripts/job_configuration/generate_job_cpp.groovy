pipelineJob("${{REPO_NAME}}"){{
                            environmentVariables {{
                                env('REPO', "${{REPO}}")
                                env('REPO_NAME', "${{REPO_NAME}}")
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
                            sh \'\'\'
                                #!/bin/bash
                                if [ "\\$(find . -maxdepth 1 -name 'CMakeLists.txt')" != "" ]; then
                                    mkdir -p build
                                    cd build
                                    cmake ..
                                    make
                                elif [ "\\$(find . -maxdepth 1 -name 'Makefile*')" != "" ]; then
                                    make
                                else
                                    g++ -o output *.cpp
                                fi
                            \'\'\'
                        }}
                    }}
                }}

                stage('Test') {{
                    steps {{
                        script {{
                            sh \'\'\'
                                #!/bin/bash
                                if [ "\\$(find . -maxdepth 1 -name 'CMakeLists.txt')" != "" ]; then
                                    cd build
                                    ctest
                                elif [ "\\$(find . -maxdepth 1 -name 'Makefile*')" != "" ]; then
                                    make test
                                else
                                    ./output
                                fi
                            \'\'\'
                        }}
                    }}
                }}
            }}
            post {{
                always {{
                    // Archive any test results and build artifacts
                    archiveArtifacts artifacts: '**/build/**', allowEmptyArchive: true
                }}
            }}
        }}""")
                                }}
                            }}
                        }}