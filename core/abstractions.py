from abc import ABC, abstractmethod


class AbstractQuestionGenerator(ABC):

    @abstractmethod
    def get_question_types(self):
        pass

    @abstractmethod
    def get_questions(self, quest_type):
        pass


class AbstactExerciseFactory(ABC):

    @abstractmethod
    def create_exercises(self, scenario):
        pass

    @abstractmethod
    def _create_exercise(self, data):
        pass

    @abstractmethod
    def _create_exercise_opt(self, data):
        pass
