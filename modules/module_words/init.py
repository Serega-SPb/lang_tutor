from core.abstractions import AbstractModuleInit
from core.exercise_factory import ExerciseFactory
from .question_generator import QuestionTypes, WordsQuestionGenerator
from .serializer import WordsScenarioSerilizer
from .editor import init as editor_block


class Init(AbstractModuleInit):
    __exercise_factory = ExerciseFactory(WordsQuestionGenerator)
    __scenario_serializer = WordsScenarioSerilizer()

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
