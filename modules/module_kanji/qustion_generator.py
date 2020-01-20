from core.abstractions import AbstractQuestionGenerator


class KanjiQuestionGenerator(AbstractQuestionGenerator):

    KEY_QUEST = "f'Which key is correct for this KANJI'"  # TODO load from file

    kanji_list = []
    quest_types = {}

    def __init__(self, scenario_kanji):
        self.kanji_list = scenario_kanji
        self.quest_types = {
            'key_quests': self.get_key_questions,
            'translate_quests': self.get_translate_questions,
            'reading_quests': self.get_reading_questions,
        }

    def get_question_types(self):
        return self.quest_types.keys()

    def get_questions(self, quest_type):
        return self.quest_types[quest_type] \
            if quest_type in self.quest_types.keys() else None

    def get_key_questions(self):
        quests = []
        for kan in self.kanji_list:
            if kan.key == kan:
                continue
            q, a = self.KEY_QUEST.replace('KANJI', kan), kan.key
            quests.append((q, a))
        return quests

    def get_translate_questions(self):
        quests = []
        for kan in self.kanji_list:
            pass
        return quests

    def get_reading_questions(self):
        quests = []
        for kan in self.kanji_list:
            pass
        return quests
