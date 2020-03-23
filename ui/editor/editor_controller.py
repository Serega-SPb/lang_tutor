from core.data_loader import DataLoader
from core.scenario import Scenario, ScenarioData
from ui.cross_widget_events import CrossWidgetEvents, ScreenIndex as ScI
from ui.cross_widget_events import EditorMode as eMode


class EditorController:

    WIDGETS = {}

    def __init__(self, model):
        self.model = model
        self.data_loader = DataLoader()
        CrossWidgetEvents.start_editor_event += self.start_editor_handler
        # TODO memento manager

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

    def set_block_widget(self, block):
        if block.module_name in self.WIDGETS.keys():
            wid = self.WIDGETS[block.module_name]
        else:
            mod_init = self.data_loader.get_init(block.module_name)
            wid = mod_init.get_editor_block_widget()
            self.WIDGETS[block.module_name] = wid
        self.model.block_widget = wid
        wid.controller.load_data(block)

    def save_scenario(self):
        # TODO serialize -> send open savefiledialog
        pass

    def undo(self):  # TODO memento manager undo + update status can_undo
        pass

    def redo(self):  # TODO memento manager redo + update status can_redo
        pass

    def back_to_menu(self, *args):
        # TODO QuestMsgBx Cancel changes or not? Y/N + Update scenarios
        self.WIDGETS.clear()
        self.data_loader.load_scenarios()
        CrossWidgetEvents.change_screen_event.emit(ScI.MAIN)

    def test_run(self):  # ?
        pass

    # endregion

    # region actions with record history
    def add_block(self, block):
        self.model.append_scenario_data(ScenarioData.empty_init(block))

    def remove_block(self, block):
        self.model.remove_scenario_data(block)

    def change_scenarion_name(self, value):
        # TODO save old name
        self.model.scenario.name = value

    # endregion
