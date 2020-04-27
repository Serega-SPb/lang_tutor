import os

from core.abstractions import AbstractModuleInit

from .editor.additional_widgets_word import WordWidget
from .question_generator import QuestionTypes, WordsQuestionGenerator
from .serializer import WordsScenarioSerilizer
from .editor import init as editor_block
from .word import Word
from .translator import ModuleTranslator


DIR = os.path.dirname(__file__)
NAME = DIR.split('/')[-1]
ModuleTranslator.register(NAME, DIR)
QuestionTypes.translate_func = ModuleTranslator.get_value().translate


class Init(AbstractModuleInit):
    __scenario_serializer = WordsScenarioSerilizer()

    def get_name(self):
        return ModuleTranslator.get_value().translate('NAME')

    def get_question_types(self):
        return QuestionTypes.get_types()

    @staticmethod
    def translate_local(var):
        return ModuleTranslator.get_value().translate(var.upper())

    def get_exercises(self, scenario_block, question_type, ex_with_opt=True):
        return self.__exercise_factory.create_exercises(scenario_block, question_type, ex_with_opt)

    def get_question_generator(self):
        return WordsQuestionGenerator

    def serialize_block(self, data):
        return self.__scenario_serializer.serialize(data)

    def deserialize_block(self, data):
        return self.__scenario_serializer.deserialize(data)

    def get_exercise_widget(self):
        pass

    def get_exercise_opt_widget(self):
        pass

    def get_editor_listitem_widget_cls(self):
        return WordWidget

    def get_editor_block_widget(self):
        return editor_block()

    def create_new_data_object(self):
        return Word('?', '?', [])
