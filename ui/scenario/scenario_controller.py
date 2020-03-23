import random

from core.data_loader import DataLoader
from ui.cross_widget_events import ScreenIndex as ScI
from ui.cross_widget_events import CrossWidgetEvents, MessageType as MsgType


class ScenarioController:

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.data_loader = DataLoader()
        CrossWidgetEvents.load_scenario_event += self.load_scenario

    def load_scenario(self, scenario, opt_enb):
        self.model.name = scenario.name
        exercises = []
        for data in scenario.scenario_data:
            mod = self.data_loader.get_init(data.module_name)
            tuple_lamb = lambda x: (data.module_name, x)
            q_type = data.quest_type
            exercises.extend(list(map(tuple_lamb, mod.get_exercises(data.data, q_type, opt_enb))))
        random.shuffle(exercises)
        self.model.set_exercises(exercises)

    def accept_answer(self, answer):
        self.model.check_answer(answer)

    def end_scenario(self):
        msg = f'Correct answers: {self.model.correct_count}/{self.model.total}'
        CrossWidgetEvents.show_message_event.emit(MsgType.INFO, 'Results', msg)
        self.model.scenario_ended.emit()

    def back_to_menu(self, *args):
        CrossWidgetEvents.change_screen_event.emit(ScI.MAIN)
