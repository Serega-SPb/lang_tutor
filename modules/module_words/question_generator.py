from core.abstractions import AbstractQuestionGenerator
from core.scenario import QuestType


class QuestionTypes:
    TRANSLATE_QUESTS = 'translate_quests'
    READING_QUESTS = 'reading_quests'

    translate_func = lambda x: x

    @staticmethod
    def get_types():
        qt = QuestionTypes
        return QuestType(qt.TRANSLATE_QUESTS, qt.translate_func), \
               QuestType(qt.READING_QUESTS, qt.translate_func)


class WordsQuestionGenerator(AbstractQuestionGenerator):

    words = []
    quest_types = {}

    def __init__(self, scenario_words):
        self.words = scenario_words
        self.quest_types = {
            QuestionTypes.TRANSLATE_QUESTS: self.get_translate_questions,
            QuestionTypes.READING_QUESTS: self.get_reading_questions,
        }

    def get_questions(self, quest_type):
        return self.quest_types[quest_type]() \
            if quest_type in self.quest_types.keys() else None

    def get_translate_questions(self):
        quests = []
        for word in self.words:
            q, a = word.spelling, word.translate
            quests.append((q, a))
        return quests

    def get_reading_questions(self):
        quests = []
        for word in self.words:
            q, a = word.spelling, word.reading
            quests.append((q, a))
        return quests
