from ..qustion_generator import QuestionTypes
from ..storage import KanjiStorage
from ..kanji import Kanji


SEPARATORS = [',', '\n', ';']


def split(txt, seps):
    default_sep = seps[0]
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]


class EditorBlockController:

    def __init__(self, model):
        self.model = model
        self.storage = KanjiStorage()

    def load_data(self, sc_data):
        self.model.sc_data = sc_data
        self.loads()
        self.model.kanjis_changed.emit(self.model.kanjis)

    def loads(self):
        self.load_quest_types()
        self.load_keys()

    def load_keys(self):
        self.model.keys = list(self.storage.kanji_keys.values())

    def load_quest_types(self):
        self.model.quest_types = QuestionTypes.get_types()

    def add_kanji(self):
        kanji = Kanji(self.storage.get_key_by_id(1), '', 1)
        self.model.append_kanji(kanji)

    def remove_kanji(self, value):
        self.model.remove_kanji(value)

    def select_kanji(self, value):
        self.model.current_kanji = value

    # region actions with record history

    def set_quest_type(self, value):
        self.model.quest_type = value

    def set_kanji_key(self, value):
        if not self.model.current_kanji:
            return
        self.model.current_kanji.key = value
        pass

    def set_kanji_key_by_id(self, num):
        self.set_kanji_key(self.storage.get_key_by_id(num))

    def set_kanji_dash_count(self, value):
        if not self.model.current_kanji:
            return
        self.model.current_kanji.dash_count = value

    def set_kanji_value(self, value):
        if not self.model.current_kanji:
            return
        self.model.current_kanji.value = value
        self.model.update_label_event.emit()

    def set_kanji_on_reading(self, value):
        if not self.model.current_kanji:
            return
        self.model.current_kanji.on = split(value, SEPARATORS)

    def set_kanji_kun_reading(self, value):
        if not self.model.current_kanji:
            return
        self.model.current_kanji.kun = split(value, SEPARATORS)

    def set_kanji_translate(self, value):
        if not self.model.current_kanji:
            return
        self.model.current_kanji.translate = split(value, SEPARATORS)

    # endregion
