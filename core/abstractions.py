from abc import ABC, abstractmethod


class AbstractModuleInit(ABC):

    @abstractmethod
    def get_question_types(self):
        pass

    @abstractmethod
    def get_exercises(self, scenario_block, question_type, ex_with_opt=True):
        pass

    @abstractmethod
    def serialize_block(self, data):
        pass

    @abstractmethod
    def deserialize_block(self, data):
        pass


class AbstractQuestionGenerator(ABC):

    # @abstractmethod
    # def get_question_types(self):
    #     pass

    @abstractmethod
    def get_questions(self, quest_type):
        pass


class AbstactExerciseFactory(ABC):

    @abstractmethod
    def create_exercises(self, scenario, quest_type, ex_with_opt):
        pass

    @abstractmethod
    def _create_exercise(self, data):
        pass

    @abstractmethod
    def _create_exercise_opt(self, data):
        pass


class AbstractScenarioSerializer(ABC):

    @abstractmethod
    def serialize(self, m_data):
        pass

    @abstractmethod
    def deserialize(self, sc_data):
        pass
