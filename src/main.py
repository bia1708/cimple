from service.configurator import Configurator


if __name__ == '__main__':
    config = Configurator()
    # config.perform_fresh_install("bia", "1234")
    # config.connect_to_existing_jenkins("bia", "1234", "http://localhost:8080")
    print(config.get_current_server())
    # config.install_plugins()
    config.enable_proxy()
    