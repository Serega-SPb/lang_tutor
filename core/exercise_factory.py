import random

from core.exercise import Exercise, ExerciseWithOptions
from core.log_config import logger


class ExerciseFactory:

    def __init__(self, quest_generator_cls):
        self.logger = logger
        self.quest_generator_cl = quest_generator_cls

    def create_exercises(self, scenario, quest_type, ex_with_opt):
        self.quest_gen = self.quest_generator_cl(scenario)
        quests = self.quest_gen.get_questions(quest_type)

        return self._create_exercise_opt(quests, quest_type) if ex_with_opt \
            else self._create_exercise(quests, quest_type)

    @staticmethod
    def _create_exercise(data, quest_type):
        result = []
        for quest, answ in data:
            ex = Exercise(quest, answ if isinstance(answ, list) else [answ], quest_type)
            result.append(ex)
            ex_rev = Exercise(','.join(answ) if isinstance(answ, list) else answ, [quest], quest_type)
            result.append(ex_rev)
        return result

    @staticmethod
    def _create_exercise_opt(data, quest_type):
        def gen_opt_answers(o_answs, a):
            sample_k = len(o_answs) if len(o_answs) < 3 else 3
            opt_answers = random.sample(o_answs, k=sample_k)
            opt_answers.append(a)
            random.shuffle(opt_answers)
            return opt_answers

        result = []
        for quest, answ in data:
            other_answers = [a for _, a in data if answ != a]
            opts = gen_opt_answers(other_answers, answ)
            ex_answ = answ if isinstance(answ, list) else [answ]
            ex = ExerciseWithOptions(quest, ex_answ, opts, quest_type)
            result.append(ex)

            rev_other_answers = [q for q, _ in data if quest != q]
            rev_opts = gen_opt_answers(rev_other_answers, quest)
            rev_ex_answ = ','.join(answ) if isinstance(answ, list) else answ
            rev_ex = ExerciseWithOptions(rev_ex_answ, [quest], rev_opts, quest_type)
            result.append(rev_ex)
        return result
