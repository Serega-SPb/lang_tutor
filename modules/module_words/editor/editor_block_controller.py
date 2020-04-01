from core.memento import MementoManager
from ..question_generator import QuestionTypes
from ..word import Word


SEPARATORS = [',', '\n', ';']


def split(txt, seps):
    default_sep = seps[0]
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep) if i]


class EditorBlockController:
    def __init__(self, model):
        self.model = model
        self.memnto_manager = MementoManager()

    def set_data_index(self, value):
        self.model.set_data_index(value)

    def set_word_index(self, value):
        self.model.set_word_index(value)

    def load_data(self, sc_data):
        self.model.sc_data = sc_data
        self.load_quest_types()
        self.model.words_changed.emit(self.model.words)

    def load_quest_types(self):
        self.model.quest_types = QuestionTypes.get_types()

    def add_word(self):
        word = Word('', '', [])
        self.model.append_word(word)

    def remove_word(self, value):
        self.model.remove_word(value)

    def select_word(self, value):
        self.model.current_word = value

    # region actions with record history

    def set_quest_type(self, value):
        self.model.quest_type = value

    def set_word_spelling(self, value):
        self.model.set_word_prop('spelling', value)
        self.model.update_label_event.emit()

    def set_word_reading(self, value):
        self.model.set_word_prop('reading', value)
        self.model.update_label_event.emit()

    def set_word_translate(self, value):
        self.model.set_word_prop('translate', split(value, SEPARATORS))

    # endregion
