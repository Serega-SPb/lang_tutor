class Exercise:

    def __init__(self, question, correct_answers):
        self.question = question
        self.correct_answers = correct_answers

    def check_answer(self, user_answer):
        return user_answer in self.correct_answers


class ExerciseWithOptions(Exercise):

    def __init__(self, question, correct_answers, options_answers):
        super().__init__(question, correct_answers)
        self.options_answers = options_answers
