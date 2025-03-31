from importlib import resources
import json

def cfg_item(*items):
    data = Config.get_instance().data
    for key in items:
        data = data[key]
    return data

class Config:

    __instance = None

    @staticmethod
    def get_instance():
        if Config.__instance is None:
            Config()
        return Config.__instance

    def __init__(self):
        if Config.__instance is None:
            Config.__instance = self

            file_path = resources.files("falling_letters.assets.config").joinpath('config.json')
            with resources.as_file(file_path) as config_data__path:
                with open(config_data__path) as file:
                    self.data = json.load(file)
        else:
            raise Exception("There Can Be Only One Config!!!")