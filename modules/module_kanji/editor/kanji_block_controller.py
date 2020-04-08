from core.memento import MementoManager
from ..storage import KanjiStorage


SEPARATORS = [',', '\n', ';']


def split(txt, seps):
    default_sep = seps[0]
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep) if i]


class EditorBlockController:
    def __init__(self, model):
        self.model = model
        self.storage = KanjiStorage()
        self.memnto_manager = MementoManager()

    def load_keys(self):
        self.model.keys = list(self.storage.kanji_keys.values())

    def load_block_data(self, data, prop_path):
        self.model.prop_path = prop_path
        self.model.set_kanji(data)
        self.load_keys()

    def set_kanji_key(self, value):
        self.model.set_kanji_prop('key', value)
        pass

    def set_kanji_key_by_id(self, num):
        self.set_kanji_key(self.storage.get_key_by_id(num))

    def set_kanji_dash_count(self, value):
        self.model.set_kanji_prop('dash_count', value)

    def set_kanji_value(self, value):
        self.model.set_kanji_prop('value', value)
        self.model.update_label_event.emit()

    def set_kanji_on_reading(self, value):
        self.model.set_kanji_prop('on', split(value, SEPARATORS))

    def set_kanji_kun_reading(self, value):
        self.model.set_kanji_prop('kun', split(value, SEPARATORS))

    def set_kanji_translate(self, value):
        self.model.set_kanji_prop('translate', split(value, SEPARATORS))