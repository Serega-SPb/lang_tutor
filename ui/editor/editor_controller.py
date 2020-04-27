from core.data_loader import DataLoader
from core.memento import MementoManager, ChangeMemento
from core.scenario import Scenario, ScenarioData
from ui.cross_widget_events import CrossWidgetEvents, ScreenIndex as ScI
from ui.cross_widget_events import EditorMode as eMode
from ui.translator import Translator
from ui.ui_messaga_bus import Event


class EditorController:

    WIDGETS = {}
    MODS = {}

    _save_index = -1

    def __init__(self, model):
        self.model = model
        self.data_loader = DataLoader()
        self.tranlator = Translator.get_translator('main')
        CrossWidgetEvents.start_editor_event += self.start_editor_handler
        self.memento_manager = MementoManager()
        self.memento_manager.can_undo_changed += self.model.can_undo_changed.emit
        self.memento_manager.can_redo_changed += self.model.can_redo_changed.emit
        self.memento_manager.index_changed += \
            lambda x: self.model.can_save_changed.emit(self.can_save)

    @property
    def can_save(self):
        return self._save_index != self.memento_manager.index

    def load_modules(self):
        self.model.blocks = [m for m in self.data_loader.modules.values() if m.is_enabled]

    # region start editor methods

    def start_editor_handler(self, mode, *args):
        if mode == eMode.CREATE_NEW:
            self.create_new_scenario()
        elif mode == eMode.CREATE_FROM:
            self.create_from_scenarios(*args)
        elif mode == eMode.LOAD:
            self.load_scenario(*args)
        else:
            raise ValueError('Inccorect editor mode')
        self.memento_manager.set_subject(self.model.scenario)
        self.load_modules()
        self._save_index = -1

    def create_new_scenario(self):
        def_name = self.tranlator.translate('UNTITLED_TEXT')
        self.model.scenario = Scenario(f'<{def_name}>')

    def create_from_scenarios(self, scenarios):
        names = []
        req_mods = set()
        sc_data = []

        for sc in scenarios:
            names.append(sc.name)
            req_mods.update(sc.required_modules)
            sc_data.extend(sc.scenario_data)

        new_name = ', '.join(names)
        self.model.scenario = Scenario(new_name, required_modules=req_mods, scenario_data=sc_data)

    def load_scenario(self, scenario):
        self.model.scenario = scenario

    # endregion

    # region UI handlers

    def save_scenario(self):
        old_sc_name = next((name for name, sc in self.data_loader.scenarios.items()
                            if sc == self.model.scenario), None)
        if old_sc_name:
            self.data_loader.remove_scenario(old_sc_name)
        self.data_loader.save_scenario(self.model.scenario)
        self._save_index = self.memento_manager.index
        self.model.can_save_changed.emit(self.can_save)

    def undo(self):
        self.memento_manager.undo()

    def redo(self):
        self.memento_manager.redo()

    def back_to_menu(self, *args):
        def _return_action():
            self.WIDGETS.clear()
            CrossWidgetEvents.reload_scenarios_event.emit()
            CrossWidgetEvents.change_screen_event.emit(ScI.MAIN)

        def _cancel_action():
            self.memento_manager.cancel()
            _return_action()

        if self.can_save:
            title = self.tranlator.translate('QUESTION_TITLE')
            msg = self.tranlator.translate('CANCEL_UNSAVED_TEXT')
            CrossWidgetEvents.show_question_event.emit(title, msg, _cancel_action)
        else:
            _return_action()

    def set_sc_block_index(self, value):
        self.model.current_sc_block_index = value
        self.apply_sc_block()

    def apply_sc_block(self):
        curr_sc_block = self.model.get_current_sc_block()
        if curr_sc_block:
            mod_init = curr_sc_block.module.init
            q_types = mod_init.get_question_types()
            li_wid = mod_init.get_editor_listitem_widget_cls()
            bl_wid = mod_init.get_editor_block_widget()
        else:
            q_types, li_wid, bl_wid = None, None, None

        self.model.quest_types = q_types
        self.model.listitem_widget = li_wid
        self.model.block_widget = bl_wid
        self.model.send_sc_block()

    def set_data_index(self, value):
        self.model.current_data_index = value

    # endregion

    # region actions with record history
    def add_block(self, block):
        bl = ScenarioData.empty_init(block)
        self.model.append_scenario_data(bl)

    def remove_block(self, block):
        self.model.remove_scenario_data(block)

    def add_block_data(self):
        mod_init = self.model.get_current_sc_block().module.init
        self.model.append_block_data(mod_init.create_new_data_object())

    def remove_block_data(self, value):
        self.model.remove_block_data(value)

    def set_quest_type(self, value):
        if value:
            self.model.current_quest_type = value

    def change_scenarion_name(self, value):
        @ChangeMemento('name', self.model.update_scenario_name_event)
        def action():
            self.model.scenario.name = value
        action()

    # endregion
