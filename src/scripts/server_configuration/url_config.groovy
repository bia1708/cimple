import jenkins.model.JenkinsLocationConfiguration

jlc = GlobalConfiguration.all().getInstance(JenkinsLocationConfiguration.class)
jlc.setUrl("http://127.0.0.1:8080/") 
jlc.save() 