
node {{
    stage("test") {{
        script {{
            sh 'pwd && printenv'
        }}
    }}
}}