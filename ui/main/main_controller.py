import logging

from core.data_loader import DataLoader
from core.log_config import LOGGER_NAME
from ui.cross_widget_events import ScreenIndex as ScI
from ui.cross_widget_events import CrossWidgetEvents as CrossEvent, \
                                    MessageType as MsgType
from ui.translator import Translator


class MainController:
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.data_loader = DataLoader()
        self.tranlator = Translator.get_translator('main')
        self.logger = logging.getLogger(LOGGER_NAME)
        CrossEvent.reload_scenarios_event += self.reload_scenarios
        CrossEvent.locale_changed_event += self.reloads

    def reload_modules(self):
        self.data_loader.load_modules()
        self.model.modules_changed.emit()

    def reload_scenarios(self):
        self.data_loader.load_scenarios()
        self.model.scenarios_changed.emit()

    def start_scenario(self, scenario, opt_enb):
        self.logger.debug(f'Start {scenario.name}')
        check_mod = all(r_mod.is_enabled for r_mod in scenario.required_modules)
        if not check_mod:
            title = self.tranlator.translate('WARNING_TEXT')
            msg = self.tranlator.translate('REQ_MODS_NOT_ENB_TEXT')
            self.logger.debug(msg)
            CrossEvent.show_message_event.emit(MsgType.WARN, title, msg)
            return

        CrossEvent.load_scenario_event.emit(scenario, opt_enb)
        CrossEvent.change_screen_event.emit(ScI.SCENARIO)

    def set_editor_mode(self, value):
        self.model.editor_mode = value

    @staticmethod
    def start_editor(mode, *args):
        CrossEvent.start_editor_event.emit(mode, *args)
        CrossEvent.change_screen_event.emit(ScI.EDITOR)

    def delete_scenarios(self, scenarios):
        def _action():
            [self.data_loader.remove_scenario(sc) for sc in scenarios]
            self.reload_scenarios()

        title = self.tranlator.translate('QUESTION_TITLE')
        msg = self.tranlator.translate('REMOVE_SELECTED_TEXT')
        CrossEvent.show_question_event.emit(title, msg, _action)

    def reloads(self):
        self.reload_modules()
        self.reload_scenarios()
