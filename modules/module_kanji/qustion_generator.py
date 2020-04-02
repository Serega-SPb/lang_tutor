from core.abstractions import AbstractQuestionGenerator


class QuestionTypes:
    KEY_QUESTS = 'key_quests'
    TRANSLATE_QUESTS = 'translate_quests'
    READING_QUESTS = 'reading_quests'
    # TODO ? add types RU->JP | JP->RU

    @staticmethod
    def get_types():
        qt = QuestionTypes
        return qt.KEY_QUESTS, qt.TRANSLATE_QUESTS, qt.READING_QUESTS


class KanjiQuestionGenerator(AbstractQuestionGenerator):

    kanji_list = []
    quest_types = {}

    def __init__(self, scenario_kanji):
        self.kanji_list = scenario_kanji
        self.quest_types = {
            QuestionTypes.KEY_QUESTS: self.get_key_questions,
            QuestionTypes.TRANSLATE_QUESTS: self.get_translate_questions,
            QuestionTypes.READING_QUESTS: self.get_reading_questions,
        }

    def get_questions(self, quest_type):
        return self.quest_types[quest_type]() \
            if quest_type in self.quest_types.keys() else None

    def get_key_questions(self):
        quests = []
        for kan in self.kanji_list:
            if kan.key == kan:
                continue
            q, a = kan.value, f'{kan.key.value}'
            if kan.key.has_reduction:
                a += f' ({", ".join(kan.key.reductions)})'
            quests.append((q, a))
        return quests

    def get_translate_questions(self):
        quests = []
        for kan in self.kanji_list:
            q, a = kan.value, kan.translate
            quests.append((q, a))
        return quests

    def get_reading_questions(self):
        quests = []
        for kan in self.kanji_list:
            q, a = kan.value, kan.on + kan.kun
            quests.append((q, a))
        return quests
