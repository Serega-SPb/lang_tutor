from core.data_loader import DataLoader
from core.memento import MementoManager, ChangeMemento
from core.scenario import Scenario, ScenarioData
from ui.cross_widget_events import CrossWidgetEvents, ScreenIndex as ScI
from ui.cross_widget_events import EditorMode as eMode
from ui.ui_messaga_bus import Event


class NotifyEvents:
    scenario_name_changed = Event()


class EditorController:

    WIDGETS = {}

    def __init__(self, model):
        self.model = model
        self.data_loader = DataLoader()
        CrossWidgetEvents.start_editor_event += self.start_editor_handler
        self.memento_manager = MementoManager()
        self.memento_manager.can_undo_changed += self.model.can_undo_changed.emit
        self.memento_manager.can_redo_changed += self.model.can_redo_changed.emit
        NotifyEvents.scenario_name_changed += self.model.update_scenario_name

    def load_modules(self):
        self.model.blocks = [m.name for m in self.data_loader.modules.values() if m.is_enabled]

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

    def create_new_scenario(self):
        self.model.scenario = Scenario('<Untitled>')

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

    def unset_widget(self):
        self.model.block_widget = None

    def set_block_widget(self, block, index):
        if block.module_name in self.WIDGETS.keys():
            wid = self.WIDGETS[block.module_name]
        else:
            mod_init = self.data_loader.get_init(block.module_name)
            wid = mod_init.get_editor_block_widget()
            self.WIDGETS[block.module_name] = wid
        self.model.block_widget = wid
        wid.controller.set_data_index(index)
        wid.controller.load_data(block)

    def save_scenario(self):
        old_sc_name = next((name for name, sc in self.data_loader.scenarios.items()
                            if sc == self.model.scenario), None)
        if old_sc_name:
            self.data_loader.remove_scenario(old_sc_name)
        self.data_loader.save_scenario(self.model.scenario)

    def undo(self):
        self.memento_manager.undo()

    def redo(self):
        self.memento_manager.redo()

    def back_to_menu(self, *args):
        # if self.model.can_undo:
        #     # TODO QuestMsgBx Cancel changes or not? Y/N
        #     self.memento_manager.cancel()
        self.WIDGETS.clear()
        CrossWidgetEvents.reload_scenarios_event.emit()
        CrossWidgetEvents.change_screen_event.emit(ScI.MAIN)

    # endregion

    # region actions with record history
    def add_block(self, block):
        bl = ScenarioData.empty_init(block)
        bl.quest_type = self.data_loader.get_init(block).get_question_types()[0]
        self.model.append_scenario_data(bl)

    def remove_block(self, block):
        self.model.remove_scenario_data(block)

    @ChangeMemento('name', NotifyEvents.scenario_name_changed)
    def change_scenarion_name(self, value):
        self.model.scenario.name = value

    # endregion
