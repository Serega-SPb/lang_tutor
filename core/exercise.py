class Exercise:

    def __init__(self, question, correct_answers, question_type):
        self.question = question
        self.correct_answers = correct_answers
        self.question_type = question_type

    def check_answer(self, user_answer):
        return user_answer in self.correct_answers \
               or self.correct_answers == user_answer

    def __str__(self):
        return self.question


class ExerciseWithOptions(Exercise):

    def __init__(self, question, correct_answers, options_answers, question_type):
        super().__init__(question, correct_answers, question_type)
        self.options_answers = options_answers

    def __str__(self):
        ans_str = "\n".join([f"{i}. {a}" for i, a in enumerate(self.options_answers, 1)])
        return f'{self.question}?\n{ans_str}'
