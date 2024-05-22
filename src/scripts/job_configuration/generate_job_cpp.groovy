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
                            // if (fileExists('CMakeLists.txt')) {{
                            //     // Use CMake to build the project
                            //     sh \'\'\'
                            //         mkdir -p build
                            //         cd build
                            //         cmake ..
                            //         make
                            //     \'\'\'
                            // }} else if (fileExists('Makefile')) {{
                            //     // Use Makefile to build the project
                            //     sh 'make'
                            // }} else {{
                            //     // Use g++ to build the project directly
                            //     sh 'g++ -o output *.cpp'
                            // }}
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
                            // if (fileExists('CMakeLists.txt')) {{
                            //     // Use CTest for testing if using CMake
                            //     sh \'\'\'
                            //         cd build
                            //         ctest
                            //     \'\'\'
                            // }} else if (fileExists('Makefile')) {{
                            //     // Assume the Makefile has a 'test' target
                            //     sh 'make test'
                            // }} else {{
                            //     // Run tests directly if not using CMake or Makefile
                            //     sh './output'
                            // }}
                        }}
                    }}
                }}
            }}
            post {{
                always {{
                    // Archive any test results and build artifacts
                    archiveArtifacts artifacts: '**/build/**', allowEmptyArchive: true
                    junit '**/build/test-reports/*.xml'
                }}
            }}
        }}""")
                                }}
                            }}
                        }}