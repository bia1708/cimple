from service.configurator import Configurator


if __name__ == '__main__':
    config = Configurator("")
    # config.connect_to_existing_jenkins("bia", "1234", "http://localhost:8080")
    print(config.get_current_server())
    
    