from core.abstractions import AbstactExerciseFactory
from .qustion_generator import KanjiQuestionGenerator


class KanjiExerciseFactory(AbstactExerciseFactory):

    def __init__(self):
        self.quest_gen = None

    def create_exercises(self, scenario):
        scenario_kanji = []  # TODO extract from scenario
        self.quest_gen = KanjiQuestionGenerator(scenario_kanji)
        # TODO if scenario['ex_with_opt']: _create_exercise_opt; else: _create_exercise

    def _create_exercise(self, data):
        pass

    def _create_exercise_opt(self, data):
        pass
