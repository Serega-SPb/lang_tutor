import os
import sys
import logging
import json

import yaml

from .config import create_config, Config
from .decorators import try_except_wrapper
from .log_config import LOGGER_NAME
from .module import Module
from .scenario import Scenario, ScenarioData
from .metaclasses import Singleton
from . import module_manager


class Constants:
    DEBUG_FLAG = '-d'
    LOCALE = 'locale'
    MODULES = 'modules'
    MODULE = 'module'
    DATA = 'data'
    QUESTION_TYPE = 'question_type'
    MODULES_DIR = 'modules_dir'
    SCENARIOS_DIR = 'scenarios_dir'
    OPTIONS_ENABLED_PARAM = 'ui.options_enabled'


class DataLoader(metaclass=Singleton):
    __user_config = None
    __user_configs_file = 'config.yaml'

    __default_modules_dir = 'modules'
    __default_scenarios_dir = 'scenarios'
    modules = {}
    scenarios = {}

    def __init__(self):
        self.logger = logging.getLogger(LOGGER_NAME)
        module_manager.get_module_dir = lambda: self.modules_dir
        self.load_config()
        self.load_modules()
        self.load_scenarios()
        self.is_debug = Constants.DEBUG_FLAG in sys.argv

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
        def init_module(mod_name, enb_status):
            mod = Module(mod_name, is_enabled=enb_status)
            mod.enable_changed += lambda n, b: self.on_mod_status_changed(mod_cfg, n, b)
            self.modules[mod_name] = mod

        self.modules.clear()
        mod_cfg = self.get_config_param(Constants.MODULES)
        if mod_cfg is None:
            mod_cfg = Config(Constants.MODULES)
            self.__user_config.add(mod_cfg)
        d_path = os.path.abspath(self.modules_dir)
        if not os.path.isdir(self.modules_dir):
            self.logger.warning('Modules directory not found')
        else:
            mods = mod_cfg.get_children()
            for m_dir in os.listdir(self.modules_dir):
                m_path = os.path.join(self.modules_dir, m_dir)
                m_dir = os.path.splitext(m_dir)[0]
                if not (os.path.isdir(m_path) or m_path.endswith('.zip')) or m_dir in self.modules:
                    continue
                status = mod_cfg.get_param(m_dir)
                init_module(m_dir, status)

        not_loaded = [name for name in mod_cfg.get_children().keys() if name not in self.modules]
        for name in not_loaded:
            init_module(name, mod_cfg.get_param(name))

    def on_mod_status_changed(self, mod_cfg, mod_name, value):
        mod_cfg.set_param(mod_name, value)
        self.save_config()

    # endregion

    # region Scenario
    @try_except_wrapper
    def load_scenarios(self):
        self.scenarios.clear()
        sc_dir = self.scenarios_dir
        if not os.path.isdir(sc_dir):
            raise NotADirectoryError('Scenario directory not found')

        for f in os.listdir(sc_dir):
            if not f.endswith(".json"):
                continue
            self.__load_scenario(os.path.join(sc_dir, f))

    @try_except_wrapper
    def __load_scenario(self, file):

        def create_sc_data(block):
            mod_name = block[Constants.MODULE]
            mod = self.modules.get(mod_name)
            if mod is None:
                self.logger.warning(f'Module {mod_name} not found')
                return None
            req_mods.add(mod)
            lazy_init = lambda: mod.init.deserialize_block(block[Constants.DATA])
            return ScenarioData(mod, block[Constants.QUESTION_TYPE], lazy_init)

        with open(file, 'r', encoding='utf-8') as reader:
            content = json.load(reader)

        scenario_name = os.path.basename(file).split('.')[0]
        req_mods = set()
        sc_data = []
        for bl in content:
            data = create_sc_data(bl)
            if data:
                sc_data.append(data)

        scenario = Scenario(scenario_name, required_modules=req_mods, scenario_data=sc_data)
        self.scenarios[scenario_name] = scenario

    @try_except_wrapper
    def save_scenario(self, scenario):
        file = os.path.join(self.scenarios_dir, f'{scenario.name}.json')
        result = []
        for sc_data in scenario.scenario_data:
            block = {
                Constants.MODULE: sc_data.module.name,
                Constants.QUESTION_TYPE: sc_data.quest_type.value,
                Constants.DATA: sc_data.module.init.serialize_block(sc_data.data)
            }
            result.append(block)

        with open(file, 'w', encoding='utf-8') as writer:
            json.dump(result, writer)

    @try_except_wrapper
    def remove_scenario(self, scenario_name):
        self.scenarios.pop(scenario_name)
        os.remove(os.path.join(self.scenarios_dir, f'{scenario_name}.json'))
    # endregion
