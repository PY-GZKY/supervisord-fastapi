import abc
import os


class ConfigProtocol(abc.ABC):
    pass


class ConfigYAML(ConfigProtocol):
    def __init__(self, config_file_path: str):
        self.config_file_path = config_file_path


class ConfigJSON(ConfigProtocol):
    def __init__(self, config_file_path: str):
        self.config_file_path = config_file_path


def setup_settings() -> ConfigProtocol:
    json_config = os.environ['CONFIG_FILE'].endswith('json')
    yaml_config = os.environ['CONFIG_FILE'].endswith(('yaml', 'yml'))

    if json_config:
        instantiated_config = ConfigJSON(os.environ['CONFIG_FILE'])
    elif yaml_config:
        instantiated_config = ConfigYAML(os.environ['CONFIG_FILE'])
    else:
        raise RuntimeError('variavel de ambiente CONFIG_FILE deve ser definida')

    return instantiated_config


settings = setup_settings()
