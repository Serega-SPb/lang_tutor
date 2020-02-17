import logging

from core.data_loader import DataLoader
from core.log_config import LOGGER_NAME
from ui.cross_widget_events import CrossWidgetEvents


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
            CrossWidgetEvents.show_message_event.emit('W', 'Warning', 'Not all required modules are enabled')
            return

        CrossWidgetEvents.load_scenario_event.emit(scenario, 'translate_quests', opt_enb)
        CrossWidgetEvents.change_screen_event.emit(1)