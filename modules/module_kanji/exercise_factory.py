import random
import logging

from core.abstractions import AbstactExerciseFactory
from core.exercise import Exercise, ExerciseWithOptions
from core.log_config import LOGGER_NAME
from .qustion_generator import KanjiQuestionGenerator


class KanjiExerciseFactory(AbstactExerciseFactory):

    def __init__(self):
        self.logger = logging.getLogger(LOGGER_NAME)
        self.quest_gen = None

    def create_exercises(self, scenario, quest_type, ex_with_opt=True):
        self.quest_gen = KanjiQuestionGenerator(scenario)
        quests = self.quest_gen.get_questions(quest_type)

        return self._create_exercise_opt(quests) if ex_with_opt \
            else self._create_exercise(quests)

    def _create_exercise(self, data):
        result = []
        for q, a in data:
            ex = Exercise(q, a if isinstance(a, list) else [a])
            result.append(ex)
        return result

    def _create_exercise_opt(self, data):
        result = []
        for q, a in data:
            other_answers = [n for m, n in data if a != n]
            if len(other_answers) < 3:
                self.logger.warning('Incorrect scenario or question type')
                continue
            opt_answers = random.sample(other_answers, k=3)
            opt_answers.append(a)
            random.shuffle(opt_answers)
            ex = ExerciseWithOptions(q, a if isinstance(a, list) else [a], opt_answers)
            result.append(ex)
        return result
