import os
import importlib
import logging
import json

import yaml

from .config import create_config, Config
from .decorators import try_except_wrapper
from .log_config import LOGGER_NAME
from .module import Module
from .scenario import Scenario, ScenarioData
from .metaclasses import Singleton


class Constants:
    MODULES = 'modules'
    MODULE = 'module'
    DATA = 'data'
    QUESTION_TYPE = 'question_type'
    MODULES_DIR = 'modules_dir'
    SCENARIOS_DIR = 'scenarios_dir'


class DataLoader(metaclass=Singleton):
    __user_config = None
    __user_configs_file = 'config.yaml'

    __default_modules_dir = 'modules'
    __default_scenarios_dir = 'scenarios'
    modules = {}
    scenarios = {}

    def __init__(self):
        self.logger = logging.getLogger(LOGGER_NAME)
        self.load_config()
        self.load_modules()
        self.load_scenarios()

    @property
    def modules_dir(self):
        m_dir = self.get_config_param(Constants.MODULES_DIR)
        if m_dir is None:
            self.set_config_param(Constants.MODULES_DIR, self.__default_modules_dir)
            return self.__default_modules_dir
        return m_dir

    @property
    def scenarios_dir(self):
        sc_dir = self.get_config_param(Constants.SCENARIOS_DIR)
        if sc_dir is None:
            self.set_config_param(Constants.SCENARIOS_DIR, self.__default_scenarios_dir)
            return self.__default_scenarios_dir
        return sc_dir

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
        self.save_config()

    # endregion

    # region Module
    def load_modules(self):
        self.modules.clear()
        if not os.path.isdir(self.modules_dir):
            self.logger.warning('Modules directory not found')
            return

        mod_cfg = self.get_config_param(Constants.MODULES)
        if mod_cfg is None:
            mod_cfg = Config(Constants.MODULES)
            self.__user_config.add(mod_cfg)

        mods = mod_cfg.get_children()
        for m_dir in os.listdir(self.modules_dir):
            mod = Module(m_dir)
            mod.enable_changed += lambda b: self.on_enabled_changed(mod.name, b)
            self.modules[m_dir] = mod

            mod_status = mod_cfg.get_param(m_dir)
            if mod_status is None or mod_status is True:
                self.activate_module(m_dir)

    @try_except_wrapper
    def activate_module(self, mod_name):
        mods = self.get_config_param(Constants.MODULES)
        mods.set_param(mod_name, True)

        mod_init = importlib.import_module(f'{self.modules_dir}.{mod_name}.init').Init()
        mod = self.modules.get(mod_name)
        if mod is None:
            raise Exception('Module not registered')
        mod.is_enabled = True
        mod.init = mod_init

    def deactivate_module(self, mod_name):
        mods = self.get_config_param(Constants.MODULES)
        mods.set_param(mod_name, False)
        mod = self.modules.get(mod_name)
        if mod is None:
            raise Exception('Module not registered')
        mod.is_enabled = False
        mod.init = None

    def on_enabled_changed(self, mod_name, value):
        self.logger.debug(f'Status {mod_name} changed to {value}')
        self.activate_module(mod_name) if value \
            else self.deactivate_module(mod_name)
        self.save_config()

    def get_init(self, mod_name):
        return self.modules.get(mod_name).init

    # endregion

    @try_except_wrapper
    def load_scenarios(self):
        self.scenarios.clear()
        sc_dir = self.scenarios_dir
        if not os.path.isdir(sc_dir):
            raise NotADirectoryError('Scenario directory not found')

        for f in os.listdir(sc_dir):
            self.__load_scenario(os.path.join(sc_dir, f))

    @try_except_wrapper
    def __load_scenario(self, file):
        with open(file, 'r', encoding='utf-8') as reader:
            content = json.load(reader)

        scenario_name = os.path.basename(file).split('.')[0]
        req_mods = []
        sc_data = []
        for bl in content:
            mod_name = bl[Constants.MODULE]
            mod_init = self.get_init(mod_name)
            if mod_init is None:
                self.logger.warning(f'Module {mod_name} not found')
                continue

            req_mods.append(mod_name)
            lazy_init = lambda: mod_init.deserialize_block(bl[Constants.DATA])
            sc_data.append(ScenarioData(mod_name, bl[Constants.QUESTION_TYPE], lazy_init))

        scenario = Scenario(scenario_name, required_modules=req_mods, scenario_data=sc_data)
        self.scenarios[scenario_name] = scenario
