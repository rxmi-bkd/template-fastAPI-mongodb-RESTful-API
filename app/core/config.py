import sys
import yaml

CONFIG_PATH = "app/config.yaml"


def read_config(config_path: str) -> dict:
    """
    :param config_path: path to *.yaml file

    :return: dict
    """
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

            return config

    except FileNotFoundError:
        print(f"FileNotFoundError: No such file or directory: '{config_path}'")
        sys.exit(1)


def get_config() -> dict:
    config = read_config(CONFIG_PATH)

    return config


class Config:
    def __init__(self):
        self.config = get_config()

    def __getattr__(self, item):
        return self.config[item]


CONFIG = Config()
