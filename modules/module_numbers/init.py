import os

from core.abstractions import AbstractModuleInit
from core.exercise_factory import ExerciseFactory

from module_numbers.editor.additional_widgets_number import NumberWidget
from module_numbers.question_generator import QuestionTypes, NumbersQuestionGenerator
from module_numbers.serializer import NumbersScenarioSerilizer
from module_numbers.editor import init as editor_block
from module_numbers.number_data import NumberData
from module_numbers.translator import ModuleTranslator


DIR = os.path.dirname(__file__)
NAME = DIR.split('/')[-1]
ModuleTranslator.register(NAME, DIR)
QuestionTypes.translate_func = ModuleTranslator.get_value().translate


class Init(AbstractModuleInit):
    __exercise_factory = ExerciseFactory(NumbersQuestionGenerator)
    __scenario_serializer = NumbersScenarioSerilizer()

    def get_name(self):
        return ModuleTranslator.get_value().translate('NAME')

    def get_question_types(self):
        return QuestionTypes.get_types()

    @staticmethod
    def translate_local(var):
        return ModuleTranslator.get_value().translate(var)

    def get_exercises(self, scenario_block, question_type, ex_with_opt=True):
        return self.__exercise_factory.create_exercises(scenario_block, question_type, ex_with_opt)

    def serialize_block(self, data):
        return self.__scenario_serializer.serialize(data)

    def deserialize_block(self, data):
        return self.__scenario_serializer.deserialize(data)

    def get_exercise_widget(self):
        pass

    def get_exercise_opt_widget(self):
        pass

    def get_editor_listitem_widget_cls(self):
        return NumberWidget

    def get_editor_block_widget(self):
        return editor_block()

    def create_new_data_object(self):
        return NumberData(False, 0, [0, 0], 1)
