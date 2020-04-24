import os

from core.abstractions import AbstractModuleInit

from .editor.additional_widgets_kan import KanjiWidget
from .kanji import Kanji
from .qustion_generator import QuestionTypes, KanjiQuestionGenerator
from .serializer import KanjiScenarioSerilizer
from .storage import KanjiStorage
from .editor import init as editor_block
from .translator import ModuleTranslator

DIR = os.path.dirname(__file__)
NAME = DIR.split('/')[-1]
ModuleTranslator.register(NAME, DIR)
QuestionTypes.translate_func = ModuleTranslator.get_value().translate


class Init(AbstractModuleInit):
    __storage = KanjiStorage()
    __scenario_serializer = KanjiScenarioSerilizer()

    def get_name(self):
        return ModuleTranslator.get_value().translate('NAME')

    def get_question_types(self):
        return QuestionTypes.get_types()

    @staticmethod
    def translate_local(var):
        return ModuleTranslator.get_value().translate(var.upper())

    def get_question_generator(self):
        return KanjiQuestionGenerator

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
