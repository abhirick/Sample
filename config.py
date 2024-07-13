import os
import configparser


class Config:
    def __init__(self, config_file="config.ini", env="default"):
        self.config = configparser.ConfigParser()
        print(self.config)
        self.config.read(config_file)
        
        self.env = env

    def get(self, key):
        try:
            return self.config[self.env][key]
        except KeyError:
            return self.config["default"][key]


def get_config(env=None):
    if env is None:
        env = os.getenv("FLASK_ENV", "default")
    return Config(env=env)
