
node {{
    stage("test") {{
        script {{
            sh 'printenv'
        }}
    }}
}}