import random

from core.decorators import try_except_wrapper
from core.exercise_factory import ExerciseFactory
from ui.cross_widget_events import ScreenIndex as ScI
from ui.cross_widget_events import CrossWidgetEvents, MessageType as MsgType
from ui.translator import Translator
from ui.exercise_ui_manager import get_widget


class ScenarioController:

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.tranlator = Translator.get_translator('main')
        CrossWidgetEvents.load_scenario_event += self.load_scenario

    @try_except_wrapper
    def load_scenario(self, scenario, opt_enb):
        self.model.name = scenario.name
        exercises = []
        for data in scenario.scenario_data:
            get_widget_lamb = lambda x: (get_widget(data.module.init, x), x)
            q_type = data.quest_type
            factory = ExerciseFactory(data.module.init.get_question_generator())
            exercises.extend(list(map(get_widget_lamb, factory.create_exercises(data.data, q_type, opt_enb))))
        random.shuffle(exercises)
        self.model.set_exercises(exercises)

    def accept_answer(self, answer):
        self.model.check_answer(answer)

    def end_scenario(self):
        title = self.tranlator.translate('RESULTS_TEXT')
        translated_text = self.tranlator.translate('CORRECT_ANSWERS_TEXT')
        msg = f'{translated_text}: {self.model.correct_count}/{self.model.total}'
        CrossWidgetEvents.show_message_event.emit(MsgType.INFO, title, msg)
        self.model.scenario_ended.emit()

    @staticmethod
    def back_to_menu(*args):
        CrossWidgetEvents.change_screen_event.emit(ScI.MAIN)
