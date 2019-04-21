""" Contains the config reader """

import yaml
import appdirs
import os


class Config:
    """ Config file object. """
    # get the config directory
    config_dir = appdirs.user_config_dir("nthsubbot")
    # get the config file path
    config_path = os.path.join(config_dir, "config.yaml")

    # read config
    @classmethod
    def read(cls):
        """
        Read config.
        :return: the config that was read
        """
        try:
            # open the config file
            with open(cls.config_path, 'r') as config_file:
                # load the config
                config = yaml.safe_load(config_file)
        except FileNotFoundError:
            # if the file doesn't exist, create config directory
            os.makedirs(cls.config_dir, exist_ok=True)
            # open config file
            with open(cls.config_path, 'w') as config_file:
                # make it empty
                yaml.safe_dump({}, config_file)
            return {}
        return config

    @classmethod
    def save(cls, config):
        """
        Saves the config.
        :param config: the config to save
        """
        # open the config file
        with open(cls.config_path, 'w') as config_file:
            # save it
            yaml.safe_dump(config, config_file)
