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

    @abstractmethod
    def get_exercise_widget(self):
        pass

    @abstractmethod
    def get_exercise_opt_widget(self):
        pass


class AbstractQuestionGenerator(ABC):

    @abstractmethod
    def get_questions(self, quest_type):
        pass


class AbstactExerciseFactory(ABC):

    QUEST_GENERATOR_CL = AbstractQuestionGenerator

    def create_exercises(self, scenario, quest_type, ex_with_opt):
        self.quest_gen = self.QUEST_GENERATOR_CL(scenario)
        quests = self.quest_gen.get_questions(quest_type)

        return self._create_exercise_opt(quests) if ex_with_opt \
            else self._create_exercise(quests)

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
