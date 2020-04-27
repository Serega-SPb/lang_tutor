import logging
import os

from core.data_loader import DataLoader, Constants
from core.log_config import LOGGER_NAME
from ui.cross_widget_events import ScreenIndex as ScI
from ui.cross_widget_events import CrossWidgetEvents as CrossEvent, \
                                    MessageType as MsgType
from ui.translator import Translator, Locales


class MainController:
    event_is_exec = False  # Fix double messege shows

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.data_loader = DataLoader()
        self.tranlator = Translator.get_translator('main')
        self.logger = logging.getLogger(LOGGER_NAME)
        CrossEvent.reload_scenarios_event += self.reload_scenarios
        CrossEvent.locale_changed_event += self.reloads

    def exec(self):
        self.reload_modules()
        self.reload_scenarios()
        self.model.set_locales(Locales.get_locales())
        self.model.is_options_enabled = self.data_loader.get_config_param(
            Constants.OPTIONS_ENABLED_PARAM) or False
        self.reload_setting()

    def reload_modules(self):
        self.data_loader.load_modules()
        self.model.update_modules()

    def reload_scenarios(self):
        self.data_loader.load_scenarios()
        self.model.update_scenarios()

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

    def set_is_options_enabled(self, value):
        self.model.is_options_enabled = value
        self.data_loader.set_config_param(Constants.OPTIONS_ENABLED_PARAM, value)

    def select_locale(self, value):
        self.model.current_locale = value

    def show_dir_warning(self):
        if self.event_is_exec:
            return
        self.event_is_exec = True
        title = self.tranlator.translate('WARNING_TEXT')
        msg = self.tranlator.translate('DIR_NOT_FOUND_TEXT')
        CrossEvent.show_message_event.emit(MsgType.WARN, title, msg)
        self.event_is_exec = False

    def set_modules_dir(self, value):
        if not os.path.isdir(value):
            self.show_dir_warning()
            return
        self.model.modules_dir = value

    def set_scenario_dir(self, value):
        if not os.path.isdir(value):
            self.show_dir_warning()
            return
        self.model.scenarios_dir = value

    def apply_settings(self):
        self.data_loader.set_config_param(Constants.MODULES_DIR, self.model.modules_dir)
        self.reload_modules()
        self.data_loader.set_config_param(Constants.SCENARIOS_DIR, self.model.scenarios_dir)
        self.reload_scenarios()
        self.data_loader.set_config_param(Constants.LOCALE, self.model.current_locale)
        Translator.set_locale(self.model.current_locale)
        self.model.is_applied_settings = True

    def reload_setting(self):
        self.model.modules_dir = self.data_loader.modules_dir
        self.model.scenarios_dir = self.data_loader.scenarios_dir
        self.model.current_locale = Translator.get_locale()
        self.model.is_applied_settings = True
