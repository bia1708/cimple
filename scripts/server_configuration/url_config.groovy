import jenkins.model.JenkinsLocationConfiguration

// Configure the jenkins server URL (default is http://localhost:8080)
jlc = GlobalConfiguration.all().getInstance(JenkinsLocationConfiguration.class)
jlc.setUrl("http://127.0.0.1:8080/") 
jlc.save() 