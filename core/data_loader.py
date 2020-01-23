import os
import importlib

import yaml

from .module import Module
from .metaclasses import Singleton


class Constants:
    MODULES = 'modules'


class DataLoader(metaclass=Singleton):

    __user_configs = {}
    __user_configs_file = 'config.yaml'

    __modules_dir = 'modules'  # TODO move into config
    __scenarios_dir = 'scenarios'  # TODO move into config
    modules = []
    scenarios = []

    def __init__(self):
        self.load_config()
        self.load_modules()
        self.load_scenario_list()

    # region Config
    def load_config(self):
        if not os.path.exists(self.__user_configs_file):
            # TODO logging
            return
        with open(self.__user_configs_file, 'r') as file:
            self.__user_configs = yaml.load(file, yaml.FullLoader)

    def save_config(self):
        with open(self.__user_configs_file, 'w+') as file:
            yaml.dump(self.__user_configs, file)

    def get_config_param(self, param):  # TODO add 'param path'
        return self.__user_configs[param] \
            if param in self.__user_configs.keys() else None

    def set_config_param(self, param, value):
        self.__user_configs[param] = value
    # endregion

    # region Module
    def load_modules(self):
        if not os.path.isdir(self.__modules_dir):
            # TODO logging
            return

        if Constants.MODULES not in self.__user_configs:
            self.__user_configs[Constants.MODULES] = {}

        mods = self.get_config_param(Constants.MODULES)
        for d in os.listdir(self.__modules_dir):
            if d not in mods or mods[d] is True:
                self.activate_module(d)

    def activate_module(self, mod_name):
        mods = self.get_config_param(Constants.MODULES)
        mods[mod_name] = True

        mod_init = importlib.import_module(f'{self.__modules_dir}.{mod_name}')
        mod = next((m for m in self.modules if m.name == mod_name), None)
        if mod is None:
            mod = Module(mod_name, init=mod_init, is_enabled=True)
            self.modules.append(mod)
        mod.is_enabled = True
        mod.init = mod_init

    def deactivate_module(self, mod_name):
        mods = self.__user_configs[Constants.MODULES]
        mods[mod_name] = False
        mod = next((m for m in self.modules if m.name == mod_name), None)
        if mod is not None:
            # TODO logging
            mod.is_enabled = False
            mod.init = None
    # endregion

    def load_scenario_list(self):  # ?
        pass
