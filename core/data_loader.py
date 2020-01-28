import os
import importlib
import logging
import json

import yaml

from .config import create_config, Config
from .decorators import try_except_wrapper
from .log_config import LOGGER_NAME
from .module import Module
from .scenario import Scenario
from .metaclasses import Singleton


class Constants:
    MODULES = 'modules'
    MODULE = 'module'
    DATA = 'data'


class DataLoader(metaclass=Singleton):

    __user_config = None
    __user_configs_file = 'config.yaml'

    __modules_dir = 'modules'  # TODO move into config
    __scenarios_dir = 'scenarios'  # TODO move into config
    modules = {}
    scenarios = {}

    def __init__(self):
        self.logger = logging.getLogger(LOGGER_NAME)
        self.load_config()
        self.load_modules()
        self.load_scenarios()

    # region Config
    def load_config(self):
        if not os.path.exists(self.__user_configs_file):
            self.logger.warning('Config file not found')
            return
        with open(self.__user_configs_file, 'r') as file:
            self.__user_config = create_config(yaml.load(file, yaml.FullLoader))

    def save_config(self):
        with open(self.__user_configs_file, 'w+') as file:
            yaml.dump(self.__user_config.get_dict(), file)

    @try_except_wrapper
    def get_config_param(self, param):
        return self.__user_config.get_param(param)

    def set_config_param(self, param, value):
        self.__user_config.set_param(param, value)
    # endregion

    # region Module
    def load_modules(self):
        if not os.path.isdir(self.__modules_dir):
            self.logger.warning('Modules directory not found')
            return

        mod_cfg = self.get_config_param(Constants.MODULES)
        if mod_cfg is None:
            mod_cfg = Config(Constants.MODULES)
            self.__user_config.add(mod_cfg)

        mods = mod_cfg.get_children()
        for d in os.listdir(self.__modules_dir):
            m = mod_cfg.get_param(d)
            if m is None or m is True:
                self.activate_module(d)

    @try_except_wrapper
    def activate_module(self, mod_name):
        mods = self.get_config_param(Constants.MODULES)
        mods.set_param(mod_name, True)

        mod_init = importlib.import_module(f'{self.__modules_dir}.{mod_name}.init').Init()
        mod = self.modules.get(mod_name)
        if mod is None:
            mod = Module(mod_name, init=mod_init, is_enabled=True)
            self.modules[mod_name] = mod
        mod.is_enabled = True
        mod.init = mod_init

    def deactivate_module(self, mod_name):
        mods = self.get_config_param(Constants.MODULES)
        mods.set_param('mod_name', False)
        mod = self.modules.get(mod_name)
        if mod is None:
            self.logger.warning('Module not found')
            return
        mod.is_enabled = False
        mod.init = None
    # endregion

    def load_scenarios(self):
        if not os.path.isdir(self.__scenarios_dir):
            self.logger.warning('Scenarios directory not found')
            return

        for f in os.listdir(self.__scenarios_dir):
            self.__load_scenario(os.path.join(self.__scenarios_dir, f))

    @try_except_wrapper
    def __load_scenario(self, file):
        with open(file, 'r', encoding='utf-8') as reader:
            content = json.load(reader)

        scenario_name = os.path.basename(file).split('.')[0]
        req_mods = []
        sc_data = {}
        for bl in content:
            mod_name = bl[Constants.MODULE]
            mod = self.modules.get(mod_name)
            if mod is None:
                self.logger.warning('Module not found')
                continue
            data = mod.init.deserialize_block(bl[Constants.DATA])

            req_mods.append(mod_name)
            sc_data[mod_name] = data  # TODO temp

        scenario = Scenario(scenario_name, required_modules=req_mods, data=sc_data)
        self.scenarios[scenario_name] = scenario
