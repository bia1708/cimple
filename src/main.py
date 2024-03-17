from service.configurator import Configurator
from service.job_configurator import Job_Configurator


if __name__ == '__main__':
    config = Configurator()
    # config.perform_fresh_install("bia", "1234")
    # config.connect_to_existing_jenkins("bia", "1234", "http://localhost:8080")
    print(config.get_current_server())
    # config.install_plugins()
    # config.enable_proxy()
    job_config = Job_Configurator()
    job_config.init_repo("cimple", "bia1708", "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")