from importlib import resources
import json

def cfg_item(*items):
    """
    Retrieves a configuration item from a nested configuration structure.

    Args:
        *items (str): A sequence of keys representing the path to the desired configuration item.

    Returns:
        The value of the configuration item specified by the provided keys.

    Raises:
        KeyError: If any of the keys do not exist in the configuration.
    """
    data = Config.get_instance().data
    for key in items:
        data = data[key]
    return data


class Config:
    """
    Singleton class to handle the loading and accessing of configuration data.

    Attributes
    ----------
    data : dict
        The configuration data loaded from the JSON file.

    Methods
    -------
    get_instance():
        Returns the singleton instance of the Config class.
    """

    __instance = None

    @staticmethod
    def get_instance():
        """
        Returns the singleton instance of the Config class. If the instance does not exist, it is created.

        Returns:
            Config: The singleton instance of the Config class.
        """
        if Config.__instance is None:
            Config()
        return Config.__instance

    def __init__(self):
        """
        Initializes the Config class by loading the configuration data from a JSON file. Ensures only one instance
        of the class exists.
        """
        if Config.__instance is None:
            Config.__instance = self

            file_path = resources.files("shmup.assets.config").joinpath('config.json')
            with resources.as_file(file_path) as config_data__path:
                with open(config_data__path) as file:
                    self.data = json.load(file)
        else:
            raise Exception("There Can Be Only One Config!!!")
