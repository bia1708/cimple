import org.jenkinsci.plugins.github.config.GitHubPluginConfig
import org.jenkinsci.plugins.github.config.GitHubServerConfig

def github = jenkins.model.Jenkins.instance.getExtensionList(GitHubPluginConfig.class)[0]

def serverConfig = new GitHubServerConfig("gh_token")
serverConfig.setName("GITHUB_SERVER")
serverConfig.setManageHooks(false)

github.setConfigs([
  serverConfig,
])
github.save()