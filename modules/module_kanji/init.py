from core.abstractions import AbstractModuleInit
from core.exercise_factory import ExerciseFactory

from .qustion_generator import QuestionTypes, KanjiQuestionGenerator
from .serializer import KanjiScenarioSerilizer
from .storage import KanjiStorage
from .editor import init as editor_block


class Init(AbstractModuleInit):
    __storage = KanjiStorage()
    __exercise_factory = ExerciseFactory(KanjiQuestionGenerator)
    __scenario_serializer = KanjiScenarioSerilizer()

    def get_question_types(self):
        return QuestionTypes.get_types()

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

    def get_editor_block_widget(self):
        return editor_block()
