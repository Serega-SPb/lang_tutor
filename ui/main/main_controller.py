import logging

from PyQt5.QtWidgets import QMessageBox

from core.data_loader import DataLoader
from core.log_config import LOGGER_NAME


class MainController:
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.data_loader = DataLoader()
        self.logger = logging.getLogger(LOGGER_NAME)

    def reload_modules(self):
        self.data_loader.load_modules()
        self.model.modules_changed.emit()

    def reload_scenarios(self):
        self.data_loader.load_scenarios()
        self.model.scenarios_changed.emit()

    def start_scenario(self, scenario, opt_enb):
        self.logger.debug(f'Start {scenario.name}')
        check_mod = all([self.data_loader.modules[r_mod].init is not None
                         for r_mod in scenario.required_modules])
        if not check_mod:
            self.logger.debug('Not all required modules are enabled')
            QMessageBox.warning(None, 'Warning', 'Not all required modules are enabled')
            return

        if hasattr(self, 'sc_controller'):
            self.sc_controller.load_scenario(scenario, 'translate_quests', opt_enb)
        else:
            self.logger.debug('SCENARIO CONTROLLER NOT FOUND')
