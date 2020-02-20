import logging

from core.data_loader import DataLoader
from core.log_config import LOGGER_NAME
from ui.cross_widget_events import CrossWidgetEvents as CrossEvent, \
                                    MessageType as MsgType


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
        check_mod = all([self.data_loader.get_init(r_mod) is not None
                         for r_mod in scenario.required_modules])
        if not check_mod:
            msg = 'Not all required modules are enabled'
            self.logger.debug(msg)
            CrossEvent.show_message_event.emit(MsgType.WARN, 'Warning', msg)
            return

        CrossEvent.load_scenario_event.emit(scenario, opt_enb)
        CrossEvent.change_screen_event.emit(1)