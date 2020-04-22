import os

from core.abstractions import AbstractModuleInit
from core.exercise_factory import ExerciseFactory

from module_kanji.editor.additional_widgets_kan import KanjiWidget
from module_kanji.kanji import Kanji
from module_kanji.qustion_generator import QuestionTypes, KanjiQuestionGenerator
from module_kanji.serializer import KanjiScenarioSerilizer
from module_kanji.storage import KanjiStorage
from module_kanji.editor import init as editor_block
from module_kanji.translator import ModuleTranslator

DIR = os.path.dirname(__file__)
NAME = DIR.split('/')[-1]
ModuleTranslator.register(NAME, DIR)
QuestionTypes.translate_func = ModuleTranslator.get_value().translate


class Init(AbstractModuleInit):
    __storage = KanjiStorage()
    __exercise_factory = ExerciseFactory(KanjiQuestionGenerator)
    __scenario_serializer = KanjiScenarioSerilizer()

    def get_name(self):
        return ModuleTranslator.get_value().translate('NAME')

    def get_question_types(self):
        return QuestionTypes.get_types()

    @staticmethod
    def translate_local(var):
        return ModuleTranslator.get_value().translate(var.upper())

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
        return KanjiWidget

    def get_editor_block_widget(self):
        return editor_block()

    def create_new_data_object(self):
        return Kanji(self.__storage.get_key_by_id(1), '?', 1)
